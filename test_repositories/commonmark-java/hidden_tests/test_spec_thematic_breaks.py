from src.commonmark import render_html


def test_example_043():
    # Spec section: Thematic breaks
    assert render_html('***\n---\n___\n') == '<hr />\n<hr />\n<hr />\n'


def test_example_044():
    # Spec section: Thematic breaks
    assert render_html('+++\n') == '<p>+++</p>\n'


def test_example_045():
    # Spec section: Thematic breaks
    assert render_html('===\n') == '<p>===</p>\n'


def test_example_046():
    # Spec section: Thematic breaks
    assert render_html('--\n**\n__\n') == '<p>--\n**\n__</p>\n'


def test_example_047():
    # Spec section: Thematic breaks
    assert render_html(' ***\n  ***\n   ***\n') == '<hr />\n<hr />\n<hr />\n'


def test_example_048():
    # Spec section: Thematic breaks
    assert render_html('    ***\n') == '<pre><code>***\n</code></pre>\n'


def test_example_049():
    # Spec section: Thematic breaks
    assert render_html('Foo\n    ***\n') == '<p>Foo\n***</p>\n'


def test_example_051():
    # Spec section: Thematic breaks
    assert render_html(' - - -\n') == '<hr />\n'


def test_example_052():
    # Spec section: Thematic breaks
    assert render_html(' **  * ** * ** * **\n') == '<hr />\n'


def test_example_053():
    # Spec section: Thematic breaks
    assert render_html('-     -      -      -\n') == '<hr />\n'


def test_example_054():
    # Spec section: Thematic breaks
    assert render_html('- - - -    \n') == '<hr />\n'


def test_example_055():
    # Spec section: Thematic breaks
    assert render_html('_ _ _ _ a\n\na------\n\n---a---\n') == '<p>_ _ _ _ a</p>\n<p>a------</p>\n<p>---a---</p>\n'


def test_example_056():
    # Spec section: Thematic breaks
    assert render_html(' *-*\n') == '<p><em>-</em></p>\n'


def test_example_057():
    # Spec section: Thematic breaks
    assert render_html('- foo\n***\n- bar\n') == '<ul>\n<li>foo</li>\n</ul>\n<hr />\n<ul>\n<li>bar</li>\n</ul>\n'


def test_example_058():
    # Spec section: Thematic breaks
    assert render_html('Foo\n***\nbar\n') == '<p>Foo</p>\n<hr />\n<p>bar</p>\n'


def test_example_059():
    # Spec section: Thematic breaks
    assert render_html('Foo\n---\nbar\n') == '<h2>Foo</h2>\n<p>bar</p>\n'


def test_example_061():
    # Spec section: Thematic breaks
    assert render_html('- Foo\n- * * *\n') == '<ul>\n<li>Foo</li>\n<li>\n<hr />\n</li>\n</ul>\n'
