from src.commonmark import render_html


def test_example_042():
    # Spec section: Precedence
    assert render_html('- `one\n- two`\n') == '<ul>\n<li>`one</li>\n<li>two`</li>\n</ul>\n'
