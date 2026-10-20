from src.commonmark import render_html


def test_example_081():
    # Spec section: Setext headings
    assert render_html('Foo *bar\nbaz*\n====\n') == '<h1>Foo <em>bar\nbaz</em></h1>\n'


def test_example_082():
    # Spec section: Setext headings
    assert render_html('  Foo *bar\nbaz*\t\n====\n') == '<h1>Foo <em>bar\nbaz</em></h1>\n'


def test_example_083():
    # Spec section: Setext headings
    assert render_html('Foo\n-------------------------\n\nFoo\n=\n') == '<h2>Foo</h2>\n<h1>Foo</h1>\n'


def test_example_084():
    # Spec section: Setext headings
    assert render_html('   Foo\n---\n\n  Foo\n-----\n\n  Foo\n  ===\n') == '<h2>Foo</h2>\n<h2>Foo</h2>\n<h1>Foo</h1>\n'


def test_example_085():
    # Spec section: Setext headings
    assert render_html('    Foo\n    ---\n\n    Foo\n---\n') == '<pre><code>Foo\n---\n\nFoo\n</code></pre>\n<hr />\n'


def test_example_086():
    # Spec section: Setext headings
    assert render_html('Foo\n   ----      \n') == '<h2>Foo</h2>\n'


def test_example_087():
    # Spec section: Setext headings
    assert render_html('Foo\n    ---\n') == '<p>Foo\n---</p>\n'


def test_example_088():
    # Spec section: Setext headings
    assert render_html('Foo\n= =\n\nFoo\n--- -\n') == '<p>Foo\n= =</p>\n<p>Foo</p>\n<hr />\n'


def test_example_089():
    # Spec section: Setext headings
    assert render_html('Foo  \n-----\n') == '<h2>Foo</h2>\n'


def test_example_091():
    # Spec section: Setext headings
    assert render_html('`Foo\n----\n`\n\n<a title="a lot\n---\nof dashes"/>\n') == '<h2>`Foo</h2>\n<p>`</p>\n<h2>&lt;a title=&quot;a lot</h2>\n<p>of dashes&quot;/&gt;</p>\n'


def test_example_092():
    # Spec section: Setext headings
    assert render_html('> Foo\n---\n') == '<blockquote>\n<p>Foo</p>\n</blockquote>\n<hr />\n'


def test_example_093():
    # Spec section: Setext headings
    assert render_html('> foo\nbar\n===\n') == '<blockquote>\n<p>foo\nbar\n===</p>\n</blockquote>\n'


def test_example_094():
    # Spec section: Setext headings
    assert render_html('- Foo\n---\n') == '<ul>\n<li>Foo</li>\n</ul>\n<hr />\n'


def test_example_095():
    # Spec section: Setext headings
    assert render_html('Foo\nBar\n---\n') == '<h2>Foo\nBar</h2>\n'


def test_example_096():
    # Spec section: Setext headings
    assert render_html('---\nFoo\n---\nBar\n---\nBaz\n') == '<hr />\n<h2>Foo</h2>\n<h2>Bar</h2>\n<p>Baz</p>\n'


def test_example_097():
    # Spec section: Setext headings
    assert render_html('\n====\n') == '<p>====</p>\n'


def test_example_098():
    # Spec section: Setext headings
    assert render_html('---\n---\n') == '<hr />\n<hr />\n'


def test_example_099():
    # Spec section: Setext headings
    assert render_html('- foo\n-----\n') == '<ul>\n<li>foo</li>\n</ul>\n<hr />\n'


def test_example_101():
    # Spec section: Setext headings
    assert render_html('> foo\n-----\n') == '<blockquote>\n<p>foo</p>\n</blockquote>\n<hr />\n'


def test_example_102():
    # Spec section: Setext headings
    assert render_html('\\> foo\n------\n') == '<h2>&gt; foo</h2>\n'


def test_example_103():
    # Spec section: Setext headings
    assert render_html('Foo\n\nbar\n---\nbaz\n') == '<p>Foo</p>\n<h2>bar</h2>\n<p>baz</p>\n'


def test_example_104():
    # Spec section: Setext headings
    assert render_html('Foo\nbar\n\n---\n\nbaz\n') == '<p>Foo\nbar</p>\n<hr />\n<p>baz</p>\n'


def test_example_105():
    # Spec section: Setext headings
    assert render_html('Foo\nbar\n* * *\nbaz\n') == '<p>Foo\nbar</p>\n<hr />\n<p>baz</p>\n'


def test_example_106():
    # Spec section: Setext headings
    assert render_html('Foo\nbar\n\\---\nbaz\n') == '<p>Foo\nbar\n---\nbaz</p>\n'
