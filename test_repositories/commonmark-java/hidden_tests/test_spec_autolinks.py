from src.commonmark import render_html


def test_example_594():
    # Spec section: Autolinks
    assert render_html('<http://foo.bar.baz>\n') == '<p><a href="http://foo.bar.baz">http://foo.bar.baz</a></p>\n'


def test_example_595():
    # Spec section: Autolinks
    assert render_html('<https://foo.bar.baz/test?q=hello&id=22&boolean>\n') == '<p><a href="https://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean">https://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean</a></p>\n'


def test_example_596():
    # Spec section: Autolinks
    assert render_html('<irc://foo.bar:2233/baz>\n') == '<p><a href="irc://foo.bar:2233/baz">irc://foo.bar:2233/baz</a></p>\n'


def test_example_597():
    # Spec section: Autolinks
    assert render_html('<MAILTO:FOO@BAR.BAZ>\n') == '<p><a href="MAILTO:FOO@BAR.BAZ">MAILTO:FOO@BAR.BAZ</a></p>\n'


def test_example_598():
    # Spec section: Autolinks
    assert render_html('<a+b+c:d>\n') == '<p><a href="a+b+c:d">a+b+c:d</a></p>\n'


def test_example_599():
    # Spec section: Autolinks
    assert render_html('<made-up-scheme://foo,bar>\n') == '<p><a href="made-up-scheme://foo,bar">made-up-scheme://foo,bar</a></p>\n'


def test_example_601():
    # Spec section: Autolinks
    assert render_html('<localhost:5001/foo>\n') == '<p><a href="localhost:5001/foo">localhost:5001/foo</a></p>\n'


def test_example_602():
    # Spec section: Autolinks
    assert render_html('<https://foo.bar/baz bim>\n') == '<p>&lt;https://foo.bar/baz bim&gt;</p>\n'


def test_example_603():
    # Spec section: Autolinks
    assert render_html('<https://example.com/\\[\\>\n') == '<p><a href="https://example.com/%5C%5B%5C">https://example.com/\\[\\</a></p>\n'


def test_example_604():
    # Spec section: Autolinks
    assert render_html('<foo@bar.example.com>\n') == '<p><a href="mailto:foo@bar.example.com">foo@bar.example.com</a></p>\n'


def test_example_605():
    # Spec section: Autolinks
    assert render_html('<foo+special@Bar.baz-bar0.com>\n') == '<p><a href="mailto:foo+special@Bar.baz-bar0.com">foo+special@Bar.baz-bar0.com</a></p>\n'


def test_example_606():
    # Spec section: Autolinks
    assert render_html('<foo\\+@bar.example.com>\n') == '<p>&lt;foo+@bar.example.com&gt;</p>\n'


def test_example_607():
    # Spec section: Autolinks
    assert render_html('<>\n') == '<p>&lt;&gt;</p>\n'


def test_example_608():
    # Spec section: Autolinks
    assert render_html('< https://foo.bar >\n') == '<p>&lt; https://foo.bar &gt;</p>\n'


def test_example_609():
    # Spec section: Autolinks
    assert render_html('<m:abc>\n') == '<p>&lt;m:abc&gt;</p>\n'


def test_example_611():
    # Spec section: Autolinks
    assert render_html('https://example.com\n') == '<p>https://example.com</p>\n'


def test_example_612():
    # Spec section: Autolinks
    assert render_html('foo@bar.example.com\n') == '<p>foo@bar.example.com</p>\n'
