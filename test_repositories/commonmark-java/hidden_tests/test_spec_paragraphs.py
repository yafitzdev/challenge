from src.commonmark import render_html


def test_example_219():
    # Spec section: Paragraphs
    assert render_html('aaa\n\nbbb\n') == '<p>aaa</p>\n<p>bbb</p>\n'


def test_example_221():
    # Spec section: Paragraphs
    assert render_html('aaa\n\n\nbbb\n') == '<p>aaa</p>\n<p>bbb</p>\n'


def test_example_222():
    # Spec section: Paragraphs
    assert render_html('  aaa\n bbb\n') == '<p>aaa\nbbb</p>\n'


def test_example_223():
    # Spec section: Paragraphs
    assert render_html('aaa\n             bbb\n                                       ccc\n') == '<p>aaa\nbbb\nccc</p>\n'


def test_example_224():
    # Spec section: Paragraphs
    assert render_html('   aaa\nbbb\n') == '<p>aaa\nbbb</p>\n'


def test_example_225():
    # Spec section: Paragraphs
    assert render_html('    aaa\nbbb\n') == '<pre><code>aaa\n</code></pre>\n<p>bbb</p>\n'


def test_example_226():
    # Spec section: Paragraphs
    assert render_html('aaa     \nbbb     \n') == '<p>aaa<br />\nbbb</p>\n'
