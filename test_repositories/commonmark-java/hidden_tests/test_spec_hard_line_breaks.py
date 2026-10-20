from src.commonmark import render_html


def test_example_633():
    # Spec section: Hard line breaks
    assert render_html('foo  \nbaz\n') == '<p>foo<br />\nbaz</p>\n'


def test_example_634():
    # Spec section: Hard line breaks
    assert render_html('foo\\\nbaz\n') == '<p>foo<br />\nbaz</p>\n'


def test_example_635():
    # Spec section: Hard line breaks
    assert render_html('foo       \nbaz\n') == '<p>foo<br />\nbaz</p>\n'


def test_example_636():
    # Spec section: Hard line breaks
    assert render_html('foo  \n     bar\n') == '<p>foo<br />\nbar</p>\n'


def test_example_637():
    # Spec section: Hard line breaks
    assert render_html('foo\\\n     bar\n') == '<p>foo<br />\nbar</p>\n'


def test_example_638():
    # Spec section: Hard line breaks
    assert render_html('*foo  \nbar*\n') == '<p><em>foo<br />\nbar</em></p>\n'


def test_example_639():
    # Spec section: Hard line breaks
    assert render_html('*foo\\\nbar*\n') == '<p><em>foo<br />\nbar</em></p>\n'


def test_example_641():
    # Spec section: Hard line breaks
    assert render_html('`code\\\nspan`\n') == '<p><code>code\\ span</code></p>\n'


def test_example_642():
    # Spec section: Hard line breaks
    assert render_html('<a href="foo  \nbar">\n') == '<p><a href="foo  \nbar"></p>\n'


def test_example_643():
    # Spec section: Hard line breaks
    assert render_html('<a href="foo\\\nbar">\n') == '<p><a href="foo\\\nbar"></p>\n'


def test_example_644():
    # Spec section: Hard line breaks
    assert render_html('foo\\\n') == '<p>foo\\</p>\n'


def test_example_645():
    # Spec section: Hard line breaks
    assert render_html('foo  \n') == '<p>foo</p>\n'


def test_example_646():
    # Spec section: Hard line breaks
    assert render_html('### foo\\\n') == '<h3>foo\\</h3>\n'


def test_example_647():
    # Spec section: Hard line breaks
    assert render_html('### foo  \n') == '<h3>foo</h3>\n'
