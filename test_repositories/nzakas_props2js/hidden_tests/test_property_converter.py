import pytest
from src.props2js import property_converter

def test_convert_to_json_with_string():
    p = {"name": "value"}
    json_out = property_converter.convert_to_json(p)
    assert "\"name\":\"value\"" in json_out

def test_convert_to_json_with_int():
    p = {"intValue": "123"}
    json_out = property_converter.convert_to_json(p)
    assert "\"intValue\":123" in json_out

def test_convert_to_json_with_float():
    p = {"floatValue": "12.34"}
    json_out = property_converter.convert_to_json(p)
    assert "\"floatValue\":12.34" in json_out

def test_convert_to_json_with_boolean_true():
    p = {"flag": "true"}
    json_out = property_converter.convert_to_json(p)
    assert "\"flag\":true" in json_out

def test_convert_to_json_with_boolean_false():
    p = {"flag": "false"}
    json_out = property_converter.convert_to_json(p)
    assert "\"flag\":false" in json_out

def test_convert_to_jsonp():
    p = {"a": "1"}
    out = property_converter.convert_to_jsonp(p, "cb")
    assert out.startswith("cb(")
    assert out.endswith(");")

def test_convert_to_javascript_var():
    p = {"foo": "bar"}
    js = property_converter.convert_to_javascript(p, "testVar")
    assert js.startswith("var testVar=")
    assert js.endswith(";")

def test_convert_to_javascript_assignment():
    p = {"foo": "bar"}
    js = property_converter.convert_to_javascript(p, "object.property")
    assert not js.startswith("var ")
    assert js.startswith("object.property=")
    assert js.endswith(";")

def test_convert_to_json_with_mixed_types():
    p = {
        "string": "text",
        "int": "42",
        "float": "2.718",
        "trueBool": "true",
        "falseBool": "false"
    }
    json_out = property_converter.convert_to_json(p)
    assert "\"string\":\"text\"" in json_out
    assert "\"int\":42" in json_out
    assert "\"float\":2.718" in json_out
    assert "\"trueBool\":true" in json_out
    assert "\"falseBool\":false" in json_out

def test_convert_to_json_handles_empty_properties():
    p = {}
    json_out = property_converter.convert_to_json(p)
    assert json_out == "{}"