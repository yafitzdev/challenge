from src.commonmark import render_html


def test_example_482():
    # Spec section: Links
    assert render_html('[link](/uri "title")\n') == '<p><a href="/uri" title="title">link</a></p>\n'


def test_example_483():
    # Spec section: Links
    assert render_html('[link](/uri)\n') == '<p><a href="/uri">link</a></p>\n'


def test_example_484():
    # Spec section: Links
    assert render_html('[](./target.md)\n') == '<p><a href="./target.md"></a></p>\n'


def test_example_485():
    # Spec section: Links
    assert render_html('[link]()\n') == '<p><a href="">link</a></p>\n'


def test_example_486():
    # Spec section: Links
    assert render_html('[link](<>)\n') == '<p><a href="">link</a></p>\n'


def test_example_487():
    # Spec section: Links
    assert render_html('[]()\n') == '<p><a href=""></a></p>\n'


def test_example_488():
    # Spec section: Links
    assert render_html('[link](/my uri)\n') == '<p>[link](/my uri)</p>\n'


def test_example_489():
    # Spec section: Links
    assert render_html('[link](</my uri>)\n') == '<p><a href="/my%20uri">link</a></p>\n'


def test_example_491():
    # Spec section: Links
    assert render_html('[link](<foo\nbar>)\n') == '<p>[link](<foo\nbar>)</p>\n'


def test_example_492():
    # Spec section: Links
    assert render_html('[a](<b)c>)\n') == '<p><a href="b)c">a</a></p>\n'


def test_example_493():
    # Spec section: Links
    assert render_html('[link](<foo\\>)\n') == '<p>[link](&lt;foo&gt;)</p>\n'


def test_example_494():
    # Spec section: Links
    assert render_html('[a](<b)c\n[a](<b)c>\n[a](<b>c)\n') == '<p>[a](&lt;b)c\n[a](&lt;b)c&gt;\n[a](<b>c)</p>\n'


def test_example_495():
    # Spec section: Links
    assert render_html('[link](\\(foo\\))\n') == '<p><a href="(foo)">link</a></p>\n'


def test_example_496():
    # Spec section: Links
    assert render_html('[link](foo(and(bar)))\n') == '<p><a href="foo(and(bar))">link</a></p>\n'


def test_example_497():
    # Spec section: Links
    assert render_html('[link](foo(and(bar))\n') == '<p>[link](foo(and(bar))</p>\n'


def test_example_498():
    # Spec section: Links
    assert render_html('[link](foo\\(and\\(bar\\))\n') == '<p><a href="foo(and(bar)">link</a></p>\n'


def test_example_499():
    # Spec section: Links
    assert render_html('[link](<foo(and(bar)>)\n') == '<p><a href="foo(and(bar)">link</a></p>\n'


def test_example_501():
    # Spec section: Links
    assert render_html('[link](#fragment)\n\n[link](https://example.com#fragment)\n\n[link](https://example.com?foo=3#frag)\n') == '<p><a href="#fragment">link</a></p>\n<p><a href="https://example.com#fragment">link</a></p>\n<p><a href="https://example.com?foo=3#frag">link</a></p>\n'


def test_example_502():
    # Spec section: Links
    assert render_html('[link](foo\\bar)\n') == '<p><a href="foo%5Cbar">link</a></p>\n'


def test_example_503():
    # Spec section: Links
    assert render_html('[link](foo%20b&auml;)\n') == '<p><a href="foo%20b%C3%A4">link</a></p>\n'


def test_example_504():
    # Spec section: Links
    assert render_html('[link]("title")\n') == '<p><a href="%22title%22">link</a></p>\n'


def test_example_505():
    # Spec section: Links
    assert render_html('[link](/url "title")\n[link](/url \'title\')\n[link](/url (title))\n') == '<p><a href="/url" title="title">link</a>\n<a href="/url" title="title">link</a>\n<a href="/url" title="title">link</a></p>\n'


def test_example_506():
    # Spec section: Links
    assert render_html('[link](/url "title \\"&quot;")\n') == '<p><a href="/url" title="title &quot;&quot;">link</a></p>\n'


def test_example_507():
    # Spec section: Links
    assert render_html('[link](/url\xa0"title")\n') == '<p><a href="/url%C2%A0%22title%22">link</a></p>\n'


def test_example_508():
    # Spec section: Links
    assert render_html('[link](/url "title "and" title")\n') == '<p>[link](/url &quot;title &quot;and&quot; title&quot;)</p>\n'


def test_example_509():
    # Spec section: Links
    assert render_html('[link](/url \'title "and" title\')\n') == '<p><a href="/url" title="title &quot;and&quot; title">link</a></p>\n'


def test_example_511():
    # Spec section: Links
    assert render_html('[link] (/uri)\n') == '<p>[link] (/uri)</p>\n'


def test_example_512():
    # Spec section: Links
    assert render_html('[link [foo [bar]]](/uri)\n') == '<p><a href="/uri">link [foo [bar]]</a></p>\n'


def test_example_513():
    # Spec section: Links
    assert render_html('[link] bar](/uri)\n') == '<p>[link] bar](/uri)</p>\n'


def test_example_514():
    # Spec section: Links
    assert render_html('[link [bar](/uri)\n') == '<p>[link <a href="/uri">bar</a></p>\n'


def test_example_515():
    # Spec section: Links
    assert render_html('[link \\[bar](/uri)\n') == '<p><a href="/uri">link [bar</a></p>\n'


def test_example_516():
    # Spec section: Links
    assert render_html('[link *foo **bar** `#`*](/uri)\n') == '<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>\n'


def test_example_517():
    # Spec section: Links
    assert render_html('[![moon](moon.jpg)](/uri)\n') == '<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>\n'


def test_example_518():
    # Spec section: Links
    assert render_html('[foo [bar](/uri)](/uri)\n') == '<p>[foo <a href="/uri">bar</a>](/uri)</p>\n'


def test_example_519():
    # Spec section: Links
    assert render_html('[foo *[bar [baz](/uri)](/uri)*](/uri)\n') == '<p>[foo <em>[bar <a href="/uri">baz</a>](/uri)</em>](/uri)</p>\n'


def test_example_521():
    # Spec section: Links
    assert render_html('*[foo*](/uri)\n') == '<p>*<a href="/uri">foo*</a></p>\n'


def test_example_522():
    # Spec section: Links
    assert render_html('[foo *bar](baz*)\n') == '<p><a href="baz*">foo *bar</a></p>\n'


def test_example_523():
    # Spec section: Links
    assert render_html('*foo [bar* baz]\n') == '<p><em>foo [bar</em> baz]</p>\n'


def test_example_524():
    # Spec section: Links
    assert render_html('[foo <bar attr="](baz)">\n') == '<p>[foo <bar attr="](baz)"></p>\n'


def test_example_525():
    # Spec section: Links
    assert render_html('[foo`](/uri)`\n') == '<p>[foo<code>](/uri)</code></p>\n'


def test_example_526():
    # Spec section: Links
    assert render_html('[foo<https://example.com/?search=](uri)>\n') == '<p>[foo<a href="https://example.com/?search=%5D(uri)">https://example.com/?search=](uri)</a></p>\n'


def test_example_527():
    # Spec section: Links
    assert render_html('[foo][bar]\n\n[bar]: /url "title"\n') == '<p><a href="/url" title="title">foo</a></p>\n'


def test_example_528():
    # Spec section: Links
    assert render_html('[link [foo [bar]]][ref]\n\n[ref]: /uri\n') == '<p><a href="/uri">link [foo [bar]]</a></p>\n'


def test_example_529():
    # Spec section: Links
    assert render_html('[link \\[bar][ref]\n\n[ref]: /uri\n') == '<p><a href="/uri">link [bar</a></p>\n'


def test_example_531():
    # Spec section: Links
    assert render_html('[![moon](moon.jpg)][ref]\n\n[ref]: /uri\n') == '<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>\n'


def test_example_532():
    # Spec section: Links
    assert render_html('[foo [bar](/uri)][ref]\n\n[ref]: /uri\n') == '<p>[foo <a href="/uri">bar</a>]<a href="/uri">ref</a></p>\n'


def test_example_533():
    # Spec section: Links
    assert render_html('[foo *bar [baz][ref]*][ref]\n\n[ref]: /uri\n') == '<p>[foo <em>bar <a href="/uri">baz</a></em>]<a href="/uri">ref</a></p>\n'


def test_example_534():
    # Spec section: Links
    assert render_html('*[foo*][ref]\n\n[ref]: /uri\n') == '<p>*<a href="/uri">foo*</a></p>\n'


def test_example_535():
    # Spec section: Links
    assert render_html('[foo *bar][ref]*\n\n[ref]: /uri\n') == '<p><a href="/uri">foo *bar</a>*</p>\n'


def test_example_536():
    # Spec section: Links
    assert render_html('[foo <bar attr="][ref]">\n\n[ref]: /uri\n') == '<p>[foo <bar attr="][ref]"></p>\n'


def test_example_537():
    # Spec section: Links
    assert render_html('[foo`][ref]`\n\n[ref]: /uri\n') == '<p>[foo<code>][ref]</code></p>\n'


def test_example_538():
    # Spec section: Links
    assert render_html('[foo<https://example.com/?search=][ref]>\n\n[ref]: /uri\n') == '<p>[foo<a href="https://example.com/?search=%5D%5Bref%5D">https://example.com/?search=][ref]</a></p>\n'


def test_example_539():
    # Spec section: Links
    assert render_html('[foo][BaR]\n\n[bar]: /url "title"\n') == '<p><a href="/url" title="title">foo</a></p>\n'


def test_example_541():
    # Spec section: Links
    assert render_html('[Foo\n  bar]: /url\n\n[Baz][Foo bar]\n') == '<p><a href="/url">Baz</a></p>\n'


def test_example_542():
    # Spec section: Links
    assert render_html('[foo] [bar]\n\n[bar]: /url "title"\n') == '<p>[foo] <a href="/url" title="title">bar</a></p>\n'


def test_example_543():
    # Spec section: Links
    assert render_html('[foo]\n[bar]\n\n[bar]: /url "title"\n') == '<p>[foo]\n<a href="/url" title="title">bar</a></p>\n'


def test_example_544():
    # Spec section: Links
    assert render_html('[foo]: /url1\n\n[foo]: /url2\n\n[bar][foo]\n') == '<p><a href="/url1">bar</a></p>\n'


def test_example_545():
    # Spec section: Links
    assert render_html('[bar][foo\\!]\n\n[foo!]: /url\n') == '<p>[bar][foo!]</p>\n'


def test_example_546():
    # Spec section: Links
    assert render_html('[foo][ref[]\n\n[ref[]: /uri\n') == '<p>[foo][ref[]</p>\n<p>[ref[]: /uri</p>\n'


def test_example_547():
    # Spec section: Links
    assert render_html('[foo][ref[bar]]\n\n[ref[bar]]: /uri\n') == '<p>[foo][ref[bar]]</p>\n<p>[ref[bar]]: /uri</p>\n'


def test_example_548():
    # Spec section: Links
    assert render_html('[[[foo]]]\n\n[[[foo]]]: /url\n') == '<p>[[[foo]]]</p>\n<p>[[[foo]]]: /url</p>\n'


def test_example_549():
    # Spec section: Links
    assert render_html('[foo][ref\\[]\n\n[ref\\[]: /uri\n') == '<p><a href="/uri">foo</a></p>\n'


def test_example_551():
    # Spec section: Links
    assert render_html('[]\n\n[]: /uri\n') == '<p>[]</p>\n<p>[]: /uri</p>\n'


def test_example_552():
    # Spec section: Links
    assert render_html('[\n ]\n\n[\n ]: /uri\n') == '<p>[\n]</p>\n<p>[\n]: /uri</p>\n'


def test_example_553():
    # Spec section: Links
    assert render_html('[foo][]\n\n[foo]: /url "title"\n') == '<p><a href="/url" title="title">foo</a></p>\n'


def test_example_554():
    # Spec section: Links
    assert render_html('[*foo* bar][]\n\n[*foo* bar]: /url "title"\n') == '<p><a href="/url" title="title"><em>foo</em> bar</a></p>\n'


def test_example_555():
    # Spec section: Links
    assert render_html('[Foo][]\n\n[foo]: /url "title"\n') == '<p><a href="/url" title="title">Foo</a></p>\n'


def test_example_556():
    # Spec section: Links
    assert render_html('[foo] \n[]\n\n[foo]: /url "title"\n') == '<p><a href="/url" title="title">foo</a>\n[]</p>\n'


def test_example_557():
    # Spec section: Links
    assert render_html('[foo]\n\n[foo]: /url "title"\n') == '<p><a href="/url" title="title">foo</a></p>\n'


def test_example_558():
    # Spec section: Links
    assert render_html('[*foo* bar]\n\n[*foo* bar]: /url "title"\n') == '<p><a href="/url" title="title"><em>foo</em> bar</a></p>\n'


def test_example_559():
    # Spec section: Links
    assert render_html('[[*foo* bar]]\n\n[*foo* bar]: /url "title"\n') == '<p>[<a href="/url" title="title"><em>foo</em> bar</a>]</p>\n'


def test_example_561():
    # Spec section: Links
    assert render_html('[Foo]\n\n[foo]: /url "title"\n') == '<p><a href="/url" title="title">Foo</a></p>\n'


def test_example_562():
    # Spec section: Links
    assert render_html('[foo] bar\n\n[foo]: /url\n') == '<p><a href="/url">foo</a> bar</p>\n'


def test_example_563():
    # Spec section: Links
    assert render_html('\\[foo]\n\n[foo]: /url "title"\n') == '<p>[foo]</p>\n'


def test_example_564():
    # Spec section: Links
    assert render_html('[foo*]: /url\n\n*[foo*]\n') == '<p>*<a href="/url">foo*</a></p>\n'


def test_example_565():
    # Spec section: Links
    assert render_html('[foo][bar]\n\n[foo]: /url1\n[bar]: /url2\n') == '<p><a href="/url2">foo</a></p>\n'


def test_example_566():
    # Spec section: Links
    assert render_html('[foo][]\n\n[foo]: /url1\n') == '<p><a href="/url1">foo</a></p>\n'


def test_example_567():
    # Spec section: Links
    assert render_html('[foo]()\n\n[foo]: /url1\n') == '<p><a href="">foo</a></p>\n'


def test_example_568():
    # Spec section: Links
    assert render_html('[foo](not a link)\n\n[foo]: /url1\n') == '<p><a href="/url1">foo</a>(not a link)</p>\n'


def test_example_569():
    # Spec section: Links
    assert render_html('[foo][bar][baz]\n\n[baz]: /url\n') == '<p>[foo]<a href="/url">bar</a></p>\n'


def test_example_571():
    # Spec section: Links
    assert render_html('[foo][bar][baz]\n\n[baz]: /url1\n[foo]: /url2\n') == '<p>[foo]<a href="/url1">bar</a></p>\n'
