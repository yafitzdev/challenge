from src.commonmark import render_html


def test_example_327():
    # Spec section: Inlines
    assert render_html('`hi`lo`\n') == '<p><code>hi</code>lo`</p>\n'
