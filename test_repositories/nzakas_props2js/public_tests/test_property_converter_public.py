from src.props2js import property_converter

def test_convert_to_json_with_string_public():
    p = {"color": "blue"}
    json_out = property_converter.convert_to_json(p)
    assert "\"color\":\"blue\"" in json_out

def test_convert_to_json_with_int_public():
    p = {"answer": "42"}
    json_out = property_converter.convert_to_json(p)
    assert "\"answer\":42" in json_out

def test_convert_to_json_with_float_public():
    p = {"ratio": "3.14"}
    json_out = property_converter.convert_to_json(p)
    assert "\"ratio\":3.14" in json_out

def test_convert_to_json_with_boolean_true_public():
    p = {"active": "true"}
    json_out = property_converter.convert_to_json(p)
    assert "\"active\":true" in json_out

def test_convert_to_json_with_boolean_false_public():
    p = {"deleted": "false"}
    json_out = property_converter.convert_to_json(p)
    assert "\"deleted\":false" in json_out

def test_convert_to_jsonp_public():
    p = {"score": "77"}
    out = property_converter.convert_to_jsonp(p, "pubcb")
    assert out.startswith("pubcb(")
    assert out.endswith(");")

def test_convert_to_javascript_var_public():
    p = {"animal": "cat"}
    js = property_converter.convert_to_javascript(p, "pubVar")
    assert js.startswith("var pubVar=")
    assert js.endswith(";")

def test_convert_to_javascript_assignment_public():
    p = {"animal": "dog"}
    js = property_converter.convert_to_javascript(p, "globals.pet")
    assert not js.startswith("var ")
    assert js.startswith("globals.pet=")
    assert js.endswith(";")

def test_convert_to_json_with_mixed_types_public():
    p = {
        "note": "hello",
        "age": "30",
        "pi": "3.1416",
        "success": "true",
        "error": "false"
    }
    json_out = property_converter.convert_to_json(p)
    assert "\"note\":\"hello\"" in json_out
    assert "\"age\":30" in json_out
    assert "\"pi\":3.1416" in json_out
    assert "\"success\":true" in json_out
    assert "\"error\":false" in json_out

def test_convert_to_json_handles_empty_properties_public():
    p = {}
    json_out = property_converter.convert_to_json(p)
    assert json_out == "{}"