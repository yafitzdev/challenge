from src.commonmark import render_html


def test_example_001():
    # Spec section: Tabs
    assert render_html('\tfoo\tbaz\t\tbim\n') == '<pre><code>foo\tbaz\t\tbim\n</code></pre>\n'


def test_example_002():
    # Spec section: Tabs
    assert render_html('  \tfoo\tbaz\t\tbim\n') == '<pre><code>foo\tbaz\t\tbim\n</code></pre>\n'


def test_example_003():
    # Spec section: Tabs
    assert render_html('    a\ta\n    ὐ\ta\n') == '<pre><code>a\ta\nὐ\ta\n</code></pre>\n'


def test_example_004():
    # Spec section: Tabs
    assert render_html('  - foo\n\n\tbar\n') == '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>\n'


def test_example_005():
    # Spec section: Tabs
    assert render_html('- foo\n\n\t\tbar\n') == '<ul>\n<li>\n<p>foo</p>\n<pre><code>  bar\n</code></pre>\n</li>\n</ul>\n'


def test_example_006():
    # Spec section: Tabs
    assert render_html('>\t\tfoo\n') == '<blockquote>\n<pre><code>  foo\n</code></pre>\n</blockquote>\n'


def test_example_007():
    # Spec section: Tabs
    assert render_html('-\t\tfoo\n') == '<ul>\n<li>\n<pre><code>  foo\n</code></pre>\n</li>\n</ul>\n'


def test_example_008():
    # Spec section: Tabs
    assert render_html('    foo\n\tbar\n') == '<pre><code>foo\nbar\n</code></pre>\n'


def test_example_009():
    # Spec section: Tabs
    assert render_html(' - foo\n   - bar\n\t - baz\n') == '<ul>\n<li>foo\n<ul>\n<li>bar\n<ul>\n<li>baz</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>\n'


def test_example_011():
    # Spec section: Tabs
    assert render_html('*\t*\t*\t\n') == '<hr />\n'
