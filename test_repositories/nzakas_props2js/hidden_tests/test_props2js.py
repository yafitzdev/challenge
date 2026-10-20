import io
import sys
import os
import tempfile
import pytest
from src.props2js import props2js

def create_temp_properties_file(content):
    fd, path = tempfile.mkstemp(suffix=".properties")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def test_json_stdout(monkeypatch):
    props = "foo=bar\nnum=42\nflag=true"
    file = create_temp_properties_file(props)
    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)
    props2js.main([file])
    result = output.getvalue()
    assert "\"foo\":\"bar\"" in result
    assert "\"num\":42" in result
    assert "\"flag\":true" in result
    os.remove(file)

def test_json_output_file(tmp_path):
    props = "foo=bar"
    file = create_temp_properties_file(props)
    out_file = tmp_path / "out.js"
    props2js.main(["-o", str(out_file), file])
    content = out_file.read_text(encoding="utf-8")
    assert "\"foo\":\"bar\"" in content
    os.remove(file)

def test_js_output_type_with_name(tmp_path):
    props = "foo=bar\nval=5"
    file = create_temp_properties_file(props)
    out_file = tmp_path / "out.js"
    props2js.main(["-o", str(out_file), "-t", "js", "-n", "resultVar", file])
    content = out_file.read_text(encoding="utf-8")
    assert content.startswith("var resultVar=") or content.startswith("resultVar=")
    assert "\"foo\":\"bar\"" in content
    os.remove(file)

def test_jsonp_output_type_with_name(tmp_path):
    props = "a=1"
    file = create_temp_properties_file(props)
    out_file = tmp_path / "out.js"
    props2js.main(["-o", str(out_file), "-t", "jsonp", "-n", "cb", file])
    content = out_file.read_text(encoding="utf-8")
    assert content.startswith("cb(")
    assert content.endswith(");")
    assert "\"a\":1" in content
    os.remove(file)

def test_help_option(monkeypatch):
    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)
    try:
        props2js.main(["-h"])
    except SystemExit:
        pass
    out = output.getvalue()
    assert "props2js [options]" in out

def test_missing_input_file():
    with pytest.raises(Exception):
        props2js.main([])

def test_missing_name_with_js_type(tmp_path):
    props = "x=1"
    file = create_temp_properties_file(props)
    with pytest.raises(Exception):
        props2js.main(["-t", "js", file])
    os.remove(file)

def test_missing_name_with_jsonp_type(tmp_path):
    props = "x=1"
    file = create_temp_properties_file(props)
    with pytest.raises(Exception):
        props2js.main(["-t", "jsonp", file])
    os.remove(file)

def test_verbose_logs(tmp_path, capsys):
    props = "foo=bar"
    file = create_temp_properties_file(props)
    out_file = tmp_path / "out.js"
    props2js.main(["-v", "-o", str(out_file), file])
    captured = capsys.readouterr()
    err = captured.err
    assert "Output file is" in err
    os.remove(file)

def test_default_output_type_is_json(tmp_path, capsys):
    props = "y=world"
    file = create_temp_properties_file(props)
    output = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = output
    props2js.main(["-v", file])
    sys.stdout = sys_stdout
    captured = capsys.readouterr()
    err = captured.err
    assert "defaulting to json" in err
    os.remove(file)