"""Python port of OpenGamma ElSql (com.opengamma.elsql)."""

import numbers
import os
import re
import sys

INTEGER_MAX_VALUE = 2147483647


# ---------------------------------------------------------------------------
# helpers emulating Java semantics
# ---------------------------------------------------------------------------
def _java_trim(s):
    start = 0
    end = len(s)
    while start < end and s[start] <= ' ':
        start += 1
    while end > start and s[end - 1] <= ' ':
        end -= 1
    return s[start:end]


def _java_str(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _parse_int(text):
    if not isinstance(text, str) or re.fullmatch(r"[+-]?[0-9]+", text) is None:
        raise ValueError('For input string: "%s"' % (text,))
    value = int(text)
    if value > INTEGER_MAX_VALUE or value < -INTEGER_MAX_VALUE - 1:
        raise ValueError('For input string: "%s"' % (text,))
    return value


def _is_number(value):
    return isinstance(value, numbers.Number) and not isinstance(value, bool)


def _buf_str(buf):
    return "".join(buf)


def _buf_len(buf):
    return sum(len(s) for s in buf)


def _buf_set_length(buf, length):
    text = "".join(buf)[:length]
    buf[:] = [text] if text else []


def _buf_ends_with(buf, match):
    s = _buf_str(buf)
    tail = s[len(s) - len(match):] if len(s) >= len(match) else ""
    return tail == match


# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------
class ElSqlConfig(object):

    DEFAULT = None
    POSTGRES = None
    HSQL = None
    MYSQL = None
    ORACLE = None
    SQL_SERVER_2008 = None
    VERTICA = None

    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    def isLikeWildcard(self, value):
        escape = False
        for ch in value:
            if escape:
                escape = False
            else:
                if ch == '\\':
                    escape = True
                elif ch == '%' or ch == '_':
                    return True
        return False

    def getLikeSuffix(self):
        return ""

    def addPaging(self, selectToPage, offset, fetchLimit):
        return selectToPage + ("" if selectToPage.endswith(" ") else " ") + self.getPaging(offset, fetchLimit)

    def getPaging(self, offset, fetchLimit):
        if fetchLimit == 0 and offset == 0:
            return ""
        if fetchLimit == 0:
            return "OFFSET " + str(offset) + " ROWS "
        if offset == 0:
            return "FETCH FIRST " + str(fetchLimit) + " ROWS ONLY "
        return "OFFSET " + str(offset) + " ROWS FETCH NEXT " + str(fetchLimit) + " ROWS ONLY "

    def __str__(self):
        return "ElSqlConfig[" + _java_str(self._name) + "]"

    __repr__ = __str__


class _PostgresElSqlConfig(ElSqlConfig):
    def __init__(self):
        ElSqlConfig.__init__(self, "Postgres")


class _HsqlElSqlConfig(ElSqlConfig):
    def __init__(self):
        ElSqlConfig.__init__(self, "HSQL")

    def getLikeSuffix(self):
        return "ESCAPE '\\' "


class _MySqlElSqlConfig(ElSqlConfig):
    def __init__(self):
        ElSqlConfig.__init__(self, "MySql")

    def getPaging(self, offset, fetchLimit):
        if fetchLimit == 0 and offset == 0:
            return ""
        if fetchLimit == 0:
            return "OFFSET " + str(offset) + " "
        if offset == 0:
            return "LIMIT " + str(fetchLimit) + " "
        return "LIMIT " + str(fetchLimit) + " OFFSET " + str(offset) + " "


class _OracleElSqlConfig(ElSqlConfig):
    def __init__(self):
        ElSqlConfig.__init__(self, "Oracle")

    def addPaging(self, selectToPage, offset, fetchLimit):
        if fetchLimit == 0 and offset == 0:
            return selectToPage
        if offset == 0 and fetchLimit > 0:
            return "SELECT * FROM ( " + selectToPage + " ) where rownum <= " + str(fetchLimit)
        start = offset
        end = offset + fetchLimit
        return ("SELECT * FROM (SELECT  row_.*,rownum rownum_ FROM ( " + selectToPage
                + " ) row_ where rownum <= " + str(end) + ")  WHERE rownum_  > " + str(start))

    def getPaging(self, offset, fetchLimit):
        raise NotImplementedError()


class _SqlServer2008ElSqlConfig(ElSqlConfig):
    def __init__(self):
        ElSqlConfig.__init__(self, "SqlServer2008")

    def addPaging(self, selectToPage, offset, fetchLimit):
        if fetchLimit == 0 and offset == 0:
            return selectToPage.replace("SELECT ", "SELECT TOP " + str(INTEGER_MAX_VALUE) + " ", 1)
        start = offset + 1
        end = offset + fetchLimit
        columns = selectToPage[selectToPage.index("SELECT ") + 7:selectToPage.index(" FROM ")]
        frm = selectToPage[selectToPage.index(" FROM ") + 6:selectToPage.index(" ORDER BY ")]
        order = selectToPage[selectToPage.index(" ORDER BY ") + 10:]
        inner = ("SELECT " + columns + ", ROW_NUMBER() OVER (ORDER BY " + _java_trim(order)
                 + ") AS ROW_NUM FROM " + frm)
        return ("SELECT * FROM (" + inner + ") AS ROW_TABLE WHERE ROW_NUM >= " + str(start)
                + " AND ROW_NUM <= " + str(end))

    def getLikeSuffix(self):
        return "ESCAPE '\\' "

    def getPaging(self, offset, fetchLimit):
        raise NotImplementedError()

    def isLikeWildcard(self, value):
        escape = False
        for ch in value:
            if escape:
                escape = False
            else:
                if ch == '\\':
                    escape = True
                elif ch == '%' or ch == '_' or ch == '[':
                    return True
        return False


class _VerticaElSqlConfig(ElSqlConfig):
    def __init__(self):
        ElSqlConfig.__init__(self, "Vertica")


ElSqlConfig.DEFAULT = ElSqlConfig("Default")
ElSqlConfig.POSTGRES = _PostgresElSqlConfig()
ElSqlConfig.HSQL = _HsqlElSqlConfig()
ElSqlConfig.MYSQL = _MySqlElSqlConfig()
ElSqlConfig.ORACLE = _OracleElSqlConfig()
ElSqlConfig.SQL_SERVER_2008 = _SqlServer2008ElSqlConfig()
ElSqlConfig.VERTICA = _VerticaElSqlConfig()


# ---------------------------------------------------------------------------
# params
# ---------------------------------------------------------------------------
class SqlParams(object):

    def contains(self, variable):
        raise NotImplementedError()

    def get(self, variable):
        raise NotImplementedError()


class EmptySqlParams(SqlParams):

    INSTANCE = None

    def contains(self, variable):
        return False

    def get(self, variable):
        return None


EmptySqlParams.INSTANCE = EmptySqlParams()


class MapSqlParams(SqlParams):

    _NO_VALUE = object()

    def __init__(self, map_or_key, value=_NO_VALUE):
        if value is MapSqlParams._NO_VALUE:
            if map_or_key is None:
                raise ValueError("Map must not be null")
            self._map = map_or_key
        else:
            self._map = {map_or_key: value}

    def with_(self, key, value):
        new_map = dict(self._map)
        new_map[key] = value
        return MapSqlParams(new_map)

    def contains(self, variable):
        return variable in self._map

    def get(self, variable):
        return self._map.get(variable)


class MapSqlParameterSource(object):
    """Minimal equivalent of Spring's MapSqlParameterSource."""

    def __init__(self, map_or_name=None, value=None):
        self._values = {}
        if isinstance(map_or_name, dict):
            self._values.update(map_or_name)
        elif map_or_name is not None:
            self._values[map_or_name] = value

    def addValue(self, paramName, value):
        if paramName is None:
            raise ValueError("Parameter name must not be null")
        self._values[paramName] = value
        return self

    def addValues(self, values):
        if values is not None:
            self._values.update(values)
        return self

    def getValues(self):
        return dict(self._values)

    def hasValue(self, paramName):
        return paramName in self._values

    def getValue(self, paramName):
        if paramName not in self._values:
            raise ValueError("No value registered for key '" + _java_str(paramName) + "'")
        return self._values[paramName]


class SpringSqlParams(SqlParams):

    def __init__(self, source):
        if source is None:
            raise ValueError("Source must not be null")
        self._source = source

    def contains(self, variable):
        return self._source.hasValue(variable)

    def get(self, variable):
        return self._source.getValue(variable) if self._source.hasValue(variable) else None


# ---------------------------------------------------------------------------
# fragments
# ---------------------------------------------------------------------------
class SqlFragment(object):

    def toSQL(self, buf, fragments, params, loopIndex):
        raise NotImplementedError()

    def applyLoopIndex(self, text, loopIndex):
        result = text
        n = len(loopIndex)
        if n == 4:
            result = result.replace("@LOOPINDEX3", str(loopIndex[3]))
        if n in (3, 4):
            result = result.replace("@LOOPINDEX2", str(loopIndex[2]))
        if n in (2, 3, 4):
            result = result.replace("@LOOPINDEX1", str(loopIndex[1]))
        if n == 0:
            raise IndexError("Index -1 out of bounds for length 0")
        result = result.replace("@LOOPINDEX", str(loopIndex[n - 1]))
        return result

    @staticmethod
    def extractVariableName(variable):
        if variable is None or not variable.startswith(":") or len(variable) < 2:
            raise ValueError("Argument is not a variable (starting with a colon)")
        post_colon = variable[1:]
        if post_colon.startswith("{") and post_colon.endswith("}"):
            return post_colon[1:-1]
        return post_colon

    @staticmethod
    def extractVariableOrLiteral(params, text):
        if text is not None:
            if text.startswith(":") and len(text) > 1:
                name = SqlFragment.extractVariableName(text)
                if params.contains(name):
                    value = params.get(name)
                    if not _is_number(value):
                        raise TypeError("Value is not a Number: " + _java_str(value))
                    return int(value)
            elif re.fullmatch(r"[0-9]+", text) is not None:
                return _parse_int(text)
        return 0

    def __str__(self):
        return "%s@%x" % (type(self).__name__, id(self))

    def __repr__(self):
        return self.__str__()


class ContainerSqlFragment(SqlFragment):

    def __init__(self):
        self._fragments = []

    def _frags(self):
        # tolerate subclasses that do not call __init__
        if not hasattr(self, "_fragments"):
            self._fragments = []
        return self._fragments

    def addFragment(self, childFragment):
        self._frags().append(childFragment)

    def getFragments(self):
        return tuple(self._frags())

    def _fragments_str(self):
        return "[" + ", ".join(_java_str(f) for f in self._frags()) + "]"

    def toSQL(self, buf, fragments, params, loopIndex):
        for fragment in self._frags():
            fragment.toSQL(buf, fragments, params, loopIndex)

    def __str__(self):
        return self._fragments_str()


class NameSqlFragment(ContainerSqlFragment):

    def __init__(self, name):
        ContainerSqlFragment.__init__(self)
        if name is None:
            raise ValueError("Name must be specified")
        self._name = name

    def getName(self):
        return self._name

    def __str__(self):
        return type(self).__name__ + ":" + self._name + " " + self._fragments_str()


class TextSqlFragment(SqlFragment):

    def __init__(self, text, endOfLine):
        if text is None:
            raise ValueError("Text must be specified")
        if endOfLine:
            trimmed = _java_trim(text)
            self._text = "" if len(trimmed) == 0 else trimmed + " "
        else:
            self._text = text

    def toSQL(self, buf, fragments, params, loopIndex):
        buf.append(self.applyLoopIndex(self._text, loopIndex))

    def __str__(self):
        return type(self).__name__ + ":" + self._text


class ValueSqlFragment(SqlFragment):

    def __init__(self, valueVariable, followWithSpace):
        self._valueVariable = SqlFragment.extractVariableName(valueVariable)
        self._followWithSpace = followWithSpace

    def toSQL(self, buf, fragments, params, loopIndex):
        var = self.applyLoopIndex(self._valueVariable, loopIndex)
        value = params.get(var)
        if value is not None:
            buf.append(_java_str(value))
            if self._followWithSpace:
                buf.append(' ')

    def __str__(self):
        return type(self).__name__ + ":" + self._valueVariable


class IncludeSqlFragment(SqlFragment):

    def __init__(self, includeKey):
        if includeKey is None:
            raise ValueError("Include key must be specified")
        self._includeKey = includeKey

    def toSQL(self, buf, fragments, params, loopIndex):
        key = self._includeKey
        if key.startswith(":"):
            var = SqlFragment.extractVariableName(key)
            if params.contains(var):
                key = _java_str(params.get(var))
        unit = fragments.getFragment(key)
        unit.toSQL(buf, fragments, params, loopIndex)

    def __str__(self):
        return type(self).__name__ + ":" + self._includeKey


class ConditionalSqlFragment(ContainerSqlFragment):

    def __init__(self, variable, matchValue):
        ContainerSqlFragment.__init__(self)
        self._variable = SqlFragment.extractVariableName(variable)
        self._matchValue = matchValue

    def getVariable(self):
        return self._variable

    def getMatchValue(self):
        return self._matchValue

    def isMatch(self, params, loopIndex):
        var = self.applyLoopIndex(self._variable, loopIndex)
        if not params.contains(var):
            return False
        value = params.get(var)
        if value is None:
            return False
        if self._matchValue is not None:
            return self._matchValue.lower() == _java_str(value).lower()
        if isinstance(value, bool):
            return value
        return True

    def endsWith(self, buf, match):
        return _buf_ends_with(buf, match)

    def __str__(self):
        return type(self).__name__ + ":" + self._variable + " " + self._fragments_str()


class AndSqlFragment(ConditionalSqlFragment):

    def toSQL(self, buf, fragments, params, loopIndex):
        if self.isMatch(params, loopIndex):
            if not self.endsWith(buf, " WHERE ") and not self.endsWith(buf, " AND "):
                buf.append("AND ")
            ConditionalSqlFragment.toSQL(self, buf, fragments, params, loopIndex)


class OrSqlFragment(ConditionalSqlFragment):

    def toSQL(self, buf, fragments, params, loopIndex):
        if self.isMatch(params, loopIndex):
            if not self.endsWith(buf, " WHERE ") and not self.endsWith(buf, " OR "):
                buf.append("OR ")
            ConditionalSqlFragment.toSQL(self, buf, fragments, params, loopIndex)


class IfSqlFragment(ConditionalSqlFragment):

    def toSQL(self, buf, fragments, params, loopIndex):
        if self.isMatch(params, loopIndex):
            ConditionalSqlFragment.toSQL(self, buf, fragments, params, loopIndex)


class OperatorSqlFragment(ContainerSqlFragment):

    def __init__(self, variable):
        ContainerSqlFragment.__init__(self)
        self._variable = SqlFragment.extractVariableName(variable)

    def __str__(self):
        return type(self).__name__ + ":" + self._variable + " " + self._fragments_str()


class EqualsSqlFragment(OperatorSqlFragment):

    def toSQL(self, buf, fragments, params, loopIndex):
        var = self.applyLoopIndex(self._variable, loopIndex)
        val = params.get(var)
        if val is None:
            buf.append("IS NULL ")
        else:
            buf.append("= ")
            OperatorSqlFragment.toSQL(self, buf, fragments, params, loopIndex)


class LikeSqlFragment(OperatorSqlFragment):

    def toSQL(self, buf, fragments, params, loopIndex):
        var = self.applyLoopIndex(self._variable, loopIndex)
        val = params.get(var)
        if val is None:
            buf.append("IS NULL ")
        else:
            if fragments.getConfig().isLikeWildcard(_java_str(val)):
                buf.append("LIKE ")
                OperatorSqlFragment.toSQL(self, buf, fragments, params, loopIndex)
                buf.append(fragments.getConfig().getLikeSuffix())
            else:
                buf.append("= ")
                OperatorSqlFragment.toSQL(self, buf, fragments, params, loopIndex)


class LoopSqlFragment(ContainerSqlFragment):

    def __init__(self, variable):
        ContainerSqlFragment.__init__(self)
        self._sizeVariable = variable

    def toSQL(self, buf, fragments, params, loopIndex):
        size = self._extractSize(params)
        child_loop_index = list(loopIndex) + [0]
        for i in range(size):
            part = []
            child_loop_index[-1] = i
            ContainerSqlFragment.toSQL(self, part, fragments, params, child_loop_index)
            text = _buf_str(part)
            join_index = text.find("@LOOPJOIN ")
            if join_index >= 0:
                if i >= size - 1:
                    text = text[:join_index]
                else:
                    text = text[:join_index] + text[join_index + 10:]
            buf.append(text)

    def _extractSize(self, params):
        if self._sizeVariable.startswith(":"):
            var = SqlFragment.extractVariableName(self._sizeVariable)
            size_obj = params.get(var)
            if _is_number(size_obj):
                return int(size_obj)
            elif isinstance(size_obj, str):
                return _parse_int(size_obj)
            elif size_obj is None:
                raise ValueError("Loop size variable not found: " + var)
            else:
                raise ValueError("Loop size variable must be Number or String: " + var)
        return _parse_int(self._sizeVariable)

    def __str__(self):
        return type(self).__name__ + " " + self._fragments_str()


class OffsetFetchSqlFragment(ContainerSqlFragment):

    def __init__(self, *args):
        ContainerSqlFragment.__init__(self)
        if len(args) == 1:
            self._offsetVariable = None
            self._fetchVariable = args[0]
        elif len(args) == 2:
            self._offsetVariable = args[0]
            self._fetchVariable = args[1]
        else:
            raise TypeError("OffsetFetchSqlFragment takes 1 or 2 arguments")

    def toSQL(self, buf, fragments, params, loopIndex):
        offset = SqlFragment.extractVariableOrLiteral(params, self._offsetVariable)
        fetch_limit = SqlFragment.extractVariableOrLiteral(params, self._fetchVariable)
        buf.append(fragments.getConfig().getPaging(offset, 0 if fetch_limit == INTEGER_MAX_VALUE else fetch_limit))

    def __str__(self):
        return type(self).__name__ + " " + self._fragments_str()


class PagingSqlFragment(ContainerSqlFragment):

    def __init__(self, offsetVariable, fetchVariable):
        ContainerSqlFragment.__init__(self)
        self._offsetVariable = offsetVariable
        self._fetchVariable = fetchVariable

    def toSQL(self, buf, fragments, params, loopIndex):
        old_len = _buf_len(buf)
        ContainerSqlFragment.toSQL(self, buf, fragments, params, loopIndex)
        select = _buf_str(buf)[old_len:]
        if select.startswith("SELECT "):
            _buf_set_length(buf, old_len)
            buf.append(self.applyPaging(select, fragments, params))

    def applyPaging(self, selectToPage, fragments, params):
        offset = SqlFragment.extractVariableOrLiteral(params, self._offsetVariable)
        fetch_limit = SqlFragment.extractVariableOrLiteral(params, self._fetchVariable)
        return fragments.getConfig().addPaging(
            selectToPage, offset, 0 if fetch_limit == INTEGER_MAX_VALUE else fetch_limit)

    def __str__(self):
        return type(self).__name__ + " " + self._fragments_str()


class WhereSqlFragment(ContainerSqlFragment):

    def toSQL(self, buf, fragments, params, loopIndex):
        old_len = _buf_len(buf)
        buf.append("WHERE ")
        new_len = _buf_len(buf)
        ContainerSqlFragment.toSQL(self, buf, fragments, params, loopIndex)
        if _buf_len(buf) == new_len:
            _buf_set_length(buf, old_len)

    def __str__(self):
        return type(self).__name__ + " " + self._fragments_str()


# ---------------------------------------------------------------------------
# parser
# ---------------------------------------------------------------------------
_IDENTIFIER = "[A-Za-z0-9_]+"
_VARIABLE = "[:](?:[A-Za-z0-9_]+|[$]?[{][A-Za-z0-9_.]+[}])"
_VARIABLE_OR_LITERAL = "[0-9]+|" + _VARIABLE
_VARIABLE_LOOPINDEX = \
    "[:](?:[A-Za-z0-9_]+(?:@LOOPINDEX[123]?)?|[$]?[{][A-Za-z0-9_.]+(?:@LOOPINDEX[123]?)?[}])"
_QUERY_TEXT = "[A-Za-z0-9_]+"

_NAME_PATTERN = re.compile("[ ]*[@]NAME[(](" + _IDENTIFIER + ")[)][ ]*")
_AND_PATTERN = re.compile(
    "[ ]*[@]AND[(](" + _VARIABLE_LOOPINDEX + ")" + "([ ]?[=][ ]?" + _QUERY_TEXT + ")?" + "[)][ ]*")
_OR_PATTERN = re.compile(
    "[ ]*[@]OR[(](" + _VARIABLE_LOOPINDEX + ")" + "([ ]?[=][ ]?" + _QUERY_TEXT + ")?" + "[)][ ]*")
_IF_PATTERN = re.compile(
    "[ ]*[@]IF[(](" + _VARIABLE_LOOPINDEX + ")" + "([ ]?[=][ ]?" + _QUERY_TEXT + ")?" + "[)][ ]*")
_LOOP_PATTERN = re.compile("[ ]*[@]LOOP[(](" + _VARIABLE_OR_LITERAL + ")[)][ ]*")
_INCLUDE_PATTERN = re.compile("[@]INCLUDE[(](" + _VARIABLE + "|" + _IDENTIFIER + ")[)](.*)", re.S)
_PAGING_PATTERN = re.compile(
    "[@]PAGING[(](" + _VARIABLE_OR_LITERAL + ")[ ]?[,][ ]?(" + _VARIABLE_OR_LITERAL + ")[)](.*)")
_OFFSET_FETCH_PATTERN = re.compile(
    "[@]OFFSETFETCH[(](" + _VARIABLE_OR_LITERAL + ")[ ]?[,][ ]?(" + _VARIABLE_OR_LITERAL + ")[)](.*)")
_FETCH_PATTERN = re.compile("[@]FETCH[(](" + _VARIABLE_OR_LITERAL + ")[)](.*)")
_VALUE_PATTERN = re.compile("[@]VALUE[(](" + _VARIABLE_LOOPINDEX + ")[)]( )*(.*)")
_OPERATOR_VARIABLE_PATTERN = re.compile("([^:])*(" + _VARIABLE_LOOPINDEX + ")(.*)")


class _Line(object):

    def __init__(self, line, lineNumber, trimmed=None, endOfLine=True):
        self._line = line
        if trimmed is None:
            comment_pos = line.find("--")
            if comment_pos >= 0:
                trimmed = _java_trim(line[:comment_pos])
            else:
                trimmed = _java_trim(line)
        self._trimmed = trimmed
        self._lineNumber = lineNumber
        self._endOfLine = endOfLine

    def line(self):
        return self._line

    def lineTrimmed(self):
        return self._trimmed

    def lineNumber(self):
        return self._lineNumber

    def endOfLine(self):
        return self._endOfLine

    def containsTab(self):
        return "\t" in self._line

    def isComment(self):
        return self._trimmed.startswith("--") or len(self._trimmed) == 0

    def indent(self):
        for i, ch in enumerate(self._line):
            if ch != ' ':
                return i
        return len(self._line)

    def split(self, trimmedIndex):
        before = self._trimmed[:trimmedIndex]
        after = self._trimmed[trimmedIndex:]
        return [_Line(before, self._lineNumber, before, False),
                _Line(after, self._lineNumber, after, self._endOfLine)]

    def splitRemainder(self, trimmedIndex):
        after = self._trimmed[trimmedIndex:]
        return _Line(after, self._lineNumber, after, self._endOfLine)

    def __str__(self):
        return "Line " + str(self._lineNumber)


class _ListIterator(object):

    def __init__(self, items):
        self._items = items
        self._pos = 0

    def hasNext(self):
        return self._pos < len(self._items)

    def next(self):
        item = self._items[self._pos]
        self._pos += 1
        return item

    def previous(self):
        self._pos -= 1
        return self._items[self._pos]

    def remove(self):
        self._pos -= 1
        del self._items[self._pos]


class ElSqlParser(object):

    def __init__(self, lines):
        self._lines = []
        self._namedFragments = {}
        for i, line in enumerate(lines):
            self._lines.append(_Line(line, i + 1))

    def parse(self):
        self._rejectTabs()
        self._parseNamedSections()
        return self._namedFragments

    def _rejectTabs(self):
        for line in self._lines:
            if line.containsTab():
                raise ValueError("Tab character not permitted: " + str(line))

    def _parseNamedSections(self):
        container = ContainerSqlFragment()
        self._parseContainerSection(container, _ListIterator(self._lines), -1)

    def _parseConditional(self, container, it, line, trimmed, pattern, cls, tag):
        m = pattern.fullmatch(trimmed)
        if m is None:
            raise ValueError(tag + " found with invalid format: " + str(line))
        frag = cls(m.group(1), self._extractVariable(m.group(2)))
        self._parseContainerSection(frag, it, line.indent())
        if len(frag.getFragments()) == 0:
            raise ValueError(tag + " found with no subsequent indented lines: " + str(line))
        container.addFragment(frag)

    def _parseContainerSection(self, container, it, indent):
        while it.hasNext():
            line = it.next()
            if line.isComment():
                it.remove()
                continue
            if line.indent() <= indent:
                it.previous()
                return
            trimmed = line.lineTrimmed()
            if trimmed.startswith("@NAME"):
                m = _NAME_PATTERN.fullmatch(trimmed)
                if m is None:
                    raise ValueError("@NAME found with invalid format: " + str(line))
                name_fragment = NameSqlFragment(m.group(1))
                self._parseContainerSection(name_fragment, it, line.indent())
                if len(name_fragment.getFragments()) == 0:
                    raise ValueError("@NAME found with no subsequent indented lines: " + str(line))
                container.addFragment(name_fragment)
                self._namedFragments[name_fragment.getName()] = name_fragment
            elif indent < 0:
                raise ValueError("Invalid fragment found at root level, only @NAME is permitted: " + str(line))
            elif trimmed.startswith("@PAGING"):
                m = _PAGING_PATTERN.fullmatch(trimmed)
                if m is None:
                    raise ValueError("@PAGING found with invalid format: " + str(line))
                frag = PagingSqlFragment(m.group(1), m.group(2))
                self._parseContainerSection(frag, it, line.indent())
                if len(frag.getFragments()) == 0:
                    raise ValueError("@PAGING found with no subsequent indented lines: " + str(line))
                container.addFragment(frag)
            elif trimmed.startswith("@WHERE"):
                if trimmed != "@WHERE":
                    raise ValueError("@WHERE found with invalid format: " + str(line))
                frag = WhereSqlFragment()
                self._parseContainerSection(frag, it, line.indent())
                if len(frag.getFragments()) == 0:
                    raise ValueError("@WHERE found with no subsequent indented lines: " + str(line))
                container.addFragment(frag)
            elif trimmed.startswith("@AND"):
                self._parseConditional(container, it, line, trimmed, _AND_PATTERN, AndSqlFragment, "@AND")
            elif trimmed.startswith("@OR"):
                self._parseConditional(container, it, line, trimmed, _OR_PATTERN, OrSqlFragment, "@OR")
            elif trimmed.startswith("@IF"):
                self._parseConditional(container, it, line, trimmed, _IF_PATTERN, IfSqlFragment, "@IF")
            elif trimmed.startswith("@LOOP"):
                if trimmed.startswith("@LOOPINDEX") or trimmed.startswith("@LOOPJOIN"):
                    self._parseLine(container, line)
                else:
                    m = _LOOP_PATTERN.fullmatch(trimmed)
                    if m is None:
                        raise ValueError("@LOOP found with invalid format: " + str(line))
                    frag = LoopSqlFragment(m.group(1))
                    self._parseContainerSection(frag, it, line.indent())
                    if len(frag.getFragments()) == 0:
                        raise ValueError("@LOOP found with no subsequent indented lines: " + str(line))
                    container.addFragment(frag)
            else:
                self._parseLine(container, line)

    def _extractVariable(self, text):
        if text is None:
            return None
        trimmed = _java_trim(text)
        if trimmed.startswith("="):
            return self._extractVariable(trimmed[1:])
        return trimmed

    def _parseLine(self, container, line):
        trimmed = line.lineTrimmed()
        if len(trimmed) == 0:
            return
        if "@INCLUDE" in trimmed:
            self._parseIncludeTag(container, line)
        elif "@LIKE" in trimmed:
            self._parseOperatorTag(container, line, "@LIKE")
        elif "@EQUALS" in trimmed:
            self._parseOperatorTag(container, line, "@EQUALS")
        elif "@OFFSETFETCH" in trimmed:
            self._parseOffsetFetchTag(container, line)
        elif "@FETCH" in trimmed:
            self._parseFetchTag(container, line)
        elif "@VALUE" in trimmed:
            self._parseValueTag(container, line)
        elif "@LOOPJOIN" in trimmed:
            container.addFragment(TextSqlFragment(trimmed, line.endOfLine()))
        elif trimmed.startswith("@"):
            raise ValueError("Unknown tag at start of line: " + str(line))
        else:
            container.addFragment(TextSqlFragment(trimmed, line.endOfLine()))

    def _parseIncludeTag(self, container, line):
        split = line.split(line.lineTrimmed().find("@INCLUDE"))
        self._parseLine(container, split[0])
        trimmed = split[1].lineTrimmed()
        m = _INCLUDE_PATTERN.fullmatch(trimmed)
        if m is None:
            raise ValueError("@INCLUDE found with invalid format: " + str(line))
        container.addFragment(IncludeSqlFragment(m.group(1)))
        self._parseLine(container, split[1].splitRemainder(m.start(2)))

    def _parseOperatorTag(self, container, line, tagName):
        split = line.split(line.lineTrimmed().find(tagName))
        self._parseLine(container, split[0])
        trimmed = split[1].lineTrimmed()
        content = trimmed[len(tagName):]
        end_tag = "@END" + tagName[1:]
        end = trimmed.find(end_tag)
        remainder_index = len(trimmed)
        if end >= 0:
            content = trimmed[len(tagName):end]
            remainder_index = end + len(end_tag)
        content_fragment = TextSqlFragment(content, line.endOfLine())
        m = _OPERATOR_VARIABLE_PATTERN.fullmatch(content)
        if m is None:
            raise ValueError(tagName + " found with invalid format: " + str(line))
        variable = m.group(2)
        operator = LikeSqlFragment(variable) if tagName == "@LIKE" else EqualsSqlFragment(variable)
        container.addFragment(operator)
        operator.addFragment(content_fragment)
        self._parseLine(container, split[1].splitRemainder(remainder_index))

    def _parseOffsetFetchTag(self, container, line):
        split = line.split(line.lineTrimmed().find("@OFFSETFETCH"))
        self._parseLine(container, split[0])
        trimmed = split[1].lineTrimmed()
        offset_variable = ":paging_offset"
        fetch_variable = ":paging_fetch"
        remainder_index = 12
        if trimmed.startswith("@OFFSETFETCH("):
            m = _OFFSET_FETCH_PATTERN.fullmatch(trimmed)
            if m is None:
                raise ValueError("@OFFSETFETCH found with invalid format: " + str(line))
            offset_variable = m.group(1)
            fetch_variable = m.group(2)
            remainder_index = m.start(3)
        container.addFragment(OffsetFetchSqlFragment(offset_variable, fetch_variable))
        self._parseLine(container, split[1].splitRemainder(remainder_index))

    def _parseFetchTag(self, container, line):
        split = line.split(line.lineTrimmed().find("@FETCH"))
        self._parseLine(container, split[0])
        trimmed = split[1].lineTrimmed()
        fetch_variable = ":paging_fetch"
        remainder_index = 6
        if trimmed.startswith("@FETCH("):
            m = _FETCH_PATTERN.fullmatch(trimmed)
            if m is not None:
                fetch_variable = m.group(1)
                remainder_index = m.start(2)
            else:
                raise ValueError("@FETCH found with invalid format: " + str(line))
        container.addFragment(OffsetFetchSqlFragment(fetch_variable))
        self._parseLine(container, split[1].splitRemainder(remainder_index))

    def _parseValueTag(self, container, line):
        split = line.split(line.lineTrimmed().find("@VALUE"))
        self._parseLine(container, split[0])
        line_at_tag = split[1]
        m = _VALUE_PATTERN.fullmatch(line_at_tag.lineTrimmed())
        if m is None:
            raise ValueError("@VALUE found with invalid format: " + str(line))
        following_spaces = m.group(2)
        sub_line = line_at_tag.splitRemainder(m.start(3))
        follow_with_space = (following_spaces is not None and len(following_spaces) > 0) \
            or len(sub_line.lineTrimmed()) == 0
        container.addFragment(ValueSqlFragment(m.group(1), follow_with_space))
        self._parseLine(container, sub_line)


# ---------------------------------------------------------------------------
# SqlFragments
# ---------------------------------------------------------------------------
def _resource_path(resource):
    """Resolve a resource (path, URL-like or object with a name/path) to a file path, or None."""
    if resource is None:
        return None
    if isinstance(resource, (str, bytes, os.PathLike)):
        return os.fsdecode(resource)
    for attr in ("path", "name"):
        value = getattr(resource, attr, None)
        if isinstance(value, (str, os.PathLike)):
            return os.fsdecode(value)
    return None


def _resource_exists(resource):
    if resource is None:
        return False
    exists = getattr(resource, "exists", None)
    if callable(exists):
        return bool(exists())
    path = _resource_path(resource)
    return path is not None and os.path.isfile(path)


class SqlFragments(object):

    NO_LOOP = [-1]
    _MISSING = object()

    @staticmethod
    def parseResource(resources, config):
        files = []
        resource_found = False
        for resource in resources:
            if _resource_exists(resource):
                resource_found = True
                files.append(SqlFragments.loadResource(resource))
        if not resource_found:
            raise ValueError("No matching resource was found")
        return SqlFragments.parse(files, config)

    @staticmethod
    def loadResource(resource):
        path = _resource_path(resource)
        with open(path, "r", encoding="utf-8", newline=None) as f:
            return f.read().splitlines()

    @staticmethod
    def parse(files_or_lines, config=_MISSING):
        if config is SqlFragments._MISSING:
            # parse(List<String> lines)
            return SqlFragments.parse([files_or_lines], ElSqlConfig.DEFAULT)
        # parse(List<List<String>> files, ElSqlConfig config)
        if not isinstance(files_or_lines, (list, tuple)):
            raise TypeError("files must be a list of lists of lines")
        parsed = {}
        for lines in files_or_lines:
            parsed.update(ElSqlParser(lines).parse())
        return SqlFragments(parsed, config)

    def __init__(self, map, config):
        if map is None:
            raise ValueError("Fragment map must not be null")
        if config is None:
            raise ValueError("Config must not be null")
        self._map = map
        self._config = config

    def getConfig(self):
        return self._config

    def withConfig(self, config):
        return SqlFragments(self._map, config)

    def getSql(self, name, params):
        if name is None:
            raise ValueError("Fragment name must not be null")
        if params is None:
            raise ValueError("SqlParams must not be null")
        fragment = self.getFragment(name)
        buf = []
        fragment.toSQL(buf, self, params, SqlFragments.NO_LOOP)
        return "".join(buf)

    def getFragment(self, name):
        if name is None:
            raise ValueError("Fragment name must not be null")
        fragment = self._map.get(name)
        if fragment is None:
            raise ValueError("Unknown fragment name: " + name)
        return fragment


# ---------------------------------------------------------------------------
# entry points
# ---------------------------------------------------------------------------
def _type_resource(type_, filename):
    """Equivalent of Class.getResource(relativeName): file next to the type's module, or None."""
    module = sys.modules.get(getattr(type_, "__module__", None))
    module_file = getattr(module, "__file__", None)
    if module_file is None:
        return None
    path = os.path.join(os.path.dirname(os.path.abspath(module_file)), filename)
    return path if os.path.isfile(path) else None


class ClassPathResource(object):
    """Minimal equivalent of Spring's ClassPathResource relative to a type."""

    def __init__(self, path, type_=None):
        self._name = path
        if type_ is not None:
            module = sys.modules.get(getattr(type_, "__module__", None))
            module_file = getattr(module, "__file__", None)
            base = os.path.dirname(os.path.abspath(module_file)) if module_file else os.getcwd()
            self.path = os.path.join(base, path)
        else:
            self.path = path

    def exists(self):
        return os.path.isfile(self.path)

    def getURL(self):
        return self.path


class ElSql(object):

    @staticmethod
    def of(config, type_):
        if config is None:
            raise ValueError("Config must not be null")
        if type_ is None:
            raise ValueError("Type must not be null")
        base = _type_resource(type_, type_.__name__ + ".elsql")
        cfg = _type_resource(type_, type_.__name__ + "-" + config.getName() + ".elsql")
        return ElSql.parse(config, base, cfg)

    @staticmethod
    def parse(config, *resources):
        if config is None:
            raise ValueError("Config must not be null")
        if len(resources) == 1 and (resources[0] is None or isinstance(resources[0], (list, tuple))):
            resources = resources[0]  # array passed directly
        if resources is None:
            raise ValueError("Resources must not be null")
        return ElSql(SqlFragments.parseResource(resources, config))

    def __init__(self, fragments):
        if fragments is None:
            raise ValueError("Fragment map must not be null")
        self._fragments = fragments

    def getConfig(self):
        return self._fragments.getConfig()

    def withConfig(self, config):
        return ElSql(self._fragments.withConfig(config))

    def getSql(self, name, params=None):
        if params is None:
            return self._fragments.getSql(name, EmptySqlParams.INSTANCE)
        if isinstance(params, dict):
            return self._fragments.getSql(name, MapSqlParams(params))
        return self._fragments.getSql(name, params)


class ElSqlBundle(object):

    @staticmethod
    def of(config, type_):
        if config is None:
            raise ValueError("Config must not be null")
        if type_ is None:
            raise ValueError("Type must not be null")
        base = ClassPathResource(type_.__name__ + ".elsql", type_)
        cfg = ClassPathResource(type_.__name__ + "-" + config.getName() + ".elsql", type_)
        return ElSqlBundle.parse(config, base, cfg)

    @staticmethod
    def parse(config, *resources):
        if config is None:
            raise ValueError("Config must not be null")
        if len(resources) == 1 and (resources[0] is None or isinstance(resources[0], (list, tuple))):
            resources = resources[0]
        if resources is None:
            raise ValueError("Resources must not be null")
        files = []
        resource_found = False
        for resource in resources:
            if _resource_exists(resource):
                resource_found = True
                files.append(SqlFragments.loadResource(resource))
        if not resource_found:
            raise ValueError("No matching resource was found")
        return ElSqlBundle(SqlFragments.parse(files, config))

    def __init__(self, fragments):
        if fragments is None:
            raise ValueError("Fragment map must not be null")
        self._fragments = fragments

    def getConfig(self):
        return self._fragments.getConfig()

    def withConfig(self, config):
        return ElSqlBundle(self._fragments.withConfig(config))

    def getSql(self, name, paramSource=None):
        if paramSource is None:
            return self._fragments.getSql(name, EmptySqlParams.INSTANCE)
        return self._fragments.getSql(name, SpringSqlParams(paramSource))
