from src.commonmark import render_html


def test_example_351():
    # Spec section: Emphasis and strong emphasis
    assert render_html('a * foo bar*\n') == '<p>a * foo bar*</p>\n'


def test_example_352():
    # Spec section: Emphasis and strong emphasis
    assert render_html('a*"foo"*\n') == '<p>a*&quot;foo&quot;*</p>\n'


def test_example_353():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*\xa0a\xa0*\n') == '<p>*\xa0a\xa0*</p>\n'


def test_example_354():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*$*alpha.\n\n*£*bravo.\n\n*€*charlie.\n') == '<p>*$*alpha.</p>\n<p>*£*bravo.</p>\n<p>*€*charlie.</p>\n'


def test_example_355():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo*bar*\n') == '<p>foo<em>bar</em></p>\n'


def test_example_356():
    # Spec section: Emphasis and strong emphasis
    assert render_html('5*6*78\n') == '<p>5<em>6</em>78</p>\n'


def test_example_357():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo bar_\n') == '<p><em>foo bar</em></p>\n'


def test_example_358():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_ foo bar_\n') == '<p>_ foo bar_</p>\n'


def test_example_359():
    # Spec section: Emphasis and strong emphasis
    assert render_html('a_"foo"_\n') == '<p>a_&quot;foo&quot;_</p>\n'


def test_example_361():
    # Spec section: Emphasis and strong emphasis
    assert render_html('5_6_78\n') == '<p>5_6_78</p>\n'


def test_example_362():
    # Spec section: Emphasis and strong emphasis
    assert render_html('пристаням_стремятся_\n') == '<p>пристаням_стремятся_</p>\n'


def test_example_363():
    # Spec section: Emphasis and strong emphasis
    assert render_html('aa_"bb"_cc\n') == '<p>aa_&quot;bb&quot;_cc</p>\n'


def test_example_364():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo-_(bar)_\n') == '<p>foo-<em>(bar)</em></p>\n'


def test_example_365():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo*\n') == '<p>_foo*</p>\n'


def test_example_366():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo bar *\n') == '<p>*foo bar *</p>\n'


def test_example_367():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo bar\n*\n') == '<p>*foo bar\n*</p>\n'


def test_example_368():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*(*foo)\n') == '<p>*(*foo)</p>\n'


def test_example_369():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*(*foo*)*\n') == '<p><em>(<em>foo</em>)</em></p>\n'


def test_example_371():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo bar _\n') == '<p>_foo bar _</p>\n'


def test_example_372():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_(_foo)\n') == '<p>_(_foo)</p>\n'


def test_example_373():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_(_foo_)_\n') == '<p><em>(<em>foo</em>)</em></p>\n'


def test_example_374():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo_bar\n') == '<p>_foo_bar</p>\n'


def test_example_375():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_пристаням_стремятся\n') == '<p>_пристаням_стремятся</p>\n'


def test_example_376():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo_bar_baz_\n') == '<p><em>foo_bar_baz</em></p>\n'


def test_example_377():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_(bar)_.\n') == '<p><em>(bar)</em>.</p>\n'


def test_example_378():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo bar**\n') == '<p><strong>foo bar</strong></p>\n'


def test_example_379():
    # Spec section: Emphasis and strong emphasis
    assert render_html('** foo bar**\n') == '<p>** foo bar**</p>\n'


def test_example_381():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo**bar**\n') == '<p>foo<strong>bar</strong></p>\n'


def test_example_382():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo bar__\n') == '<p><strong>foo bar</strong></p>\n'


def test_example_383():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__ foo bar__\n') == '<p>__ foo bar__</p>\n'


def test_example_384():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__\nfoo bar__\n') == '<p>__\nfoo bar__</p>\n'


def test_example_385():
    # Spec section: Emphasis and strong emphasis
    assert render_html('a__"foo"__\n') == '<p>a__&quot;foo&quot;__</p>\n'


def test_example_386():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo__bar__\n') == '<p>foo__bar__</p>\n'


def test_example_387():
    # Spec section: Emphasis and strong emphasis
    assert render_html('5__6__78\n') == '<p>5__6__78</p>\n'


def test_example_388():
    # Spec section: Emphasis and strong emphasis
    assert render_html('пристаням__стремятся__\n') == '<p>пристаням__стремятся__</p>\n'


def test_example_389():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo, __bar__, baz__\n') == '<p><strong>foo, <strong>bar</strong>, baz</strong></p>\n'


def test_example_391():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo bar **\n') == '<p>**foo bar **</p>\n'


def test_example_392():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**(**foo)\n') == '<p>**(**foo)</p>\n'


def test_example_393():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*(**foo**)*\n') == '<p><em>(<strong>foo</strong>)</em></p>\n'


def test_example_394():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**Gomphocarpus (*Gomphocarpus physocarpus*, syn.\n*Asclepias physocarpa*)**\n') == '<p><strong>Gomphocarpus (<em>Gomphocarpus physocarpus</em>, syn.\n<em>Asclepias physocarpa</em>)</strong></p>\n'


def test_example_395():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo "*bar*" foo**\n') == '<p><strong>foo &quot;<em>bar</em>&quot; foo</strong></p>\n'


def test_example_396():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo**bar\n') == '<p><strong>foo</strong>bar</p>\n'


def test_example_397():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo bar __\n') == '<p>__foo bar __</p>\n'


def test_example_398():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__(__foo)\n') == '<p>__(__foo)</p>\n'


def test_example_399():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_(__foo__)_\n') == '<p><em>(<strong>foo</strong>)</em></p>\n'


def test_example_401():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__пристаням__стремятся\n') == '<p>__пристаням__стремятся</p>\n'


def test_example_402():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo__bar__baz__\n') == '<p><strong>foo__bar__baz</strong></p>\n'


def test_example_403():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__(bar)__.\n') == '<p><strong>(bar)</strong>.</p>\n'


def test_example_404():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo [bar](/url)*\n') == '<p><em>foo <a href="/url">bar</a></em></p>\n'


def test_example_405():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo\nbar*\n') == '<p><em>foo\nbar</em></p>\n'


def test_example_406():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo __bar__ baz_\n') == '<p><em>foo <strong>bar</strong> baz</em></p>\n'


def test_example_407():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo _bar_ baz_\n') == '<p><em>foo <em>bar</em> baz</em></p>\n'


def test_example_408():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo_ bar_\n') == '<p><em><em>foo</em> bar</em></p>\n'


def test_example_409():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo *bar**\n') == '<p><em>foo <em>bar</em></em></p>\n'


def test_example_411():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo**bar**baz*\n') == '<p><em>foo<strong>bar</strong>baz</em></p>\n'


def test_example_412():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo**bar*\n') == '<p><em>foo**bar</em></p>\n'


def test_example_413():
    # Spec section: Emphasis and strong emphasis
    assert render_html('***foo** bar*\n') == '<p><em><strong>foo</strong> bar</em></p>\n'


def test_example_414():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo **bar***\n') == '<p><em>foo <strong>bar</strong></em></p>\n'


def test_example_415():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo**bar***\n') == '<p><em>foo<strong>bar</strong></em></p>\n'


def test_example_416():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo***bar***baz\n') == '<p>foo<em><strong>bar</strong></em>baz</p>\n'


def test_example_417():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo******bar*********baz\n') == '<p>foo<strong><strong><strong>bar</strong></strong></strong>***baz</p>\n'


def test_example_418():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo **bar *baz* bim** bop*\n') == '<p><em>foo <strong>bar <em>baz</em> bim</strong> bop</em></p>\n'


def test_example_419():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo [*bar*](/url)*\n') == '<p><em>foo <a href="/url"><em>bar</em></a></em></p>\n'


def test_example_421():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**** is not an empty strong emphasis\n') == '<p>**** is not an empty strong emphasis</p>\n'


def test_example_422():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo [bar](/url)**\n') == '<p><strong>foo <a href="/url">bar</a></strong></p>\n'


def test_example_423():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo\nbar**\n') == '<p><strong>foo\nbar</strong></p>\n'


def test_example_424():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo _bar_ baz__\n') == '<p><strong>foo <em>bar</em> baz</strong></p>\n'


def test_example_425():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo __bar__ baz__\n') == '<p><strong>foo <strong>bar</strong> baz</strong></p>\n'


def test_example_426():
    # Spec section: Emphasis and strong emphasis
    assert render_html('____foo__ bar__\n') == '<p><strong><strong>foo</strong> bar</strong></p>\n'


def test_example_427():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo **bar****\n') == '<p><strong>foo <strong>bar</strong></strong></p>\n'


def test_example_428():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo *bar* baz**\n') == '<p><strong>foo <em>bar</em> baz</strong></p>\n'


def test_example_429():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo*bar*baz**\n') == '<p><strong>foo<em>bar</em>baz</strong></p>\n'


def test_example_431():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo *bar***\n') == '<p><strong>foo <em>bar</em></strong></p>\n'


def test_example_432():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo *bar **baz**\nbim* bop**\n') == '<p><strong>foo <em>bar <strong>baz</strong>\nbim</em> bop</strong></p>\n'


def test_example_433():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo [*bar*](/url)**\n') == '<p><strong>foo <a href="/url"><em>bar</em></a></strong></p>\n'


def test_example_434():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__ is not an empty emphasis\n') == '<p>__ is not an empty emphasis</p>\n'


def test_example_435():
    # Spec section: Emphasis and strong emphasis
    assert render_html('____ is not an empty strong emphasis\n') == '<p>____ is not an empty strong emphasis</p>\n'


def test_example_436():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo ***\n') == '<p>foo ***</p>\n'


def test_example_437():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo *\\**\n') == '<p>foo <em>*</em></p>\n'


def test_example_438():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo *_*\n') == '<p>foo <em>_</em></p>\n'


def test_example_439():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo *****\n') == '<p>foo *****</p>\n'


def test_example_441():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo **_**\n') == '<p>foo <strong>_</strong></p>\n'


def test_example_442():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo*\n') == '<p>*<em>foo</em></p>\n'


def test_example_443():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo**\n') == '<p><em>foo</em>*</p>\n'


def test_example_444():
    # Spec section: Emphasis and strong emphasis
    assert render_html('***foo**\n') == '<p>*<strong>foo</strong></p>\n'


def test_example_445():
    # Spec section: Emphasis and strong emphasis
    assert render_html('****foo*\n') == '<p>***<em>foo</em></p>\n'


def test_example_446():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo***\n') == '<p><strong>foo</strong>*</p>\n'


def test_example_447():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo****\n') == '<p><em>foo</em>***</p>\n'


def test_example_448():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo ___\n') == '<p>foo ___</p>\n'


def test_example_449():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo _\\__\n') == '<p>foo <em>_</em></p>\n'


def test_example_451():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo _____\n') == '<p>foo _____</p>\n'


def test_example_452():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo __\\___\n') == '<p>foo <strong>_</strong></p>\n'


def test_example_453():
    # Spec section: Emphasis and strong emphasis
    assert render_html('foo __*__\n') == '<p>foo <strong>*</strong></p>\n'


def test_example_454():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo_\n') == '<p>_<em>foo</em></p>\n'


def test_example_455():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo__\n') == '<p><em>foo</em>_</p>\n'


def test_example_456():
    # Spec section: Emphasis and strong emphasis
    assert render_html('___foo__\n') == '<p>_<strong>foo</strong></p>\n'


def test_example_457():
    # Spec section: Emphasis and strong emphasis
    assert render_html('____foo_\n') == '<p>___<em>foo</em></p>\n'


def test_example_458():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo___\n') == '<p><strong>foo</strong>_</p>\n'


def test_example_459():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo____\n') == '<p><em>foo</em>___</p>\n'


def test_example_461():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*_foo_*\n') == '<p><em><em>foo</em></em></p>\n'


def test_example_462():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__foo__\n') == '<p><strong>foo</strong></p>\n'


def test_example_463():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_*foo*_\n') == '<p><em><em>foo</em></em></p>\n'


def test_example_464():
    # Spec section: Emphasis and strong emphasis
    assert render_html('****foo****\n') == '<p><strong><strong>foo</strong></strong></p>\n'


def test_example_465():
    # Spec section: Emphasis and strong emphasis
    assert render_html('____foo____\n') == '<p><strong><strong>foo</strong></strong></p>\n'


def test_example_466():
    # Spec section: Emphasis and strong emphasis
    assert render_html('******foo******\n') == '<p><strong><strong><strong>foo</strong></strong></strong></p>\n'


def test_example_467():
    # Spec section: Emphasis and strong emphasis
    assert render_html('***foo***\n') == '<p><em><strong>foo</strong></em></p>\n'


def test_example_468():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_____foo_____\n') == '<p><em><strong><strong>foo</strong></strong></em></p>\n'


def test_example_469():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo _bar* baz_\n') == '<p><em>foo _bar</em> baz_</p>\n'


def test_example_471():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**foo **bar baz**\n') == '<p>**foo <strong>bar baz</strong></p>\n'


def test_example_472():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*foo *bar baz*\n') == '<p>*foo <em>bar baz</em></p>\n'


def test_example_473():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*[bar*](/url)\n') == '<p>*<a href="/url">bar*</a></p>\n'


def test_example_474():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_foo [bar_](/url)\n') == '<p>_foo <a href="/url">bar_</a></p>\n'


def test_example_475():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*<img src="foo" title="*"/>\n') == '<p>*<img src="foo" title="*"/></p>\n'


def test_example_476():
    # Spec section: Emphasis and strong emphasis
    assert render_html('**<a href="**">\n') == '<p>**<a href="**"></p>\n'


def test_example_477():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__<a href="__">\n') == '<p>__<a href="__"></p>\n'


def test_example_478():
    # Spec section: Emphasis and strong emphasis
    assert render_html('*a `*`*\n') == '<p><em>a <code>*</code></em></p>\n'


def test_example_479():
    # Spec section: Emphasis and strong emphasis
    assert render_html('_a `_`_\n') == '<p><em>a <code>_</code></em></p>\n'


def test_example_481():
    # Spec section: Emphasis and strong emphasis
    assert render_html('__a<https://foo.bar/?q=__>\n') == '<p>__a<a href="https://foo.bar/?q=__">https://foo.bar/?q=__</a></p>\n'
