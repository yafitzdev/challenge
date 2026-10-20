from src.commonmark import render_html


def test_example_192():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /url "title"\n\n[foo]\n') == '<p><a href="/url" title="title">foo</a></p>\n'


def test_example_193():
    # Spec section: Link reference definitions
    assert render_html("   [foo]: \n      /url  \n           'the title'  \n\n[foo]\n") == '<p><a href="/url" title="the title">foo</a></p>\n'


def test_example_194():
    # Spec section: Link reference definitions
    assert render_html("[Foo*bar\\]]:my_(url) 'title (with parens)'\n\n[Foo*bar\\]]\n") == '<p><a href="my_(url)" title="title (with parens)">Foo*bar]</a></p>\n'


def test_example_195():
    # Spec section: Link reference definitions
    assert render_html("[Foo bar]:\n<my url>\n'title'\n\n[Foo bar]\n") == '<p><a href="my%20url" title="title">Foo bar</a></p>\n'


def test_example_196():
    # Spec section: Link reference definitions
    assert render_html("[foo]: /url '\ntitle\nline1\nline2\n'\n\n[foo]\n") == '<p><a href="/url" title="\ntitle\nline1\nline2\n">foo</a></p>\n'


def test_example_197():
    # Spec section: Link reference definitions
    assert render_html("[foo]: /url 'title\n\nwith blank line'\n\n[foo]\n") == "<p>[foo]: /url 'title</p>\n<p>with blank line'</p>\n<p>[foo]</p>\n"


def test_example_198():
    # Spec section: Link reference definitions
    assert render_html('[foo]:\n/url\n\n[foo]\n') == '<p><a href="/url">foo</a></p>\n'


def test_example_199():
    # Spec section: Link reference definitions
    assert render_html('[foo]:\n\n[foo]\n') == '<p>[foo]:</p>\n<p>[foo]</p>\n'


def test_example_201():
    # Spec section: Link reference definitions
    assert render_html('[foo]: <bar>(baz)\n\n[foo]\n') == '<p>[foo]: <bar>(baz)</p>\n<p>[foo]</p>\n'


def test_example_202():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /url\\bar\\*baz "foo\\"bar\\baz"\n\n[foo]\n') == '<p><a href="/url%5Cbar*baz" title="foo&quot;bar\\baz">foo</a></p>\n'


def test_example_203():
    # Spec section: Link reference definitions
    assert render_html('[foo]\n\n[foo]: url\n') == '<p><a href="url">foo</a></p>\n'


def test_example_204():
    # Spec section: Link reference definitions
    assert render_html('[foo]\n\n[foo]: first\n[foo]: second\n') == '<p><a href="first">foo</a></p>\n'


def test_example_205():
    # Spec section: Link reference definitions
    assert render_html('[FOO]: /url\n\n[Foo]\n') == '<p><a href="/url">Foo</a></p>\n'


def test_example_206():
    # Spec section: Link reference definitions
    assert render_html('[ΑΓΩ]: /φου\n\n[αγω]\n') == '<p><a href="/%CF%86%CE%BF%CF%85">αγω</a></p>\n'


def test_example_207():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /url\n') == ''


def test_example_208():
    # Spec section: Link reference definitions
    assert render_html('[\nfoo\n]: /url\nbar\n') == '<p>bar</p>\n'


def test_example_209():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /url "title" ok\n') == '<p>[foo]: /url &quot;title&quot; ok</p>\n'


def test_example_211():
    # Spec section: Link reference definitions
    assert render_html('    [foo]: /url "title"\n\n[foo]\n') == '<pre><code>[foo]: /url &quot;title&quot;\n</code></pre>\n<p>[foo]</p>\n'


def test_example_212():
    # Spec section: Link reference definitions
    assert render_html('```\n[foo]: /url\n```\n\n[foo]\n') == '<pre><code>[foo]: /url\n</code></pre>\n<p>[foo]</p>\n'


def test_example_213():
    # Spec section: Link reference definitions
    assert render_html('Foo\n[bar]: /baz\n\n[bar]\n') == '<p>Foo\n[bar]: /baz</p>\n<p>[bar]</p>\n'


def test_example_214():
    # Spec section: Link reference definitions
    assert render_html('# [Foo]\n[foo]: /url\n> bar\n') == '<h1><a href="/url">Foo</a></h1>\n<blockquote>\n<p>bar</p>\n</blockquote>\n'


def test_example_215():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /url\nbar\n===\n[foo]\n') == '<h1>bar</h1>\n<p><a href="/url">foo</a></p>\n'


def test_example_216():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /url\n===\n[foo]\n') == '<p>===\n<a href="/url">foo</a></p>\n'


def test_example_217():
    # Spec section: Link reference definitions
    assert render_html('[foo]: /foo-url "foo"\n[bar]: /bar-url\n  "bar"\n[baz]: /baz-url\n\n[foo],\n[bar],\n[baz]\n') == '<p><a href="/foo-url" title="foo">foo</a>,\n<a href="/bar-url" title="bar">bar</a>,\n<a href="/baz-url">baz</a></p>\n'


def test_example_218():
    # Spec section: Link reference definitions
    assert render_html('[foo]\n\n> [foo]: /url\n') == '<p><a href="/url">foo</a></p>\n<blockquote>\n</blockquote>\n'
