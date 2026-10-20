from src.commonmark import render_html


def test_example_012():
    # Spec section: Backslash escapes
    assert render_html('\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^\\_\\`\\{\\|\\}\\~\n') == "<p>!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~</p>\n"


def test_example_013():
    # Spec section: Backslash escapes
    assert render_html('\\\t\\A\\a\\ \\3\\φ\\«\n') == '<p>\\\t\\A\\a\\ \\3\\φ\\«</p>\n'


def test_example_014():
    # Spec section: Backslash escapes
    assert render_html('\\*not emphasized*\n\\<br/> not a tag\n\\[not a link](/foo)\n\\`not code`\n1\\. not a list\n\\* not a list\n\\# not a heading\n\\[foo]: /url "not a reference"\n\\&ouml; not a character entity\n') == '<p>*not emphasized*\n&lt;br/&gt; not a tag\n[not a link](/foo)\n`not code`\n1. not a list\n* not a list\n# not a heading\n[foo]: /url &quot;not a reference&quot;\n&amp;ouml; not a character entity</p>\n'


def test_example_015():
    # Spec section: Backslash escapes
    assert render_html('\\\\*emphasis*\n') == '<p>\\<em>emphasis</em></p>\n'


def test_example_016():
    # Spec section: Backslash escapes
    assert render_html('foo\\\nbar\n') == '<p>foo<br />\nbar</p>\n'


def test_example_017():
    # Spec section: Backslash escapes
    assert render_html('`` \\[\\` ``\n') == '<p><code>\\[\\`</code></p>\n'


def test_example_018():
    # Spec section: Backslash escapes
    assert render_html('    \\[\\]\n') == '<pre><code>\\[\\]\n</code></pre>\n'


def test_example_019():
    # Spec section: Backslash escapes
    assert render_html('~~~\n\\[\\]\n~~~\n') == '<pre><code>\\[\\]\n</code></pre>\n'


def test_example_021():
    # Spec section: Backslash escapes
    assert render_html('<a href="/bar\\/)">\n') == '<a href="/bar\\/)">\n'


def test_example_022():
    # Spec section: Backslash escapes
    assert render_html('[foo](/bar\\* "ti\\*tle")\n') == '<p><a href="/bar*" title="ti*tle">foo</a></p>\n'


def test_example_023():
    # Spec section: Backslash escapes
    assert render_html('[foo]\n\n[foo]: /bar\\* "ti\\*tle"\n') == '<p><a href="/bar*" title="ti*tle">foo</a></p>\n'


def test_example_024():
    # Spec section: Backslash escapes
    assert render_html('``` foo\\+bar\nfoo\n```\n') == '<pre><code class="language-foo+bar">foo\n</code></pre>\n'
