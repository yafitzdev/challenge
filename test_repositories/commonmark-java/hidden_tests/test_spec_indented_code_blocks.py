from src.commonmark import render_html


def test_example_107():
    # Spec section: Indented code blocks
    assert render_html('    a simple\n      indented code block\n') == '<pre><code>a simple\n  indented code block\n</code></pre>\n'


def test_example_108():
    # Spec section: Indented code blocks
    assert render_html('  - foo\n\n    bar\n') == '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>\n'


def test_example_109():
    # Spec section: Indented code blocks
    assert render_html('1.  foo\n\n    - bar\n') == '<ol>\n<li>\n<p>foo</p>\n<ul>\n<li>bar</li>\n</ul>\n</li>\n</ol>\n'


def test_example_111():
    # Spec section: Indented code blocks
    assert render_html('    chunk1\n\n    chunk2\n  \n \n \n    chunk3\n') == '<pre><code>chunk1\n\nchunk2\n\n\n\nchunk3\n</code></pre>\n'


def test_example_112():
    # Spec section: Indented code blocks
    assert render_html('    chunk1\n      \n      chunk2\n') == '<pre><code>chunk1\n  \n  chunk2\n</code></pre>\n'


def test_example_113():
    # Spec section: Indented code blocks
    assert render_html('Foo\n    bar\n\n') == '<p>Foo\nbar</p>\n'


def test_example_114():
    # Spec section: Indented code blocks
    assert render_html('    foo\nbar\n') == '<pre><code>foo\n</code></pre>\n<p>bar</p>\n'


def test_example_115():
    # Spec section: Indented code blocks
    assert render_html('# Heading\n    foo\nHeading\n------\n    foo\n----\n') == '<h1>Heading</h1>\n<pre><code>foo\n</code></pre>\n<h2>Heading</h2>\n<pre><code>foo\n</code></pre>\n<hr />\n'


def test_example_116():
    # Spec section: Indented code blocks
    assert render_html('        foo\n    bar\n') == '<pre><code>    foo\nbar\n</code></pre>\n'


def test_example_117():
    # Spec section: Indented code blocks
    assert render_html('\n    \n    foo\n    \n\n') == '<pre><code>foo\n</code></pre>\n'


def test_example_118():
    # Spec section: Indented code blocks
    assert render_html('    foo  \n') == '<pre><code>foo  \n</code></pre>\n'
