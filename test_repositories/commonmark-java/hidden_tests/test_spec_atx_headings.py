from src.commonmark import render_html


def test_example_062():
    # Spec section: ATX headings
    assert render_html('# foo\n## foo\n### foo\n#### foo\n##### foo\n###### foo\n') == '<h1>foo</h1>\n<h2>foo</h2>\n<h3>foo</h3>\n<h4>foo</h4>\n<h5>foo</h5>\n<h6>foo</h6>\n'


def test_example_063():
    # Spec section: ATX headings
    assert render_html('####### foo\n') == '<p>####### foo</p>\n'


def test_example_064():
    # Spec section: ATX headings
    assert render_html('#5 bolt\n\n#hashtag\n') == '<p>#5 bolt</p>\n<p>#hashtag</p>\n'


def test_example_065():
    # Spec section: ATX headings
    assert render_html('\\## foo\n') == '<p>## foo</p>\n'


def test_example_066():
    # Spec section: ATX headings
    assert render_html('# foo *bar* \\*baz\\*\n') == '<h1>foo <em>bar</em> *baz*</h1>\n'


def test_example_067():
    # Spec section: ATX headings
    assert render_html('#                  foo                     \n') == '<h1>foo</h1>\n'


def test_example_068():
    # Spec section: ATX headings
    assert render_html(' ### foo\n  ## foo\n   # foo\n') == '<h3>foo</h3>\n<h2>foo</h2>\n<h1>foo</h1>\n'


def test_example_069():
    # Spec section: ATX headings
    assert render_html('    # foo\n') == '<pre><code># foo\n</code></pre>\n'


def test_example_071():
    # Spec section: ATX headings
    assert render_html('## foo ##\n  ###   bar    ###\n') == '<h2>foo</h2>\n<h3>bar</h3>\n'


def test_example_072():
    # Spec section: ATX headings
    assert render_html('# foo ##################################\n##### foo ##\n') == '<h1>foo</h1>\n<h5>foo</h5>\n'


def test_example_073():
    # Spec section: ATX headings
    assert render_html('### foo ###     \n') == '<h3>foo</h3>\n'


def test_example_074():
    # Spec section: ATX headings
    assert render_html('### foo ### b\n') == '<h3>foo ### b</h3>\n'


def test_example_075():
    # Spec section: ATX headings
    assert render_html('# foo#\n') == '<h1>foo#</h1>\n'


def test_example_076():
    # Spec section: ATX headings
    assert render_html('### foo \\###\n## foo #\\##\n# foo \\#\n') == '<h3>foo ###</h3>\n<h2>foo ###</h2>\n<h1>foo #</h1>\n'


def test_example_077():
    # Spec section: ATX headings
    assert render_html('****\n## foo\n****\n') == '<hr />\n<h2>foo</h2>\n<hr />\n'


def test_example_078():
    # Spec section: ATX headings
    assert render_html('Foo bar\n# baz\nBar foo\n') == '<p>Foo bar</p>\n<h1>baz</h1>\n<p>Bar foo</p>\n'


def test_example_079():
    # Spec section: ATX headings
    assert render_html('## \n#\n### ###\n') == '<h2></h2>\n<h1></h1>\n<h3></h3>\n'
