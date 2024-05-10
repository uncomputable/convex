# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import argparse
import re
import sys
import unittest
from typing import List, Optional


def as_list(element: str, delimiter: str) -> str:
    return r"(\s*" + element + r"\s*)(" + delimiter + r"\s*" + element + r"\s*)*"


def is_string(string: str) -> bool:
    pattern = r"(0x)?([0-9a-f]{2})*"
    return bool(re.fullmatch(pattern, string))


def is_c(string: str) -> bool:
    pattern = as_list(r"0x[0-9a-f]{8}u", r",")
    return bool(re.fullmatch(pattern, string))


def is_coq(string: str) -> bool:
    pattern = as_list(r"[0-9]{1,3}%Z", r";")
    return bool(re.fullmatch(pattern, string))


def is_rust(string: str) -> bool:
    pattern = as_list(r"0x[0-9a-f]{2}", r",")
    return bool(re.fullmatch(pattern, string))


def is_json(string: str) -> bool:
    pattern = as_list(r"[0-9]{1,3}", r",")
    return bool(re.fullmatch(pattern, string))


def parse_string(string: str) -> Optional[List[int]]:
    hex_string = string \
        .removeprefix("0x") \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("[", "") \
        .replace("]", "") \
        .replace("{", "") \
        .replace("}", "")
    if not is_string(hex_string):
        return None
    hex_strings = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    return [int(s, 16) for s in hex_strings if s]


def parse_c(string: str) -> Optional[List[int]]:
    string = string \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("[", "") \
        .replace("]", "") \
        .replace("{", "") \
        .replace("}", "")
    if not is_c(string):
        return None
    four_hex_strings = string.split(",")
    hex_strings = [s[2:-1][i:i+2] for s in four_hex_strings for i in range(0, 8, 2)]
    return [int(s, 16) for s in hex_strings if s]


def parse_coq(string: str) -> Optional[List[int]]:
    string = string \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("[", "") \
        .replace("]", "") \
        .replace("{", "") \
        .replace("}", "") \
        .replace("%Z", "")
    if not is_coq(string):
        return None
    hex_strings = string.split(";")
    return [int(s) for s in hex_strings if s]


def parse_rust(string: str) -> Optional[List[int]]:
    string = string \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("[", "") \
        .replace("]", "") \
        .replace("{", "") \
        .replace("}", "")
    if not is_rust(string):
        return None
    hex_strings = string.split(",")
    return [int(s[2:], 16) for s in hex_strings if s]


def parse_json(string: str) -> Optional[List[int]]:
    string = string \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("[", "") \
        .replace("]", "") \
        .replace("{", "") \
        .replace("}", "")
    if not is_json(string):
        return None
    hex_strings = string.split(",")
    return [int(s) for s in hex_strings if s]


def parse_auto(string: str) -> Optional[List[int]]:
    if is_c(string):
        return parse_c(string)
    if is_coq(string):
        return parse_coq(string)
    if is_rust(string):
        return parse_rust(string)
    if is_json(string):
        return parse_json(string)
    return parse_string(string)


def format_string(lst: List[int]) -> str:
    return "".join([f"{x:02x}" for x in lst])


def format_c(lst: List[int]) -> str:
    four_int_values = [(lst[i], lst[i+1], lst[i+2], lst[i+3]) for i in range(0, len(lst), 4)]
    return ", ".join([f"0x{a:02x}{b:02x}{c:02x}{d:02x}u" for (a, b, c, d) in four_int_values])


def format_coq(lst: List[int]) -> str:
    return "; ".join([f"{x}%Z" for x in lst])


def format_rust(lst: List[int]) -> str:
    return ", ".join([f"0x{x:02x}" for x in lst])


def format_json(lst: List[int]) -> str:
    return ", ".join([f"{x}" for x in lst])


def main():
    parser = argparse.ArgumentParser(
        description="Convert between different hex representations",
        epilog="""String: ...89ab... (default)
        C: ... 0x89ab...
        Coq: ... 137%Z; 171%Z; ...
        Rust: ... 0x89, 0xab, ...
        JSON: ... 137, 171, ..."""
    )
    parser.add_argument("input", help="input string")
    parser.add_argument("-r", "--reverse", action="store_true", help="reverse byte order")
    from_group = parser.add_mutually_exclusive_group()
    from_group.add_argument("--from-c",    action="store_true", help="Read C")
    from_group.add_argument("--from-coq",  action="store_true", help="Read Coq")
    from_group.add_argument("--from-rust", action="store_true", help="Read Rust")
    from_group.add_argument("--from-json", action="store_true", help="Read JSON")
    to_group = parser.add_mutually_exclusive_group()
    to_group.add_argument("--to-c", action="store_true", help="Write C")
    to_group.add_argument("--to-coq", action="store_true", help="Write Coq")
    to_group.add_argument("--to-rust",   action="store_true", help="Write Rust")
    to_group.add_argument("--to-json",   action="store_true", help="Write JSON")

    args = parser.parse_args()

    # Parse input
    if args.from_rust:
        lst = parse_rust(args.input)
    elif args.from_coq:
        lst = parse_coq(args.input)
    elif args.from_json:
        lst = parse_json(args.input)
    elif args.from_c:
        lst = parse_c(args.input)
    else:
        lst = parse_auto(args.input)

    if lst is None:
        sys.stderr.write("Error: Failed to parse input string\n")
        sys.exit(1)

    if args.reverse:
        lst = list(reversed(lst))

    # Format output
    if args.to_rust:
        output = format_rust(lst)
    elif args.to_coq:
        output = format_coq(lst)
    elif args.to_json:
        output = format_json(lst)
    elif args.to_c:
        output = format_c(lst)
    else:
        output = format_string(lst)

    print(output)


if __name__ == "__main__":
    main()


class TestConvex(unittest.TestCase):
    # pylint: disable=line-too-long
    LIST = [32, 149, 119, 189, 166, 191, 75, 88, 4, 189, 70, 248, 98, 21, 128, 221, 109, 78, 139, 250, 45, 25, 14, 28, 80, 233, 50, 73, 43, 172, 160, 125]
    STRING = "209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d"
    C = "0x209577bdu, 0xa6bf4b58u, 0x04bd46f8u, 0x621580ddu, 0x6d4e8bfau, 0x2d190e1cu, 0x50e93249u, 0x2baca07du"
    COQ = "32%Z; 149%Z; 119%Z; 189%Z; 166%Z; 191%Z; 75%Z; 88%Z; 4%Z; 189%Z; 70%Z; 248%Z; 98%Z; 21%Z; 128%Z; 221%Z; 109%Z; 78%Z; 139%Z; 250%Z; 45%Z; 25%Z; 14%Z; 28%Z; 80%Z; 233%Z; 50%Z; 73%Z; 43%Z; 172%Z; 160%Z; 125%Z"
    RUST = "0x20, 0x95, 0x77, 0xbd, 0xa6, 0xbf, 0x4b, 0x58, 0x04, 0xbd, 0x46, 0xf8, 0x62, 0x15, 0x80, 0xdd, 0x6d, 0x4e, 0x8b, 0xfa, 0x2d, 0x19, 0x0e, 0x1c, 0x50, 0xe9, 0x32, 0x49, 0x2b, 0xac, 0xa0, 0x7d"
    JSON = "32, 149, 119, 189, 166, 191, 75, 88, 4, 189, 70, 248, 98, 21, 128, 221, 109, 78, 139, 250, 45, 25, 14, 28, 80, 233, 50, 73, 43, 172, 160, 125"
    # pylint: enable=line-too-long

    def test_is_string(self):
        self.assertTrue(is_string(self.STRING))
        self.assertFalse(is_string(self.C))
        self.assertFalse(is_string(self.COQ))
        self.assertFalse(is_string(self.RUST))
        self.assertFalse(is_string(self.JSON))

    def test_is_c(self):
        self.assertFalse(is_c(self.STRING))
        self.assertTrue(is_c(self.C))
        self.assertFalse(is_c(self.COQ))
        self.assertFalse(is_c(self.RUST))
        self.assertFalse(is_c(self.JSON))

    def test_is_coq(self):
        self.assertFalse(is_coq(self.STRING))
        self.assertFalse(is_coq(self.C))
        self.assertTrue(is_coq(self.COQ))
        self.assertFalse(is_coq(self.RUST))
        self.assertFalse(is_coq(self.JSON))

    def test_is_rust(self):
        self.assertFalse(is_rust(self.STRING))
        self.assertFalse(is_rust(self.C))
        self.assertFalse(is_rust(self.COQ))
        self.assertTrue(is_rust(self.RUST))
        self.assertFalse(is_rust(self.JSON))

    def test_is_json(self):
        self.assertFalse(is_json(self.STRING))
        self.assertFalse(is_json(self.C))
        self.assertFalse(is_json(self.COQ))
        self.assertFalse(is_json(self.RUST))
        self.assertTrue(is_json(self.JSON))

    def test_parse_string(self):
        self.assertEqual(self.LIST, parse_string(self.STRING))

    def test_parse_c(self):
        self.assertEqual(self.LIST, parse_c(self.C))

    def test_parse_coq(self):
        self.assertEqual(self.LIST, parse_coq(self.COQ))

    def test_parse_rust(self):
        self.assertEqual(self.LIST, parse_rust(self.RUST))

    def test_parse_json(self):
        self.assertEqual(self.LIST, parse_json(self.JSON))

    def test_format_string(self):
        self.assertEqual(self.STRING, format_string(self.LIST))

    def test_format_c(self):
        self.assertEqual(self.C, format_c(self.LIST))

    def test_format_coq(self):
        self.assertEqual(self.COQ, format_coq(self.LIST))

    def test_format_rust(self):
        self.assertEqual(self.RUST, format_rust(self.LIST))

    def test_format_json(self):
        self.assertEqual(self.JSON, format_json(self.LIST))
