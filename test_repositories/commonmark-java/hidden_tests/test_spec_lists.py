from src.commonmark import render_html


def test_example_301():
    # Spec section: Lists
    assert render_html('- foo\n- bar\n+ baz\n') == '<ul>\n<li>foo</li>\n<li>bar</li>\n</ul>\n<ul>\n<li>baz</li>\n</ul>\n'


def test_example_302():
    # Spec section: Lists
    assert render_html('1. foo\n2. bar\n3) baz\n') == '<ol>\n<li>foo</li>\n<li>bar</li>\n</ol>\n<ol start="3">\n<li>baz</li>\n</ol>\n'


def test_example_303():
    # Spec section: Lists
    assert render_html('Foo\n- bar\n- baz\n') == '<p>Foo</p>\n<ul>\n<li>bar</li>\n<li>baz</li>\n</ul>\n'


def test_example_304():
    # Spec section: Lists
    assert render_html('The number of windows in my house is\n14.  The number of doors is 6.\n') == '<p>The number of windows in my house is\n14.  The number of doors is 6.</p>\n'


def test_example_305():
    # Spec section: Lists
    assert render_html('The number of windows in my house is\n1.  The number of doors is 6.\n') == '<p>The number of windows in my house is</p>\n<ol>\n<li>The number of doors is 6.</li>\n</ol>\n'


def test_example_306():
    # Spec section: Lists
    assert render_html('- foo\n\n- bar\n\n\n- baz\n') == '<ul>\n<li>\n<p>foo</p>\n</li>\n<li>\n<p>bar</p>\n</li>\n<li>\n<p>baz</p>\n</li>\n</ul>\n'


def test_example_307():
    # Spec section: Lists
    assert render_html('- foo\n  - bar\n    - baz\n\n\n      bim\n') == '<ul>\n<li>foo\n<ul>\n<li>bar\n<ul>\n<li>\n<p>baz</p>\n<p>bim</p>\n</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>\n'


def test_example_308():
    # Spec section: Lists
    assert render_html('- foo\n- bar\n\n<!-- -->\n\n- baz\n- bim\n') == '<ul>\n<li>foo</li>\n<li>bar</li>\n</ul>\n<!-- -->\n<ul>\n<li>baz</li>\n<li>bim</li>\n</ul>\n'


def test_example_309():
    # Spec section: Lists
    assert render_html('-   foo\n\n    notcode\n\n-   foo\n\n<!-- -->\n\n    code\n') == '<ul>\n<li>\n<p>foo</p>\n<p>notcode</p>\n</li>\n<li>\n<p>foo</p>\n</li>\n</ul>\n<!-- -->\n<pre><code>code\n</code></pre>\n'


def test_example_311():
    # Spec section: Lists
    assert render_html('1. a\n\n  2. b\n\n   3. c\n') == '<ol>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n<li>\n<p>c</p>\n</li>\n</ol>\n'


def test_example_312():
    # Spec section: Lists
    assert render_html('- a\n - b\n  - c\n   - d\n    - e\n') == '<ul>\n<li>a</li>\n<li>b</li>\n<li>c</li>\n<li>d\n- e</li>\n</ul>\n'


def test_example_313():
    # Spec section: Lists
    assert render_html('1. a\n\n  2. b\n\n    3. c\n') == '<ol>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n</ol>\n<pre><code>3. c\n</code></pre>\n'


def test_example_314():
    # Spec section: Lists
    assert render_html('- a\n- b\n\n- c\n') == '<ul>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n<li>\n<p>c</p>\n</li>\n</ul>\n'


def test_example_315():
    # Spec section: Lists
    assert render_html('* a\n*\n\n* c\n') == '<ul>\n<li>\n<p>a</p>\n</li>\n<li></li>\n<li>\n<p>c</p>\n</li>\n</ul>\n'


def test_example_316():
    # Spec section: Lists
    assert render_html('- a\n- b\n\n  c\n- d\n') == '<ul>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n<p>c</p>\n</li>\n<li>\n<p>d</p>\n</li>\n</ul>\n'


def test_example_317():
    # Spec section: Lists
    assert render_html('- a\n- b\n\n  [ref]: /url\n- d\n') == '<ul>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n<li>\n<p>d</p>\n</li>\n</ul>\n'


def test_example_318():
    # Spec section: Lists
    assert render_html('- a\n- ```\n  b\n\n\n  ```\n- c\n') == '<ul>\n<li>a</li>\n<li>\n<pre><code>b\n\n\n</code></pre>\n</li>\n<li>c</li>\n</ul>\n'


def test_example_319():
    # Spec section: Lists
    assert render_html('- a\n  - b\n\n    c\n- d\n') == '<ul>\n<li>a\n<ul>\n<li>\n<p>b</p>\n<p>c</p>\n</li>\n</ul>\n</li>\n<li>d</li>\n</ul>\n'


def test_example_321():
    # Spec section: Lists
    assert render_html('- a\n  > b\n  ```\n  c\n  ```\n- d\n') == '<ul>\n<li>a\n<blockquote>\n<p>b</p>\n</blockquote>\n<pre><code>c\n</code></pre>\n</li>\n<li>d</li>\n</ul>\n'


def test_example_322():
    # Spec section: Lists
    assert render_html('- a\n') == '<ul>\n<li>a</li>\n</ul>\n'


def test_example_323():
    # Spec section: Lists
    assert render_html('- a\n  - b\n') == '<ul>\n<li>a\n<ul>\n<li>b</li>\n</ul>\n</li>\n</ul>\n'


def test_example_324():
    # Spec section: Lists
    assert render_html('1. ```\n   foo\n   ```\n\n   bar\n') == '<ol>\n<li>\n<pre><code>foo\n</code></pre>\n<p>bar</p>\n</li>\n</ol>\n'


def test_example_325():
    # Spec section: Lists
    assert render_html('* foo\n  * bar\n\n  baz\n') == '<ul>\n<li>\n<p>foo</p>\n<ul>\n<li>bar</li>\n</ul>\n<p>baz</p>\n</li>\n</ul>\n'


def test_example_326():
    # Spec section: Lists
    assert render_html('- a\n  - b\n  - c\n\n- d\n  - e\n  - f\n') == '<ul>\n<li>\n<p>a</p>\n<ul>\n<li>b</li>\n<li>c</li>\n</ul>\n</li>\n<li>\n<p>d</p>\n<ul>\n<li>e</li>\n<li>f</li>\n</ul>\n</li>\n</ul>\n'
