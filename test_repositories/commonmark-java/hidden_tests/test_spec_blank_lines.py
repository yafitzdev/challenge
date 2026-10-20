from src.commonmark import render_html


def test_example_227():
    # Spec section: Blank lines
    assert render_html('  \n\naaa\n  \n\n# aaa\n\n  \n') == '<p>aaa</p>\n<h1>aaa</h1>\n'
