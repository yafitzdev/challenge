from src.commonmark import render_html


def test_example_253():
    # Spec section: List items
    assert render_html('A paragraph\nwith two lines.\n\n    indented code\n\n> A block quote.\n') == '<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n'


def test_example_254():
    # Spec section: List items
    assert render_html('1.  A paragraph\n    with two lines.\n\n        indented code\n\n    > A block quote.\n') == '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>\n'


def test_example_255():
    # Spec section: List items
    assert render_html('- one\n\n two\n') == '<ul>\n<li>one</li>\n</ul>\n<p>two</p>\n'


def test_example_256():
    # Spec section: List items
    assert render_html('- one\n\n  two\n') == '<ul>\n<li>\n<p>one</p>\n<p>two</p>\n</li>\n</ul>\n'


def test_example_257():
    # Spec section: List items
    assert render_html(' -    one\n\n     two\n') == '<ul>\n<li>one</li>\n</ul>\n<pre><code> two\n</code></pre>\n'


def test_example_258():
    # Spec section: List items
    assert render_html(' -    one\n\n      two\n') == '<ul>\n<li>\n<p>one</p>\n<p>two</p>\n</li>\n</ul>\n'


def test_example_259():
    # Spec section: List items
    assert render_html('   > > 1.  one\n>>\n>>     two\n') == '<blockquote>\n<blockquote>\n<ol>\n<li>\n<p>one</p>\n<p>two</p>\n</li>\n</ol>\n</blockquote>\n</blockquote>\n'


def test_example_261():
    # Spec section: List items
    assert render_html('-one\n\n2.two\n') == '<p>-one</p>\n<p>2.two</p>\n'


def test_example_262():
    # Spec section: List items
    assert render_html('- foo\n\n\n  bar\n') == '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>\n'


def test_example_263():
    # Spec section: List items
    assert render_html('1.  foo\n\n    ```\n    bar\n    ```\n\n    baz\n\n    > bam\n') == '<ol>\n<li>\n<p>foo</p>\n<pre><code>bar\n</code></pre>\n<p>baz</p>\n<blockquote>\n<p>bam</p>\n</blockquote>\n</li>\n</ol>\n'


def test_example_264():
    # Spec section: List items
    assert render_html('- Foo\n\n      bar\n\n\n      baz\n') == '<ul>\n<li>\n<p>Foo</p>\n<pre><code>bar\n\n\nbaz\n</code></pre>\n</li>\n</ul>\n'


def test_example_265():
    # Spec section: List items
    assert render_html('123456789. ok\n') == '<ol start="123456789">\n<li>ok</li>\n</ol>\n'


def test_example_266():
    # Spec section: List items
    assert render_html('1234567890. not ok\n') == '<p>1234567890. not ok</p>\n'


def test_example_267():
    # Spec section: List items
    assert render_html('0. ok\n') == '<ol start="0">\n<li>ok</li>\n</ol>\n'


def test_example_268():
    # Spec section: List items
    assert render_html('003. ok\n') == '<ol start="3">\n<li>ok</li>\n</ol>\n'


def test_example_269():
    # Spec section: List items
    assert render_html('-1. not ok\n') == '<p>-1. not ok</p>\n'


def test_example_271():
    # Spec section: List items
    assert render_html('  10.  foo\n\n           bar\n') == '<ol start="10">\n<li>\n<p>foo</p>\n<pre><code>bar\n</code></pre>\n</li>\n</ol>\n'


def test_example_272():
    # Spec section: List items
    assert render_html('    indented code\n\nparagraph\n\n    more code\n') == '<pre><code>indented code\n</code></pre>\n<p>paragraph</p>\n<pre><code>more code\n</code></pre>\n'


def test_example_273():
    # Spec section: List items
    assert render_html('1.     indented code\n\n   paragraph\n\n       more code\n') == '<ol>\n<li>\n<pre><code>indented code\n</code></pre>\n<p>paragraph</p>\n<pre><code>more code\n</code></pre>\n</li>\n</ol>\n'


def test_example_274():
    # Spec section: List items
    assert render_html('1.      indented code\n\n   paragraph\n\n       more code\n') == '<ol>\n<li>\n<pre><code> indented code\n</code></pre>\n<p>paragraph</p>\n<pre><code>more code\n</code></pre>\n</li>\n</ol>\n'


def test_example_275():
    # Spec section: List items
    assert render_html('   foo\n\nbar\n') == '<p>foo</p>\n<p>bar</p>\n'


def test_example_276():
    # Spec section: List items
    assert render_html('-    foo\n\n  bar\n') == '<ul>\n<li>foo</li>\n</ul>\n<p>bar</p>\n'


def test_example_277():
    # Spec section: List items
    assert render_html('-  foo\n\n   bar\n') == '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>\n'


def test_example_278():
    # Spec section: List items
    assert render_html('-\n  foo\n-\n  ```\n  bar\n  ```\n-\n      baz\n') == '<ul>\n<li>foo</li>\n<li>\n<pre><code>bar\n</code></pre>\n</li>\n<li>\n<pre><code>baz\n</code></pre>\n</li>\n</ul>\n'


def test_example_279():
    # Spec section: List items
    assert render_html('-   \n  foo\n') == '<ul>\n<li>foo</li>\n</ul>\n'


def test_example_281():
    # Spec section: List items
    assert render_html('- foo\n-\n- bar\n') == '<ul>\n<li>foo</li>\n<li></li>\n<li>bar</li>\n</ul>\n'


def test_example_282():
    # Spec section: List items
    assert render_html('- foo\n-   \n- bar\n') == '<ul>\n<li>foo</li>\n<li></li>\n<li>bar</li>\n</ul>\n'


def test_example_283():
    # Spec section: List items
    assert render_html('1. foo\n2.\n3. bar\n') == '<ol>\n<li>foo</li>\n<li></li>\n<li>bar</li>\n</ol>\n'


def test_example_284():
    # Spec section: List items
    assert render_html('*\n') == '<ul>\n<li></li>\n</ul>\n'


def test_example_285():
    # Spec section: List items
    assert render_html('foo\n*\n\nfoo\n1.\n') == '<p>foo\n*</p>\n<p>foo\n1.</p>\n'


def test_example_286():
    # Spec section: List items
    assert render_html(' 1.  A paragraph\n     with two lines.\n\n         indented code\n\n     > A block quote.\n') == '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>\n'


def test_example_287():
    # Spec section: List items
    assert render_html('  1.  A paragraph\n      with two lines.\n\n          indented code\n\n      > A block quote.\n') == '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>\n'


def test_example_288():
    # Spec section: List items
    assert render_html('   1.  A paragraph\n       with two lines.\n\n           indented code\n\n       > A block quote.\n') == '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>\n'


def test_example_289():
    # Spec section: List items
    assert render_html('    1.  A paragraph\n        with two lines.\n\n            indented code\n\n        > A block quote.\n') == '<pre><code>1.  A paragraph\n    with two lines.\n\n        indented code\n\n    &gt; A block quote.\n</code></pre>\n'


def test_example_291():
    # Spec section: List items
    assert render_html('  1.  A paragraph\n    with two lines.\n') == '<ol>\n<li>A paragraph\nwith two lines.</li>\n</ol>\n'


def test_example_292():
    # Spec section: List items
    assert render_html('> 1. > Blockquote\ncontinued here.\n') == '<blockquote>\n<ol>\n<li>\n<blockquote>\n<p>Blockquote\ncontinued here.</p>\n</blockquote>\n</li>\n</ol>\n</blockquote>\n'


def test_example_293():
    # Spec section: List items
    assert render_html('> 1. > Blockquote\n> continued here.\n') == '<blockquote>\n<ol>\n<li>\n<blockquote>\n<p>Blockquote\ncontinued here.</p>\n</blockquote>\n</li>\n</ol>\n</blockquote>\n'


def test_example_294():
    # Spec section: List items
    assert render_html('- foo\n  - bar\n    - baz\n      - boo\n') == '<ul>\n<li>foo\n<ul>\n<li>bar\n<ul>\n<li>baz\n<ul>\n<li>boo</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>\n'


def test_example_295():
    # Spec section: List items
    assert render_html('- foo\n - bar\n  - baz\n   - boo\n') == '<ul>\n<li>foo</li>\n<li>bar</li>\n<li>baz</li>\n<li>boo</li>\n</ul>\n'


def test_example_296():
    # Spec section: List items
    assert render_html('10) foo\n    - bar\n') == '<ol start="10">\n<li>foo\n<ul>\n<li>bar</li>\n</ul>\n</li>\n</ol>\n'


def test_example_297():
    # Spec section: List items
    assert render_html('10) foo\n   - bar\n') == '<ol start="10">\n<li>foo</li>\n</ol>\n<ul>\n<li>bar</li>\n</ul>\n'


def test_example_298():
    # Spec section: List items
    assert render_html('- - foo\n') == '<ul>\n<li>\n<ul>\n<li>foo</li>\n</ul>\n</li>\n</ul>\n'


def test_example_299():
    # Spec section: List items
    assert render_html('1. - 2. foo\n') == '<ol>\n<li>\n<ul>\n<li>\n<ol start="2">\n<li>foo</li>\n</ol>\n</li>\n</ul>\n</li>\n</ol>\n'
