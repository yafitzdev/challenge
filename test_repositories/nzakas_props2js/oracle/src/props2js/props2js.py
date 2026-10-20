"""Port of net.nczonline.web.props2js.Props2Js (command line runner)."""
import os
import sys
import traceback

from . import property_converter as PropertyConverter


class Props2JsExit(SystemExit, Exception):
    """Raised where the Java code calls System.exit(code).

    It is a SystemExit (so running as a script terminates with the code) and also an
    Exception, mirroring how System.exit surfaces as a SecurityException when the JVM
    forbids exiting (the situation the Java tests are written for).
    """


def _exit(code):
    raise Props2JsExit(code)


class OptionException(Exception):
    """Equivalent of jargs CmdLineParser.OptionException."""


# ---------------------------------------------------------------------------
# java.util.Properties.load(Reader) port
# ---------------------------------------------------------------------------
class Properties(dict):
    def get_property(self, key):
        return self.get(key)

    getProperty = get_property

    def load(self, text):
        for key, value in _parse_properties(text):
            self[key] = value


def _logical_lines(text):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].lstrip(" \t\f")
        i += 1
        if line == "" or line[0] in "#!":
            continue
        # handle continuation lines (odd number of trailing backslashes)
        while True:
            bs = len(line) - len(line.rstrip("\\"))
            if bs % 2 == 1:
                line = line[:-1]
                if i < n:
                    line += lines[i].lstrip(" \t\f")
                    i += 1
                else:
                    break
            else:
                break
        yield line


def _unescape(s):
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        i += 1
        if c == "\\" and i < n:
            c = s[i]
            i += 1
            if c == "u":
                hexs = s[i:i + 4]
                if len(hexs) < 4 or any(h not in "0123456789abcdefABCDEF" for h in hexs):
                    raise ValueError("Malformed \\uxxxx encoding.")
                out.append(chr(int(hexs, 16)))
                i += 4
            elif c == "t":
                out.append("\t")
            elif c == "r":
                out.append("\r")
            elif c == "n":
                out.append("\n")
            elif c == "f":
                out.append("\f")
            else:
                out.append(c)
        elif c == "\\":
            # trailing lone backslash is dropped
            pass
        else:
            out.append(c)
    return "".join(out)


def _parse_properties(text):
    for line in _logical_lines(text):
        n = len(line)
        key_len = 0
        value_start = n
        has_sep = False
        preceding_backslash = False
        while key_len < n:
            c = line[key_len]
            if (c == "=" or c == ":") and not preceding_backslash:
                value_start = key_len + 1
                has_sep = True
                break
            elif c in " \t\f" and not preceding_backslash:
                value_start = key_len + 1
                break
            preceding_backslash = (not preceding_backslash) if c == "\\" else False
            key_len += 1
        while value_start < n:
            c = line[value_start]
            if c not in " \t\f":
                if not has_sep and (c == "=" or c == ":"):
                    has_sep = True
                else:
                    break
            value_start += 1
        yield _unescape(line[:key_len]), _unescape(line[value_start:])


# ---------------------------------------------------------------------------
# minimal jargs CmdLineParser port
# ---------------------------------------------------------------------------
class _Option:
    def __init__(self, short, long, wants_value):
        self.short = short
        self.long = long
        self.wants_value = wants_value


class CmdLineParser:
    def __init__(self):
        self._options = {}
        self._values = {}
        self._remaining = []

    def _add(self, short, long, wants_value):
        opt = _Option(short, long, wants_value)
        self._options["-" + short] = opt
        self._options["--" + long] = opt
        return opt

    def add_boolean_option(self, short, long):
        return self._add(short, long, False)

    def add_string_option(self, short, long):
        return self._add(short, long, True)

    def parse(self, args):
        self._values = {}
        remaining = []
        i = 0
        args = list(args)
        while i < len(args):
            cur = args[i]
            if cur.startswith("-"):
                if cur == "--":
                    remaining.extend(args[i + 1:])
                    break
                value = None
                if cur.startswith("--") and "=" in cur:
                    cur, value = cur.split("=", 1)
                elif not cur.startswith("--") and len(cur) > 2:
                    # combined short boolean options, e.g. -vh
                    for ch in cur[1:]:
                        opt = self._options.get("-" + ch)
                        if opt is None or opt.wants_value:
                            raise OptionException("Unknown option '%s'" % cur)
                        self._values[opt] = True
                    i += 1
                    continue
                opt = self._options.get(cur)
                if opt is None:
                    raise OptionException("Unknown option '%s'" % cur)
                if opt.wants_value:
                    if value is None:
                        i += 1
                        if i >= len(args):
                            raise OptionException("Illegal value for option '%s'" % cur)
                        value = args[i]
                    self._values[opt] = value
                else:
                    self._values[opt] = True
            else:
                remaining.append(cur)
            i += 1
        self._remaining = remaining

    def get_option_value(self, opt):
        return self._values.get(opt)

    def get_remaining_args(self):
        return list(self._remaining)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(args=None):
    if args is None:
        args = sys.argv[1:]

    verbose = False
    output_filename = None
    out = None
    buffer = []
    infile = None

    parser = CmdLineParser()
    verbose_opt = parser.add_boolean_option("v", "verbose")
    help_opt = parser.add_boolean_option("h", "help")
    output_filename_opt = parser.add_string_option("o", "output")
    name_opt = parser.add_string_option("n", "name")
    output_type_opt = parser.add_string_option("t", "to")

    try:
        try:
            parser.parse(args)

            help_ = parser.get_option_value(help_opt)
            if help_:
                usage()
                _exit(0)

            verbose = parser.get_option_value(verbose_opt) is not None

            file_args = parser.get_remaining_args()
            if len(file_args) == 0:
                # Java indexes fileArgs[0] before its length check -> ArrayIndexOutOfBoundsException
                raise IndexError("Index 0 out of bounds for length 0")
            input_filename = file_args[0]

            infile = open(input_filename, "r", encoding="utf-8")
            properties = Properties()
            properties.load(infile.read())

            output_type = parser.get_option_value(output_type_opt)
            if output_type is None:
                output_type = "json"
                if verbose:
                    sys.stderr.write("[INFO] No output type specified, defaulting to json.\n")
            else:
                if verbose:
                    sys.stderr.write("[INFO] Output type set to " + output_type + ".\n")

            output_filename = parser.get_option_value(output_filename_opt)
            if output_filename is None:
                if verbose:
                    sys.stderr.write("[INFO] No output file specified, defaulting to stdout.\n")
                out = "stdout"
            else:
                if verbose:
                    sys.stderr.write("[INFO] Output file is '" + os.path.abspath(output_filename) + "'\n")
                out = "buffer"

            name = parser.get_option_value(name_opt)
            if name is None and output_type.lower() != "json":
                raise Exception("Missing --name option.")

            if output_type.lower() == "js":
                result = PropertyConverter.convert_to_javascript(properties, name)
            elif output_type.lower() == "jsonp":
                result = PropertyConverter.convert_to_jsonp(properties, name)
            else:
                result = PropertyConverter.convert_to_json(properties)

            if out == "stdout":
                sys.stdout.write(result)
            else:
                buffer.append(result)

        except OptionException:
            usage()
            _exit(1)
        except Props2JsExit:
            raise
        except Exception as e:
            sys.stderr.write("[ERROR] " + str(e) + "\n")
            if verbose:
                traceback.print_exc()
            _exit(1)
    finally:
        if out is not None:
            try:
                if out == "stdout":
                    sys.stdout.flush()
                data = "".join(buffer)
                if len(data) > 0:
                    with open(output_filename, "w", encoding="utf-8", newline="") as f:
                        f.write(data)
            except IOError as e:
                sys.stderr.write("[ERROR] " + str(e) + "\n")
                if verbose:
                    traceback.print_exc()
        if infile is not None:
            try:
                infile.close()
            except IOError as e:
                sys.stderr.write("[ERROR] " + str(e) + "\n")


def usage():
    print(
        "\nUsage: java -jar props2js-x.y.z.jar [options] [input file]\n\n"
        "Global Options\n"
        "  -h, --help            Displays this information.\n"
        "  -v, --verbose         Display informational messages and warnings.\n"
        "  --name <name>         The variable/callback name.\n"
        "  --to <format>         The output format: json (default), jsonp, or js.\n"
        "  -o <file>             Place the output into <file>. Defaults to stdout."
    )


if __name__ == "__main__":
    main()
