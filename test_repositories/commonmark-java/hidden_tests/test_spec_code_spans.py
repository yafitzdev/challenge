from src.commonmark import render_html


def test_example_328():
    # Spec section: Code spans
    assert render_html('`foo`\n') == '<p><code>foo</code></p>\n'


def test_example_329():
    # Spec section: Code spans
    assert render_html('`` foo ` bar ``\n') == '<p><code>foo ` bar</code></p>\n'


def test_example_331():
    # Spec section: Code spans
    assert render_html('`  ``  `\n') == '<p><code> `` </code></p>\n'


def test_example_332():
    # Spec section: Code spans
    assert render_html('` a`\n') == '<p><code> a</code></p>\n'


def test_example_333():
    # Spec section: Code spans
    assert render_html('`\xa0b\xa0`\n') == '<p><code>\xa0b\xa0</code></p>\n'


def test_example_334():
    # Spec section: Code spans
    assert render_html('`\xa0`\n`  `\n') == '<p><code>\xa0</code>\n<code>  </code></p>\n'


def test_example_335():
    # Spec section: Code spans
    assert render_html('``\nfoo\nbar  \nbaz\n``\n') == '<p><code>foo bar   baz</code></p>\n'


def test_example_336():
    # Spec section: Code spans
    assert render_html('``\nfoo \n``\n') == '<p><code>foo </code></p>\n'


def test_example_337():
    # Spec section: Code spans
    assert render_html('`foo   bar \nbaz`\n') == '<p><code>foo   bar  baz</code></p>\n'


def test_example_338():
    # Spec section: Code spans
    assert render_html('`foo\\`bar`\n') == '<p><code>foo\\</code>bar`</p>\n'


def test_example_339():
    # Spec section: Code spans
    assert render_html('``foo`bar``\n') == '<p><code>foo`bar</code></p>\n'


def test_example_341():
    # Spec section: Code spans
    assert render_html('*foo`*`\n') == '<p>*foo<code>*</code></p>\n'


def test_example_342():
    # Spec section: Code spans
    assert render_html('[not a `link](/foo`)\n') == '<p>[not a <code>link](/foo</code>)</p>\n'


def test_example_343():
    # Spec section: Code spans
    assert render_html('`<a href="`">`\n') == '<p><code>&lt;a href=&quot;</code>&quot;&gt;`</p>\n'


def test_example_344():
    # Spec section: Code spans
    assert render_html('<a href="`">`\n') == '<p><a href="`">`</p>\n'


def test_example_345():
    # Spec section: Code spans
    assert render_html('`<https://foo.bar.`baz>`\n') == '<p><code>&lt;https://foo.bar.</code>baz&gt;`</p>\n'


def test_example_346():
    # Spec section: Code spans
    assert render_html('<https://foo.bar.`baz>`\n') == '<p><a href="https://foo.bar.%60baz">https://foo.bar.`baz</a>`</p>\n'


def test_example_347():
    # Spec section: Code spans
    assert render_html('```foo``\n') == '<p>```foo``</p>\n'


def test_example_348():
    # Spec section: Code spans
    assert render_html('`foo\n') == '<p>`foo</p>\n'


def test_example_349():
    # Spec section: Code spans
    assert render_html('`foo``bar``\n') == '<p>`foo<code>bar</code></p>\n'
