from src.commonmark import render_html


def test_example_010():
    # Spec section: Tabs
    assert render_html('#\tFoo\n') == '<h1>Foo</h1>\n'


def test_example_020():
    # Spec section: Backslash escapes
    assert render_html('<https://example.com?find=\\*>\n') == '<p><a href="https://example.com?find=%5C*">https://example.com?find=\\*</a></p>\n'


def test_example_030():
    # Spec section: Entity and numeric character references
    assert render_html('&MadeUpEntity;\n') == '<p>&amp;MadeUpEntity;</p>\n'


def test_example_040():
    # Spec section: Entity and numeric character references
    assert render_html('&#9;foo\n') == '<p>\tfoo</p>\n'


def test_example_050():
    # Spec section: Thematic breaks
    assert render_html('_____________________________________\n') == '<hr />\n'


def test_example_060():
    # Spec section: Thematic breaks
    assert render_html('* Foo\n* * *\n* Bar\n') == '<ul>\n<li>Foo</li>\n</ul>\n<hr />\n<ul>\n<li>Bar</li>\n</ul>\n'


def test_example_070():
    # Spec section: ATX headings
    assert render_html('foo\n    # bar\n') == '<p>foo\n# bar</p>\n'


def test_example_080():
    # Spec section: Setext headings
    assert render_html('Foo *bar*\n=========\n\nFoo *bar*\n---------\n') == '<h1>Foo <em>bar</em></h1>\n<h2>Foo <em>bar</em></h2>\n'


def test_example_090():
    # Spec section: Setext headings
    assert render_html('Foo\\\n----\n') == '<h2>Foo\\</h2>\n'


def test_example_100():
    # Spec section: Setext headings
    assert render_html('    foo\n---\n') == '<pre><code>foo\n</code></pre>\n<hr />\n'


def test_example_110():
    # Spec section: Indented code blocks
    assert render_html('    <a/>\n    *hi*\n\n    - one\n') == '<pre><code>&lt;a/&gt;\n*hi*\n\n- one\n</code></pre>\n'


def test_example_120():
    # Spec section: Fenced code blocks
    assert render_html('~~~\n<\n >\n~~~\n') == '<pre><code>&lt;\n &gt;\n</code></pre>\n'


def test_example_130():
    # Spec section: Fenced code blocks
    assert render_html('```\n```\n') == '<pre><code></code></pre>\n'


def test_example_140():
    # Spec section: Fenced code blocks
    assert render_html('foo\n```\nbar\n```\nbaz\n') == '<p>foo</p>\n<pre><code>bar\n</code></pre>\n<p>baz</p>\n'


def test_example_150():
    # Spec section: HTML blocks
    assert render_html(' <div>\n  *hello*\n         <foo><a>\n') == ' <div>\n  *hello*\n         <foo><a>\n'


def test_example_160():
    # Spec section: HTML blocks
    assert render_html('<table><tr><td>\nfoo\n</td></tr></table>\n') == '<table><tr><td>\nfoo\n</td></tr></table>\n'


def test_example_170():
    # Spec section: HTML blocks
    assert render_html('<script type="text/javascript">\n// JavaScript example\n\ndocument.getElementById("demo").innerHTML = "Hello JavaScript!";\n</script>\nokay\n') == '<script type="text/javascript">\n// JavaScript example\n\ndocument.getElementById("demo").innerHTML = "Hello JavaScript!";\n</script>\n<p>okay</p>\n'


def test_example_180():
    # Spec section: HTML blocks
    assert render_html("<?php\n\n  echo '>';\n\n?>\nokay\n") == "<?php\n\n  echo '>';\n\n?>\n<p>okay</p>\n"


def test_example_190():
    # Spec section: HTML blocks
    assert render_html('<table>\n\n<tr>\n\n<td>\nHi\n</td>\n\n</tr>\n\n</table>\n') == '<table>\n<tr>\n<td>\nHi\n</td>\n</tr>\n</table>\n'


def test_example_200():
    # Spec section: Link reference definitions
    assert render_html('[foo]: <>\n\n[foo]\n') == '<p><a href="">foo</a></p>\n'


def test_example_210():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /url\n"title" ok\n') == '<p>&quot;title&quot; ok</p>\n'


def test_example_220():
    # Spec section: Paragraphs
    assert render_html('aaa\nbbb\n\nccc\nddd\n') == '<p>aaa\nbbb</p>\n<p>ccc\nddd</p>\n'


def test_example_230():
    # Spec section: Block quotes
    assert render_html('   > # Foo\n   > bar\n > baz\n') == '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>\n'


def test_example_240():
    # Spec section: Block quotes
    assert render_html('>\n>  \n> \n') == '<blockquote>\n</blockquote>\n'


def test_example_250():
    # Spec section: Block quotes
    assert render_html('> > > foo\nbar\n') == '<blockquote>\n<blockquote>\n<blockquote>\n<p>foo\nbar</p>\n</blockquote>\n</blockquote>\n</blockquote>\n'


def test_example_260():
    # Spec section: List items
    assert render_html('>>- one\n>>\n  >  > two\n') == '<blockquote>\n<blockquote>\n<ul>\n<li>one</li>\n</ul>\n<p>two</p>\n</blockquote>\n</blockquote>\n'


def test_example_270():
    # Spec section: List items
    assert render_html('- foo\n\n      bar\n') == '<ul>\n<li>\n<p>foo</p>\n<pre><code>bar\n</code></pre>\n</li>\n</ul>\n'


def test_example_280():
    # Spec section: List items
    assert render_html('-\n\n  foo\n') == '<ul>\n<li></li>\n</ul>\n<p>foo</p>\n'


def test_example_290():
    # Spec section: List items
    assert render_html('  1.  A paragraph\nwith two lines.\n\n          indented code\n\n      > A block quote.\n') == '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>\n'


def test_example_300():
    # Spec section: List items
    assert render_html('- # Foo\n- Bar\n  ---\n  baz\n') == '<ul>\n<li>\n<h1>Foo</h1>\n</li>\n<li>\n<h2>Bar</h2>\nbaz</li>\n</ul>\n'


def test_example_310():
    # Spec section: Lists
    assert render_html('- a\n - b\n  - c\n   - d\n  - e\n - f\n- g\n') == '<ul>\n<li>a</li>\n<li>b</li>\n<li>c</li>\n<li>d</li>\n<li>e</li>\n<li>f</li>\n<li>g</li>\n</ul>\n'


def test_example_320():
    # Spec section: Lists
    assert render_html('* a\n  > b\n  >\n* c\n') == '<ul>\n<li>a\n<blockquote>\n<p>b</p>\n</blockquote>\n</li>\n<li>c</li>\n</ul>\n'


def test_example_330():
    # Spec section: Code spans
    assert render_html('` `` `\n') == '<p><code>``</code></p>\n'


def test_example_340():
    # Spec section: Code spans
    assert render_html('` foo `` bar `\n') == '<p><code>foo `` bar</code></p>\n'


def test_example_350():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo bar*\n') == '<p><em>foo bar</em></p>\n'


def test_example_360():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo_bar_\n') == '<p>foo_bar_</p>\n'


def test_example_370():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo*bar\n') == '<p><em>foo</em>bar</p>\n'


def test_example_380():
    # Spec section: Emphasis and strong emphasis
    assert render_html('a**"foo"**\n') == '<p>a**&quot;foo&quot;**</p>\n'


def test_example_390():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo-__(bar)__\n') == '<p>foo-<strong>(bar)</strong></p>\n'


def test_example_400():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo__bar\n') == '<p>__foo__bar</p>\n'


def test_example_410():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo **bar** baz*\n') == '<p><em>foo <strong>bar</strong> baz</em></p>\n'


def test_example_420():
    # Spec section: Emphasis and strong emphasis
    assert render_html('** is not an empty emphasis\n') == '<p>** is not an empty emphasis</p>\n'


def test_example_430():
    # Spec section: Emphasis and strong emphasis
    assert render_html('***foo* bar**\n') == '<p><strong><em>foo</em> bar</strong></p>\n'


def test_example_440():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo **\\***\n') == '<p>foo <strong>*</strong></p>\n'


def test_example_450():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo _*_\n') == '<p>foo <em>*</em></p>\n'


def test_example_460():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo**\n') == '<p><strong>foo</strong></p>\n'


def test_example_470():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo __bar *baz bim__ bam*\n') == '<p><em>foo <strong>bar *baz bim</strong> bam</em></p>\n'


def test_example_480():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**a<https://foo.bar/?q=**>\n') == '<p>**a<a href="https://foo.bar/?q=**">https://foo.bar/?q=**</a></p>\n'


def test_example_490():
    # Spec section: Links
    assert render_html('[link](foo\nbar)\n') == '<p>[link](foo\nbar)</p>\n'


def test_example_500():
    # Spec section: Links
    assert render_html('[link](foo\\)\\:)\n') == '<p><a href="foo):">link</a></p>\n'


def test_example_510():
    # Spec section: Links
    assert render_html('[link](   /uri\n  "title"  )\n') == '<p><a href="/uri" title="title">link</a></p>\n'


def test_example_520():
    # Spec section: Links
    assert render_html('![[[foo](uri1)](uri2)](uri3)\n') == '<p><img src="uri3" alt="[foo](uri2)" /></p>\n'


def test_example_530():
    # Spec section: Links
    assert render_html('[link *foo **bar** `#`*][ref]\n\n[ref]: /uri\n') == '<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>\n'


def test_example_540():
    # Spec section: Links
    assert render_html('[ẞ]\n\n[SS]: /url\n') == '<p><a href="/url">ẞ</a></p>\n'


def test_example_550():
    # Spec section: Links
    assert render_html('[bar\\\\]: /uri\n\n[bar\\\\]\n') == '<p><a href="/uri">bar\\</a></p>\n'


def test_example_560():
    # Spec section: Links
    assert render_html('[[bar [foo]\n\n[foo]: /url\n') == '<p>[[bar <a href="/url">foo</a></p>\n'


def test_example_570():
    # Spec section: Links
    assert render_html('[foo][bar][baz]\n\n[baz]: /url1\n[bar]: /url2\n') == '<p><a href="/url2">foo</a><a href="/url1">baz</a></p>\n'


def test_example_580():
    # Spec section: Images
    assert render_html('![foo](<url>)\n') == '<p><img src="url" alt="foo" /></p>\n'


def test_example_590():
    # Spec section: Images
    assert render_html('![[foo]]\n\n[[foo]]: /url "title"\n') == '<p>![[foo]]</p>\n<p>[[foo]]: /url &quot;title&quot;</p>\n'


def test_example_600():
    # Spec section: Autolinks
    assert render_html('<https://../>\n') == '<p><a href="https://../">https://../</a></p>\n'


def test_example_610():
    # Spec section: Autolinks
    assert render_html('<foo.bar.baz>\n') == '<p>&lt;foo.bar.baz&gt;</p>\n'


def test_example_620():
    # Spec section: Raw HTML
    assert render_html('<a href="hi\'> <a href=hi\'>\n') == "<p>&lt;a href=&quot;hi'&gt; &lt;a href=hi'&gt;</p>\n"


def test_example_630():
    # Spec section: Raw HTML
    assert render_html('foo <a href="&ouml;">\n') == '<p>foo <a href="&ouml;"></p>\n'


def test_example_640():
    # Spec section: Hard line breaks
    assert render_html('`code  \nspan`\n') == '<p><code>code   span</code></p>\n'


def test_example_650():
    # Spec section: Textual content
    assert render_html("hello $.;'there\n") == "<p>hello $.;'there</p>\n"
