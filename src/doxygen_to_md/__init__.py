"""doxygen_to_md

Minimal public package interface and version.
"""

from __future__ import annotations

__version__ = "0.0.0"

__all__ = ["convert"]

from typing import List
from xml.etree import ElementTree as ET


def _text_from_elem(elem: ET.Element) -> str:
    """Return the concatenated text content of an element's paragraphs.

    Joins child <para> elements with double newlines for Markdown paragraphs.
    """
    paras: List[str] = []
    for p in elem.findall("para"):
        text = "".join(p.itertext()).strip()
        if text:
            paras.append(text)
    # if there are no <para> children, fallback to any text
    if not paras:
        text = "".join(elem.itertext()).strip()
        if text:
            paras = [text]
    return "\n\n".join(paras)


def convert(doxygen_text: str) -> str:
    """Convert minimal Doxygen XML content to Markdown.

    - If the input appears to be Doxygen XML (contains a top-level <doxygen>),
      this parser will extract `memberdef` (function) entries and convert them
      to a small Markdown representation including name, brief, params,
      return description, and code examples.
    - For non-XML input, falls back to a conservative strip of common
      leading comment markers.

    This implementation focuses on the small set of tags used by the
    repository's tests/fixtures and is intentionally lightweight.

    Args:
        doxygen_text: Doxygen XML text (or a comment string fallback).

    Returns:
        Markdown string.
    """
    # Expect valid Doxygen XML; fail fast on parse error so caller knows input
    try:
        root = ET.fromstring(doxygen_text)
    except ET.ParseError as exc:
        raise ValueError("Input is not valid XML Doxygen output") from exc

    md_parts: List[str] = []

    # Handle compound types first (classes, structs, files)
    for comp in root.findall(".//compounddef"):
        kind = comp.get("kind", "")
        cname = comp.findtext("compoundname") or ""
        if kind in ("class", "struct", "namespace"):
            md_parts.append(f"## {cname}")
            brief = comp.find("briefdescription")
            if brief is not None:
                bt = _text_from_elem(brief)
                if bt:
                    md_parts.append(bt)
            deta = comp.find("detaileddescription")
            if deta is not None:
                dt = _text_from_elem(deta)
                if dt:
                    md_parts.append(dt)

        # Enums inside compounddef
        for enum in comp.findall(".//enum"):
            ename = enum.findtext("name") or enum.findtext("definition") or ""
            md_parts.append(f"### Enum: {ename}")
            brief = enum.find("briefdescription")
            if brief is not None:
                bt = _text_from_elem(brief)
                if bt:
                    md_parts.append(bt)
            # enum values
            for ev in enum.findall("enumvalue"):
                vname = ev.findtext("name") or ev.findtext("id") or ""
                vbrief = _text_from_elem(ev.find("briefdescription") or ET.Element(""))
                md_parts.append(f"- `{vname}`: {vbrief}")

    # Now handle memberdef entries (functions, enums, variables, etc.)
    for member in root.findall(".//memberdef"):
        name = member.findtext("name") or ""
        args = member.findtext("argsstring") or ""
        ret_type = (member.findtext("type") or "").strip()

        header = f"### {name}{args}"
        md_parts.append(header)

        def _anchor(text: str) -> str:
            s = text.lower()
            # keep alnum and replace others with hyphens
            import re

            s = re.sub(r"[^a-z0-9]+", "-", s)
            s = s.strip("-")
            return s

        func_anchor = _anchor(f"{name} {args}")

        # brief
        brief = member.find("briefdescription")
        if brief is not None:
            brief_text = _text_from_elem(brief)
            if brief_text:
                md_parts.append(f"**Brief:** {brief_text}")

        # detailed description
        detailed = member.find("detaileddescription")
        if detailed is not None:
            detail_text = _text_from_elem(detailed)
            if detail_text:
                md_parts.append(detail_text)

            # programlisting -> fenced code block
            for prog in detailed.findall("programlisting"):
                code = "".join(prog.itertext()).strip("\n")
                if code:
                    md_parts.append("```cpp\n" + code.strip() + "\n```")

            # simplesect kind=return
            for s in detailed.findall("simplesect"):
                if s.get("kind") == "return":
                    ret_text = _text_from_elem(s)
                    if ret_text:
                        md_parts.append(f"**Returns:** {ret_text}")

        # params -> render as a Markdown table: Name | Type | Description
        params = member.findall("param")
        if params:
            md_parts.append("**Parameters:**")
            md_parts.append("| Name | Type | Description |")
            md_parts.append("| --- | --- | --- |")
            for p in params:
                pname = p.findtext("declname") or p.findtext("defname") or ""
                ptype = (p.findtext("type") or "").strip()
                pbrief = _text_from_elem(p.find("briefdescription") or ET.Element(""))
                # format type as inline code and link type name to a type anchor
                type_anchor = _anchor(ptype or "")
                ptype_fmt = f"`{ptype}`"
                if type_anchor:
                    ptype_fmt = f"[`{ptype}`](#type-{type_anchor})"
                # link parameter name to function anchor + param name
                pname_anchor = _anchor(pname)
                pname_link = (
                    f"[`{pname}`](#{func_anchor}-{pname_anchor})" if pname else ""
                )
                md_parts.append(f"| {pname_link} | {ptype_fmt} | {pbrief} |")

        # template parameters (templateparamlist)
        tpl = member.find("templateparamlist") or member.find("../templateparamlist")
        if tpl is not None:
            tparams = []
            for t in tpl.findall("param"):
                tname = t.findtext("type") or "".join(t.itertext()).strip()
                tparams.append(tname.strip())
            if tparams:
                md_parts.append("**Template parameters:**")
                for tp in tparams:
                    md_parts.append(f"- {tp}")

        # return type (fallback)
        if ret_type and not any(p.startswith("**Returns:**") for p in md_parts[-3:]):
            md_parts.append(f"**Type:** {ret_type}")

        md_parts.append("")

    return "\n".join(md_parts).strip() + "\n"
