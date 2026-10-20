from src.commonmark import render_html


def test_example_651():
    # Spec section: Textual content
    assert render_html('Foo χρῆν\n') == '<p>Foo χρῆν</p>\n'


def test_example_652():
    # Spec section: Textual content
    assert render_html('Multiple     spaces\n') == '<p>Multiple     spaces</p>\n'
