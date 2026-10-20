from src.commonmark import render_html


def test_example_025():
    # Spec section: Entity and numeric character references
    assert render_html('&nbsp; &amp; &copy; &AElig; &Dcaron;\n&frac34; &HilbertSpace; &DifferentialD;\n&ClockwiseContourIntegral; &ngE;\n') == '<p>\xa0 &amp; © Æ Ď\n¾ ℋ ⅆ\n∲ ≧̸</p>\n'


def test_example_026():
    # Spec section: Entity and numeric character references
    assert render_html('&#35; &#1234; &#992; &#0;\n') == '<p># Ӓ Ϡ �</p>\n'


def test_example_027():
    # Spec section: Entity and numeric character references
    assert render_html('&#X22; &#XD06; &#xcab;\n') == '<p>&quot; ആ ಫ</p>\n'


def test_example_028():
    # Spec section: Entity and numeric character references
    assert render_html('&nbsp &x; &#; &#x;\n&#87654321;\n&#abcdef0;\n&ThisIsNotDefined; &hi?;\n') == '<p>&amp;nbsp &amp;x; &amp;#; &amp;#x;\n&amp;#87654321;\n&amp;#abcdef0;\n&amp;ThisIsNotDefined; &amp;hi?;</p>\n'


def test_example_029():
    # Spec section: Entity and numeric character references
    assert render_html('&copy\n') == '<p>&amp;copy</p>\n'


def test_example_031():
    # Spec section: Entity and numeric character references
    assert render_html('<a href="&ouml;&ouml;.html">\n') == '<a href="&ouml;&ouml;.html">\n'


def test_example_032():
    # Spec section: Entity and numeric character references
    assert render_html('[foo](/f&ouml;&ouml; "f&ouml;&ouml;")\n') == '<p><a href="/f%C3%B6%C3%B6" title="föö">foo</a></p>\n'


def test_example_033():
    # Spec section: Entity and numeric character references
    assert render_html('[foo]\n\n[foo]: /f&ouml;&ouml; "f&ouml;&ouml;"\n') == '<p><a href="/f%C3%B6%C3%B6" title="föö">foo</a></p>\n'


def test_example_034():
    # Spec section: Entity and numeric character references
    assert render_html('``` f&ouml;&ouml;\nfoo\n```\n') == '<pre><code class="language-föö">foo\n</code></pre>\n'


def test_example_035():
    # Spec section: Entity and numeric character references
    assert render_html('`f&ouml;&ouml;`\n') == '<p><code>f&amp;ouml;&amp;ouml;</code></p>\n'


def test_example_036():
    # Spec section: Entity and numeric character references
    assert render_html('    f&ouml;f&ouml;\n') == '<pre><code>f&amp;ouml;f&amp;ouml;\n</code></pre>\n'


def test_example_037():
    # Spec section: Entity and numeric character references
    assert render_html('&#42;foo&#42;\n*foo*\n') == '<p>*foo*\n<em>foo</em></p>\n'


def test_example_038():
    # Spec section: Entity and numeric character references
    assert render_html('&#42; foo\n\n* foo\n') == '<p>* foo</p>\n<ul>\n<li>foo</li>\n</ul>\n'


def test_example_039():
    # Spec section: Entity and numeric character references
    assert render_html('foo&#10;&#10;bar\n') == '<p>foo\n\nbar</p>\n'


def test_example_041():
    # Spec section: Entity and numeric character references
    assert render_html('[a](url &quot;tit&quot;)\n') == '<p>[a](url &quot;tit&quot;)</p>\n'
