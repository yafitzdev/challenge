import io
import sys
import os
import tempfile
import pytest
from src.props2js import props2js

def create_temp_properties_file_public(content):
    fd, path = tempfile.mkstemp(suffix=".properties")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def test_json_stdout_public(monkeypatch):
    props = "hello=world\ncount=128\nenabled=false"
    file = create_temp_properties_file_public(props)
    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)
    props2js.main([file])
    result = output.getvalue()
    assert "\"hello\":\"world\"" in result
    assert "\"count\":128" in result
    assert "\"enabled\":false" in result
    os.remove(file)

def test_json_output_file_public(tmp_path):
    props = "baz=qux"
    file = create_temp_properties_file_public(props)
    out_file = tmp_path / "public_out.js"
    props2js.main(["-o", str(out_file), file])
    content = out_file.read_text(encoding="utf-8")
    assert "\"baz\":\"qux\"" in content
    os.remove(file)

def test_js_output_type_with_name_public(tmp_path):
    props = "alpha=omega\nnumval=12"
    file = create_temp_properties_file_public(props)
    out_file = tmp_path / "public_out.js"
    props2js.main(["-o", str(out_file), "-t", "js", "-n", "newVar", file])
    content = out_file.read_text(encoding="utf-8")
    assert content.startswith("var newVar=") or content.startswith("newVar=")
    assert "\"alpha\":\"omega\"" in content
    os.remove(file)

def test_jsonp_output_type_with_name_public(tmp_path):
    props = "b=22"
    file = create_temp_properties_file_public(props)
    out_file = tmp_path / "public_out.js"
    props2js.main(["-o", str(out_file), "-t", "jsonp", "-n", "fCallback", file])
    content = out_file.read_text(encoding="utf-8")
    assert content.startswith("fCallback(")
    assert content.endswith(");")
    assert "\"b\":22" in content
    os.remove(file)

def test_help_option_public(monkeypatch):
    output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", output)
    try:
        props2js.main(["--help"])
    except SystemExit:
        pass
    out = output.getvalue()
    assert "props2js [options]" in out

def test_missing_input_file_public():
    with pytest.raises(Exception):
        props2js.main(["--output", "nofile.js"])

def test_missing_name_with_js_type_public(tmp_path):
    props = "some=99"
    file = create_temp_properties_file_public(props)
    with pytest.raises(Exception):
        props2js.main(["-t", "js", file])
    os.remove(file)

def test_missing_name_with_jsonp_type_public(tmp_path):
    props = "some=88"
    file = create_temp_properties_file_public(props)
    with pytest.raises(Exception):
        props2js.main(["-t", "jsonp", file])
    os.remove(file)

def test_verbose_logs_public(tmp_path, capsys):
    props = "welcome=here"
    file = create_temp_properties_file_public(props)
    out_file = tmp_path / "public_out.js"
    props2js.main(["-v", "-o", str(out_file), file])
    captured = capsys.readouterr()
    err = captured.err
    assert "Output file is" in err
    os.remove(file)

def test_default_output_type_is_json_public(tmp_path, capsys):
    props = "foo=barz"
    file = create_temp_properties_file_public(props)
    output = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = output
    props2js.main(["-v", file])
    sys.stdout = sys_stdout
    captured = capsys.readouterr()
    err = captured.err
    assert "defaulting to json" in err
    os.remove(file)