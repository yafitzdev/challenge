from src.commonmark import render_html


def test_example_613():
    # Spec section: Raw HTML
    assert render_html('<a><bab><c2c>\n') == '<p><a><bab><c2c></p>\n'


def test_example_614():
    # Spec section: Raw HTML
    assert render_html('<a/><b2/>\n') == '<p><a/><b2/></p>\n'


def test_example_615():
    # Spec section: Raw HTML
    assert render_html('<a  /><b2\ndata="foo" >\n') == '<p><a  /><b2\ndata="foo" ></p>\n'


def test_example_616():
    # Spec section: Raw HTML
    assert render_html('<a foo="bar" bam = \'baz <em>"</em>\'\n_boolean zoop:33=zoop:33 />\n') == '<p><a foo="bar" bam = \'baz <em>"</em>\'\n_boolean zoop:33=zoop:33 /></p>\n'


def test_example_617():
    # Spec section: Raw HTML
    assert render_html('Foo <responsive-image src="foo.jpg" />\n') == '<p>Foo <responsive-image src="foo.jpg" /></p>\n'


def test_example_618():
    # Spec section: Raw HTML
    assert render_html('<33> <__>\n') == '<p>&lt;33&gt; &lt;__&gt;</p>\n'


def test_example_619():
    # Spec section: Raw HTML
    assert render_html('<a h*#ref="hi">\n') == '<p>&lt;a h*#ref=&quot;hi&quot;&gt;</p>\n'


def test_example_621():
    # Spec section: Raw HTML
    assert render_html('< a><\nfoo><bar/ >\n<foo bar=baz\nbim!bop />\n') == '<p>&lt; a&gt;&lt;\nfoo&gt;&lt;bar/ &gt;\n&lt;foo bar=baz\nbim!bop /&gt;</p>\n'


def test_example_622():
    # Spec section: Raw HTML
    assert render_html("<a href='bar'title=title>\n") == "<p>&lt;a href='bar'title=title&gt;</p>\n"


def test_example_623():
    # Spec section: Raw HTML
    assert render_html('</a></foo >\n') == '<p></a></foo ></p>\n'


def test_example_624():
    # Spec section: Raw HTML
    assert render_html('</a href="foo">\n') == '<p>&lt;/a href=&quot;foo&quot;&gt;</p>\n'


def test_example_625():
    # Spec section: Raw HTML
    assert render_html('foo <!-- this is a --\ncomment - with hyphens -->\n') == '<p>foo <!-- this is a --\ncomment - with hyphens --></p>\n'


def test_example_626():
    # Spec section: Raw HTML
    assert render_html('foo <!--> foo -->\n\nfoo <!---> foo -->\n') == '<p>foo <!--> foo --&gt;</p>\n<p>foo <!---> foo --&gt;</p>\n'


def test_example_627():
    # Spec section: Raw HTML
    assert render_html('foo <?php echo $a; ?>\n') == '<p>foo <?php echo $a; ?></p>\n'


def test_example_628():
    # Spec section: Raw HTML
    assert render_html('foo <!ELEMENT br EMPTY>\n') == '<p>foo <!ELEMENT br EMPTY></p>\n'


def test_example_629():
    # Spec section: Raw HTML
    assert render_html('foo <![CDATA[>&<]]>\n') == '<p>foo <![CDATA[>&<]]></p>\n'


def test_example_631():
    # Spec section: Raw HTML
    assert render_html('foo <a href="\\*">\n') == '<p>foo <a href="\\*"></p>\n'


def test_example_632():
    # Spec section: Raw HTML
    assert render_html('<a href="\\"">\n') == '<p>&lt;a href=&quot;&quot;&quot;&gt;</p>\n'
