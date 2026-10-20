from src.commonmark import render_html


def test_example_228():
    # Spec section: Block quotes
    assert render_html('> # Foo\n> bar\n> baz\n') == '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>\n'


def test_example_229():
    # Spec section: Block quotes
    assert render_html('># Foo\n>bar\n> baz\n') == '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>\n'


def test_example_231():
    # Spec section: Block quotes
    assert render_html('    > # Foo\n    > bar\n    > baz\n') == '<pre><code>&gt; # Foo\n&gt; bar\n&gt; baz\n</code></pre>\n'


def test_example_232():
    # Spec section: Block quotes
    assert render_html('> # Foo\n> bar\nbaz\n') == '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>\n'


def test_example_233():
    # Spec section: Block quotes
    assert render_html('> bar\nbaz\n> foo\n') == '<blockquote>\n<p>bar\nbaz\nfoo</p>\n</blockquote>\n'


def test_example_234():
    # Spec section: Block quotes
    assert render_html('> foo\n---\n') == '<blockquote>\n<p>foo</p>\n</blockquote>\n<hr />\n'


def test_example_235():
    # Spec section: Block quotes
    assert render_html('> - foo\n- bar\n') == '<blockquote>\n<ul>\n<li>foo</li>\n</ul>\n</blockquote>\n<ul>\n<li>bar</li>\n</ul>\n'


def test_example_236():
    # Spec section: Block quotes
    assert render_html('>     foo\n    bar\n') == '<blockquote>\n<pre><code>foo\n</code></pre>\n</blockquote>\n<pre><code>bar\n</code></pre>\n'


def test_example_237():
    # Spec section: Block quotes
    assert render_html('> ```\nfoo\n```\n') == '<blockquote>\n<pre><code></code></pre>\n</blockquote>\n<p>foo</p>\n<pre><code></code></pre>\n'


def test_example_238():
    # Spec section: Block quotes
    assert render_html('> foo\n    - bar\n') == '<blockquote>\n<p>foo\n- bar</p>\n</blockquote>\n'


def test_example_239():
    # Spec section: Block quotes
    assert render_html('>\n') == '<blockquote>\n</blockquote>\n'


def test_example_241():
    # Spec section: Block quotes
    assert render_html('>\n> foo\n>  \n') == '<blockquote>\n<p>foo</p>\n</blockquote>\n'


def test_example_242():
    # Spec section: Block quotes
    assert render_html('> foo\n\n> bar\n') == '<blockquote>\n<p>foo</p>\n</blockquote>\n<blockquote>\n<p>bar</p>\n</blockquote>\n'


def test_example_243():
    # Spec section: Block quotes
    assert render_html('> foo\n> bar\n') == '<blockquote>\n<p>foo\nbar</p>\n</blockquote>\n'


def test_example_244():
    # Spec section: Block quotes
    assert render_html('> foo\n>\n> bar\n') == '<blockquote>\n<p>foo</p>\n<p>bar</p>\n</blockquote>\n'


def test_example_245():
    # Spec section: Block quotes
    assert render_html('foo\n> bar\n') == '<p>foo</p>\n<blockquote>\n<p>bar</p>\n</blockquote>\n'


def test_example_246():
    # Spec section: Block quotes
    assert render_html('> aaa\n***\n> bbb\n') == '<blockquote>\n<p>aaa</p>\n</blockquote>\n<hr />\n<blockquote>\n<p>bbb</p>\n</blockquote>\n'


def test_example_247():
    # Spec section: Block quotes
    assert render_html('> bar\nbaz\n') == '<blockquote>\n<p>bar\nbaz</p>\n</blockquote>\n'


def test_example_248():
    # Spec section: Block quotes
    assert render_html('> bar\n\nbaz\n') == '<blockquote>\n<p>bar</p>\n</blockquote>\n<p>baz</p>\n'


def test_example_249():
    # Spec section: Block quotes
    assert render_html('> bar\n>\nbaz\n') == '<blockquote>\n<p>bar</p>\n</blockquote>\n<p>baz</p>\n'


def test_example_251():
    # Spec section: Block quotes
    assert render_html('>>> foo\n> bar\n>>baz\n') == '<blockquote>\n<blockquote>\n<blockquote>\n<p>foo\nbar\nbaz</p>\n</blockquote>\n</blockquote>\n</blockquote>\n'


def test_example_252():
    # Spec section: Block quotes
    assert render_html('>     code\n\n>    not code\n') == '<blockquote>\n<pre><code>code\n</code></pre>\n</blockquote>\n<blockquote>\n<p>not code</p>\n</blockquote>\n'
