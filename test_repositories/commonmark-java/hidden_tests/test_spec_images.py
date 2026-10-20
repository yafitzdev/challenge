from src.commonmark import render_html


def test_example_572():
    # Spec section: Images
    assert render_html('![foo](/url "title")\n') == '<p><img src="/url" alt="foo" title="title" /></p>\n'


def test_example_573():
    # Spec section: Images
    assert render_html('![foo *bar*]\n\n[foo *bar*]: train.jpg "train & tracks"\n') == '<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>\n'


def test_example_574():
    # Spec section: Images
    assert render_html('![foo ![bar](/url)](/url2)\n') == '<p><img src="/url2" alt="foo bar" /></p>\n'


def test_example_575():
    # Spec section: Images
    assert render_html('![foo [bar](/url)](/url2)\n') == '<p><img src="/url2" alt="foo bar" /></p>\n'


def test_example_576():
    # Spec section: Images
    assert render_html('![foo *bar*][]\n\n[foo *bar*]: train.jpg "train & tracks"\n') == '<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>\n'


def test_example_577():
    # Spec section: Images
    assert render_html('![foo *bar*][foobar]\n\n[FOOBAR]: train.jpg "train & tracks"\n') == '<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>\n'


def test_example_578():
    # Spec section: Images
    assert render_html('![foo](train.jpg)\n') == '<p><img src="train.jpg" alt="foo" /></p>\n'


def test_example_579():
    # Spec section: Images
    assert render_html('My ![foo bar](/path/to/train.jpg  "title"   )\n') == '<p>My <img src="/path/to/train.jpg" alt="foo bar" title="title" /></p>\n'


def test_example_581():
    # Spec section: Images
    assert render_html('![](/url)\n') == '<p><img src="/url" alt="" /></p>\n'


def test_example_582():
    # Spec section: Images
    assert render_html('![foo][bar]\n\n[bar]: /url\n') == '<p><img src="/url" alt="foo" /></p>\n'


def test_example_583():
    # Spec section: Images
    assert render_html('![foo][bar]\n\n[BAR]: /url\n') == '<p><img src="/url" alt="foo" /></p>\n'


def test_example_584():
    # Spec section: Images
    assert render_html('![foo][]\n\n[foo]: /url "title"\n') == '<p><img src="/url" alt="foo" title="title" /></p>\n'


def test_example_585():
    # Spec section: Images
    assert render_html('![*foo* bar][]\n\n[*foo* bar]: /url "title"\n') == '<p><img src="/url" alt="foo bar" title="title" /></p>\n'


def test_example_586():
    # Spec section: Images
    assert render_html('![Foo][]\n\n[foo]: /url "title"\n') == '<p><img src="/url" alt="Foo" title="title" /></p>\n'


def test_example_587():
    # Spec section: Images
    assert render_html('![foo] \n[]\n\n[foo]: /url "title"\n') == '<p><img src="/url" alt="foo" title="title" />\n[]</p>\n'


def test_example_588():
    # Spec section: Images
    assert render_html('![foo]\n\n[foo]: /url "title"\n') == '<p><img src="/url" alt="foo" title="title" /></p>\n'


def test_example_589():
    # Spec section: Images
    assert render_html('![*foo* bar]\n\n[*foo* bar]: /url "title"\n') == '<p><img src="/url" alt="foo bar" title="title" /></p>\n'


def test_example_591():
    # Spec section: Images
    assert render_html('![Foo]\n\n[foo]: /url "title"\n') == '<p><img src="/url" alt="Foo" title="title" /></p>\n'


def test_example_592():
    # Spec section: Images
    assert render_html('!\\[foo]\n\n[foo]: /url "title"\n') == '<p>![foo]</p>\n'


def test_example_593():
    # Spec section: Images
    assert render_html('\\![foo]\n\n[foo]: /url "title"\n') == '<p>!<a href="/url" title="title">foo</a></p>\n'
