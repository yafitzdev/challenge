"""Port of net.nczonline.web.props2js.PropertyConverter (Gson-compatible JSON output)."""
import math
import re
import struct

_float_pattern = re.compile(r"[0-9]+(\.[0-9]+)?")
_int_pattern = re.compile(r"[0-9]+")

_INT_MIN = -(2 ** 31)
_INT_MAX = 2 ** 31 - 1


def _parse_int(value):
    """Integer.parseInt: raises ValueError (NumberFormatException) on overflow."""
    n = int(value, 10)
    if n < _INT_MIN or n > _INT_MAX:
        raise ValueError('For input string: "%s"' % value)
    return n


def _to_float32(x):
    return struct.unpack(">f", struct.pack(">f", x))[0]


def _java_float_to_string(value):
    """Approximates Java's Float.toString for a finite float32 value."""
    f = _to_float32(value)
    if f != f:
        return "NaN"
    if math.isinf(f):
        return "Infinity" if f > 0 else "-Infinity"
    if f == 0.0:
        return "-0.0" if math.copysign(1.0, f) < 0 else "0.0"
    # shortest decimal digits that round-trip through float32
    digits = None
    for p in range(1, 10):
        s = "%.*e" % (p - 1, f)
        if _to_float32(float(s)) == f:
            digits = s
            break
    if digits is None:
        digits = "%.8e" % f
    sign = ""
    if digits.startswith("-"):
        sign = "-"
        digits = digits[1:]
    mant, exp = digits.split("e")
    exp = int(exp)
    mant_digits = mant.replace(".", "").rstrip("0") or "0"
    a = abs(f)
    if 1e-3 <= a < 1e7:
        # plain decimal notation
        point = exp + 1  # position of decimal point relative to digit string
        if point <= 0:
            int_part = "0"
            frac = "0" * (-point) + mant_digits
        elif point >= len(mant_digits):
            int_part = mant_digits + "0" * (point - len(mant_digits))
            frac = ""
        else:
            int_part = mant_digits[:point]
            frac = mant_digits[point:]
        frac = frac.rstrip("0") or "0"
        return sign + int_part + "." + frac
    # computerized scientific notation: d.dddE[-]n
    first = mant_digits[0]
    rest = mant_digits[1:] or "0"
    return sign + first + "." + rest + "E" + str(exp)


def _gson_escape(s):
    """Escapes a string the way Gson's JsonWriter does (htmlSafe=true by default)."""
    out = ['"']
    for c in s:
        if c == '"' or c == "\\":
            out.append("\\" + c)
        elif c == "\t":
            out.append("\\t")
        elif c == "\b":
            out.append("\\b")
        elif c == "\n":
            out.append("\\n")
        elif c == "\r":
            out.append("\\r")
        elif c == "\f":
            out.append("\\f")
        elif c in "<>&='":
            out.append("\\u%04x" % ord(c))
        elif c in "  ":
            out.append("\\u%04x" % ord(c))
        elif ord(c) <= 0x1F:
            out.append("\\u%04x" % ord(c))
        else:
            out.append(c)
    out.append('"')
    return "".join(out)


def _keys(properties):
    if hasattr(properties, "keys"):
        return list(properties.keys())
    return list(properties)


def _get_property(properties, key):
    if hasattr(properties, "get_property"):
        return properties.get_property(key)
    if hasattr(properties, "getProperty"):
        return properties.getProperty(key)
    return properties.get(key)


def convert_to_json(properties):
    """Converts the properties object into a JSON string."""
    members = []
    for key in _keys(properties):
        k = str(key)
        value = _get_property(properties, k)
        if value == "true" or value == "false":
            rendered = "true" if value == "true" else "false"
        elif _int_pattern.fullmatch(value):
            rendered = str(_parse_int(value))
        elif _float_pattern.fullmatch(value):
            rendered = _java_float_to_string(float(value))
        else:
            rendered = _gson_escape(value)
        members.append(_gson_escape(k) + ":" + rendered)
    return "{" + ",".join(members) + "}"


def convert_to_jsonp(properties, callback):
    """Converts the properties object into a JSONP string: callback(json);"""
    return str(callback) + "(" + convert_to_json(properties) + ");"


def convert_to_javascript(properties, variable):
    """Converts to 'var variable=json;' or 'object.property=json;'."""
    result = str(variable) + "=" + convert_to_json(properties) + ";"
    if "." not in variable:
        result = "var " + result
    return result


# Java-style aliases
convertToJson = convert_to_json
convertToJsonP = convert_to_jsonp
convertToJavaScript = convert_to_javascript


class PropertyConverter:
    convert_to_json = staticmethod(convert_to_json)
    convert_to_jsonp = staticmethod(convert_to_jsonp)
    convert_to_javascript = staticmethod(convert_to_javascript)
    convertToJson = staticmethod(convert_to_json)
    convertToJsonP = staticmethod(convert_to_jsonp)
    convertToJavaScript = staticmethod(convert_to_javascript)
