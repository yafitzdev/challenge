from src.commonmark import render_html


def test_example_119():
    # Spec section: Fenced code blocks
    assert render_html('```\n<\n >\n```\n') == '<pre><code>&lt;\n &gt;\n</code></pre>\n'


def test_example_121():
    # Spec section: Fenced code blocks
    assert render_html('``\nfoo\n``\n') == '<p><code>foo</code></p>\n'


def test_example_122():
    # Spec section: Fenced code blocks
    assert render_html('```\naaa\n~~~\n```\n') == '<pre><code>aaa\n~~~\n</code></pre>\n'


def test_example_123():
    # Spec section: Fenced code blocks
    assert render_html('~~~\naaa\n```\n~~~\n') == '<pre><code>aaa\n```\n</code></pre>\n'


def test_example_124():
    # Spec section: Fenced code blocks
    assert render_html('````\naaa\n```\n``````\n') == '<pre><code>aaa\n```\n</code></pre>\n'


def test_example_125():
    # Spec section: Fenced code blocks
    assert render_html('~~~~\naaa\n~~~\n~~~~\n') == '<pre><code>aaa\n~~~\n</code></pre>\n'


def test_example_126():
    # Spec section: Fenced code blocks
    assert render_html('```\n') == '<pre><code></code></pre>\n'


def test_example_127():
    # Spec section: Fenced code blocks
    assert render_html('`````\n\n```\naaa\n') == '<pre><code>\n```\naaa\n</code></pre>\n'


def test_example_128():
    # Spec section: Fenced code blocks
    assert render_html('> ```\n> aaa\n\nbbb\n') == '<blockquote>\n<pre><code>aaa\n</code></pre>\n</blockquote>\n<p>bbb</p>\n'


def test_example_129():
    # Spec section: Fenced code blocks
    assert render_html('```\n\n  \n```\n') == '<pre><code>\n  \n</code></pre>\n'


def test_example_131():
    # Spec section: Fenced code blocks
    assert render_html(' ```\n aaa\naaa\n```\n') == '<pre><code>aaa\naaa\n</code></pre>\n'


def test_example_132():
    # Spec section: Fenced code blocks
    assert render_html('  ```\naaa\n  aaa\naaa\n  ```\n') == '<pre><code>aaa\naaa\naaa\n</code></pre>\n'


def test_example_133():
    # Spec section: Fenced code blocks
    assert render_html('   ```\n   aaa\n    aaa\n  aaa\n   ```\n') == '<pre><code>aaa\n aaa\naaa\n</code></pre>\n'


def test_example_134():
    # Spec section: Fenced code blocks
    assert render_html('    ```\n    aaa\n    ```\n') == '<pre><code>```\naaa\n```\n</code></pre>\n'


def test_example_135():
    # Spec section: Fenced code blocks
    assert render_html('```\naaa\n  ```\n') == '<pre><code>aaa\n</code></pre>\n'


def test_example_136():
    # Spec section: Fenced code blocks
    assert render_html('   ```\naaa\n  ```\n') == '<pre><code>aaa\n</code></pre>\n'


def test_example_137():
    # Spec section: Fenced code blocks
    assert render_html('```\naaa\n    ```\n') == '<pre><code>aaa\n    ```\n</code></pre>\n'


def test_example_138():
    # Spec section: Fenced code blocks
    assert render_html('``` ```\naaa\n') == '<p><code> </code>\naaa</p>\n'


def test_example_139():
    # Spec section: Fenced code blocks
    assert render_html('~~~~~~\naaa\n~~~ ~~\n') == '<pre><code>aaa\n~~~ ~~\n</code></pre>\n'


def test_example_141():
    # Spec section: Fenced code blocks
    assert render_html('foo\n---\n~~~\nbar\n~~~\n# baz\n') == '<h2>foo</h2>\n<pre><code>bar\n</code></pre>\n<h1>baz</h1>\n'


def test_example_142():
    # Spec section: Fenced code blocks
    assert render_html('```ruby\ndef foo(x)\n  return 3\nend\n```\n') == '<pre><code class="language-ruby">def foo(x)\n  return 3\nend\n</code></pre>\n'


def test_example_143():
    # Spec section: Fenced code blocks
    assert render_html('~~~~    ruby startline=3 $%@#$\ndef foo(x)\n  return 3\nend\n~~~~~~~\n') == '<pre><code class="language-ruby">def foo(x)\n  return 3\nend\n</code></pre>\n'


def test_example_144():
    # Spec section: Fenced code blocks
    assert render_html('````;\n````\n') == '<pre><code class="language-;"></code></pre>\n'


def test_example_145():
    # Spec section: Fenced code blocks
    assert render_html('``` aa ```\nfoo\n') == '<p><code>aa</code>\nfoo</p>\n'


def test_example_146():
    # Spec section: Fenced code blocks
    assert render_html('~~~ aa ``` ~~~\nfoo\n~~~\n') == '<pre><code class="language-aa">foo\n</code></pre>\n'


def test_example_147():
    # Spec section: Fenced code blocks
    assert render_html('```\n``` aaa\n```\n') == '<pre><code>``` aaa\n</code></pre>\n'
