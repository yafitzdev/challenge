from src.commonmark import render_html


def test_example_648():
    # Spec section: Soft line breaks
    assert render_html('foo\nbaz\n') == '<p>foo\nbaz</p>\n'


def test_example_649():
    # Spec section: Soft line breaks
    assert render_html('foo \n baz\n') == '<p>foo\nbaz</p>\n'
