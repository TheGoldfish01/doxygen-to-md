from pathlib import Path

from doxygen_to_md import convert


def test_all_doxygen_constructs():
    fixture = Path(__file__).with_name('fixtures').joinpath('doxygen_all.xml')
    xml_text = fixture.read_text(encoding='utf-8')
    md = convert(xml_text)

    # Basic function
    assert '### add(int a, int b)' in md
    assert 'Add two integers.' in md
    # parameter name is linked to function anchor, type is linked to type anchor, and description present
    assert '[`a`](' in md
    assert '[`int`](#type-int)' in md
    assert 'First operand.' in md
    assert 'int result = add(2, 3);' in md
    assert 'Sum of a and b.' in md

    # Class and templated member
    assert '## Math' in md
    assert 'Utility math functions.' in md
    assert '### max(T a, T b)' in md
    assert 'Template parameters:' in md
    assert '[`a`](' in md
    assert '[`T`](#type-t)' in md
    assert 'First value.' in md

    # Enum
    assert '### Enum: Color' in md
    assert '- `Red`' in md

    # Namespace and overloaded functions
    assert '## math' in md
    assert '### add(int a, int b)' in md
    assert '### add(double a, double b)' in md

    # Template free function
    assert '### tmpl(T v)' in md
    assert 'Template parameters:' in md
    assert '[`v`](' in md
    assert '[`T`](#type-t)' in md
    assert 'Value' in md