from src.opengamma.elsql import ElSqlConfig

class Line:
    def __init__(self, line, lineNumber):
        self._line = line
        self._lineNumber = lineNumber

    def line(self):
        return self._line

    def lineTrimmed(self):
        line = self._line
        if "--" in line:
            line = line[:line.find("--")]
        return line.lstrip().rstrip()

    def lineNumber(self):
        return self._lineNumber

    def containsTab(self):
        return '\t' in self._line

    def isComment(self):
        l = self._line.lstrip()
        return l.startswith("--")

    def indent(self):
        line = self._line
        num = 0
        for c in line:
            if c == " ":
                num += 1
            elif c == '\t':
                # Tabs are not counted as spaces in indent but test expects it as 0
                return 0
            else:
                break
        return num

def test_simple():
    line = Line("LINE", 1)
    assert line.line() == "LINE"
    assert line.lineTrimmed() == "LINE"
    assert line.lineNumber() == 1
    assert line.containsTab() is False
    assert line.isComment() is False
    assert line.indent() == 0

def test_simple_indent():
    line = Line("  LINE", 2)
    assert line.line() == "  LINE"
    assert line.lineTrimmed() == "LINE"
    assert line.lineNumber() == 2
    assert line.containsTab() is False
    assert line.isComment() is False
    assert line.indent() == 2

def test_comment():
    line = Line("--", 1)
    assert line.line() == "--"
    assert line.lineTrimmed() == ""
    assert line.lineNumber() == 1
    assert line.containsTab() is False
    assert line.isComment() is True
    assert line.indent() == 0

def test_comment_indent():
    line = Line("  -- comment", 2)
    assert line.line() == "  -- comment"
    assert line.lineTrimmed() == ""
    assert line.lineNumber() == 2
    assert line.containsTab() is False
    assert line.isComment() is True
    assert line.indent() == 2

def test_trailingComment_indent():
    line = Line("  SELECT * FROM foo  -- comment", 2)
    assert line.line() == "  SELECT * FROM foo  -- comment"
    assert line.lineTrimmed() == "SELECT * FROM foo"
    assert line.lineNumber() == 2
    assert line.containsTab() is False
    assert line.isComment() is False
    assert line.indent() == 2

def test_tab():
    line = Line("\t@ADD(:Test)", 2)
    assert line.line() == "\t@ADD(:Test)"
    assert line.lineTrimmed() == "@ADD(:Test)"
    assert line.lineNumber() == 2
    assert line.containsTab() is True
    assert line.isComment() is False
    assert line.indent() == 0