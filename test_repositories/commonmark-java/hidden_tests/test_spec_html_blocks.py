from src.commonmark import render_html


def test_example_148():
    # Spec section: HTML blocks
    assert render_html('<table><tr><td>\n<pre>\n**Hello**,\n\n_world_.\n</pre>\n</td></tr></table>\n') == '<table><tr><td>\n<pre>\n**Hello**,\n<p><em>world</em>.\n</pre></p>\n</td></tr></table>\n'


def test_example_149():
    # Spec section: HTML blocks
    assert render_html('<table>\n  <tr>\n    <td>\n           hi\n    </td>\n  </tr>\n</table>\n\nokay.\n') == '<table>\n  <tr>\n    <td>\n           hi\n    </td>\n  </tr>\n</table>\n<p>okay.</p>\n'


def test_example_151():
    # Spec section: HTML blocks
    assert render_html('</div>\n*foo*\n') == '</div>\n*foo*\n'


def test_example_152():
    # Spec section: HTML blocks
    assert render_html('<DIV CLASS="foo">\n\n*Markdown*\n\n</DIV>\n') == '<DIV CLASS="foo">\n<p><em>Markdown</em></p>\n</DIV>\n'


def test_example_153():
    # Spec section: HTML blocks
    assert render_html('<div id="foo"\n  class="bar">\n</div>\n') == '<div id="foo"\n  class="bar">\n</div>\n'


def test_example_154():
    # Spec section: HTML blocks
    assert render_html('<div id="foo" class="bar\n  baz">\n</div>\n') == '<div id="foo" class="bar\n  baz">\n</div>\n'


def test_example_155():
    # Spec section: HTML blocks
    assert render_html('<div>\n*foo*\n\n*bar*\n') == '<div>\n*foo*\n<p><em>bar</em></p>\n'


def test_example_156():
    # Spec section: HTML blocks
    assert render_html('<div id="foo"\n*hi*\n') == '<div id="foo"\n*hi*\n'


def test_example_157():
    # Spec section: HTML blocks
    assert render_html('<div class\nfoo\n') == '<div class\nfoo\n'


def test_example_158():
    # Spec section: HTML blocks
    assert render_html('<div *???-&&&-<---\n*foo*\n') == '<div *???-&&&-<---\n*foo*\n'


def test_example_159():
    # Spec section: HTML blocks
    assert render_html('<div><a href="bar">*foo*</a></div>\n') == '<div><a href="bar">*foo*</a></div>\n'


def test_example_161():
    # Spec section: HTML blocks
    assert render_html('<div></div>\n``` c\nint x = 33;\n```\n') == '<div></div>\n``` c\nint x = 33;\n```\n'


def test_example_162():
    # Spec section: HTML blocks
    assert render_html('<a href="foo">\n*bar*\n</a>\n') == '<a href="foo">\n*bar*\n</a>\n'


def test_example_163():
    # Spec section: HTML blocks
    assert render_html('<Warning>\n*bar*\n</Warning>\n') == '<Warning>\n*bar*\n</Warning>\n'


def test_example_164():
    # Spec section: HTML blocks
    assert render_html('<i class="foo">\n*bar*\n</i>\n') == '<i class="foo">\n*bar*\n</i>\n'


def test_example_165():
    # Spec section: HTML blocks
    assert render_html('</ins>\n*bar*\n') == '</ins>\n*bar*\n'


def test_example_166():
    # Spec section: HTML blocks
    assert render_html('<del>\n*foo*\n</del>\n') == '<del>\n*foo*\n</del>\n'


def test_example_167():
    # Spec section: HTML blocks
    assert render_html('<del>\n\n*foo*\n\n</del>\n') == '<del>\n<p><em>foo</em></p>\n</del>\n'


def test_example_168():
    # Spec section: HTML blocks
    assert render_html('<del>*foo*</del>\n') == '<p><del><em>foo</em></del></p>\n'


def test_example_169():
    # Spec section: HTML blocks
    assert render_html('<pre language="haskell"><code>\nimport Text.HTML.TagSoup\n\nmain :: IO ()\nmain = print $ parseTags tags\n</code></pre>\nokay\n') == '<pre language="haskell"><code>\nimport Text.HTML.TagSoup\n\nmain :: IO ()\nmain = print $ parseTags tags\n</code></pre>\n<p>okay</p>\n'


def test_example_171():
    # Spec section: HTML blocks
    assert render_html('<textarea>\n\n*foo*\n\n_bar_\n\n</textarea>\n') == '<textarea>\n\n*foo*\n\n_bar_\n\n</textarea>\n'


def test_example_172():
    # Spec section: HTML blocks
    assert render_html('<style\n  type="text/css">\nh1 {color:red;}\n\np {color:blue;}\n</style>\nokay\n') == '<style\n  type="text/css">\nh1 {color:red;}\n\np {color:blue;}\n</style>\n<p>okay</p>\n'


def test_example_173():
    # Spec section: HTML blocks
    assert render_html('<style\n  type="text/css">\n\nfoo\n') == '<style\n  type="text/css">\n\nfoo\n'


def test_example_174():
    # Spec section: HTML blocks
    assert render_html('> <div>\n> foo\n\nbar\n') == '<blockquote>\n<div>\nfoo\n</blockquote>\n<p>bar</p>\n'


def test_example_175():
    # Spec section: HTML blocks
    assert render_html('- <div>\n- foo\n') == '<ul>\n<li>\n<div>\n</li>\n<li>foo</li>\n</ul>\n'


def test_example_176():
    # Spec section: HTML blocks
    assert render_html('<style>p{color:red;}</style>\n*foo*\n') == '<style>p{color:red;}</style>\n<p><em>foo</em></p>\n'


def test_example_177():
    # Spec section: HTML blocks
    assert render_html('<!-- foo -->*bar*\n*baz*\n') == '<!-- foo -->*bar*\n<p><em>baz</em></p>\n'


def test_example_178():
    # Spec section: HTML blocks
    assert render_html('<script>\nfoo\n</script>1. *bar*\n') == '<script>\nfoo\n</script>1. *bar*\n'


def test_example_179():
    # Spec section: HTML blocks
    assert render_html('<!-- Foo\n\nbar\n   baz -->\nokay\n') == '<!-- Foo\n\nbar\n   baz -->\n<p>okay</p>\n'


def test_example_181():
    # Spec section: HTML blocks
    assert render_html('<!DOCTYPE html>\n') == '<!DOCTYPE html>\n'


def test_example_182():
    # Spec section: HTML blocks
    assert render_html('<![CDATA[\nfunction matchwo(a,b)\n{\n  if (a < b && a < 0) then {\n    return 1;\n\n  } else {\n\n    return 0;\n  }\n}\n]]>\nokay\n') == '<![CDATA[\nfunction matchwo(a,b)\n{\n  if (a < b && a < 0) then {\n    return 1;\n\n  } else {\n\n    return 0;\n  }\n}\n]]>\n<p>okay</p>\n'


def test_example_183():
    # Spec section: HTML blocks
    assert render_html('  <!-- foo -->\n\n    <!-- foo -->\n') == '  <!-- foo -->\n<pre><code>&lt;!-- foo --&gt;\n</code></pre>\n'


def test_example_184():
    # Spec section: HTML blocks
    assert render_html('  <div>\n\n    <div>\n') == '  <div>\n<pre><code>&lt;div&gt;\n</code></pre>\n'


def test_example_185():
    # Spec section: HTML blocks
    assert render_html('Foo\n<div>\nbar\n</div>\n') == '<p>Foo</p>\n<div>\nbar\n</div>\n'


def test_example_186():
    # Spec section: HTML blocks
    assert render_html('<div>\nbar\n</div>\n*foo*\n') == '<div>\nbar\n</div>\n*foo*\n'


def test_example_187():
    # Spec section: HTML blocks
    assert render_html('Foo\n<a href="bar">\nbaz\n') == '<p>Foo\n<a href="bar">\nbaz</p>\n'


def test_example_188():
    # Spec section: HTML blocks
    assert render_html('<div>\n\n*Emphasized* text.\n\n</div>\n') == '<div>\n<p><em>Emphasized</em> text.</p>\n</div>\n'


def test_example_189():
    # Spec section: HTML blocks
    assert render_html('<div>\n*Emphasized* text.\n</div>\n') == '<div>\n*Emphasized* text.\n</div>\n'


def test_example_191():
    # Spec section: HTML blocks
    assert render_html('<table>\n\n  <tr>\n\n    <td>\n      Hi\n    </td>\n\n  </tr>\n\n</table>\n') == '<table>\n  <tr>\n<pre><code>&lt;td&gt;\n  Hi\n&lt;/td&gt;\n</code></pre>\n  </tr>\n</table>\n'
