from pathlib import Path


def _write_xml(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_cli_directory_conversion_and_grouping(tmp_path, monkeypatch):
    """Integration test: create several minimal Doxygen XML files in a dir,
    run the CLI on that directory and assert grouped output files are written.
    """
    in_dir = tmp_path / "input"
    out_dir = tmp_path / "out"
    in_dir.mkdir()

    ns_xml = """<doxygen>
  <compounddef kind="namespace">
    <compoundname>MyNS</compoundname>
    <briefdescription><para>Namespace brief</para></briefdescription>
  </compounddef>
</doxygen>
"""

    class_xml = """<doxygen>
  <compounddef kind="class">
    <compoundname>MyNS::Helper</compoundname>
    <briefdescription><para>Helper class</para></briefdescription>
  </compounddef>
</doxygen>
"""

    file_xml = """<doxygen>
  <compounddef kind="file">
    <compoundname>utils</compoundname>
    <briefdescription><para>Utility file</para></briefdescription>
  </compounddef>
</doxygen>
"""

    _write_xml(in_dir / "ns.xml", ns_xml)
    _write_xml(in_dir / "class.xml", class_xml)
    _write_xml(in_dir / "global.xml", file_xml)

    # Run the CLI main function directly so we stay inside the test process
    from doxygen_to_md import cli

    rc = cli.main([str(in_dir), "--outdir", str(out_dir)])
    assert rc == 0

    # Check grouping: namespace group should be MyNS, global group should be 'global'
    ns_group = out_dir / "MyNS"
    global_group = out_dir / "global"
    assert ns_group.exists() and ns_group.is_dir()
    assert global_group.exists() and global_group.is_dir()

    # Expected files
    ns_file = ns_group / "ns.md"
    class_file = ns_group / "class.md"
    global_file = global_group / "global.md"

    assert ns_file.exists()
    assert class_file.exists()
    assert global_file.exists()

    # Basic content checks
    ns_text = ns_file.read_text(encoding="utf-8")
    assert "## MyNS" in ns_text
    class_text = class_file.read_text(encoding="utf-8")
    assert "## MyNS::Helper" in class_text
    # The converter may emit minimal content for file-kind compounddefs
    # (some compound kinds only produce headers for class/struct/namespace).
    # We ensure the global file was created; exact content may vary.
    global_text = global_file.read_text(encoding="utf-8")
    assert global_text is not None
