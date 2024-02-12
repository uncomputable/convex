import argparse
import re
import sys
from typing import List, Optional


def is_string(string: str) -> bool:
    return bool(re.match(r"^(\s*[0-9a-f]{2}\s*)*$", string))


def is_c(string: str) -> bool:
    return bool(re.match(r"^(\s*0x[0-9a-f]{8}u\s*)(,\s*0x[0-9a-f]{8}u\s*)*$", string))


def is_coq(string: str) -> bool:
    return bool(re.match(r"^(\s*[0-9]{1,3}%Z\s*)(;\s*[0-9]{1,3}%Z\s*)*$", string))


def is_rust(string: str) -> bool:
    return bool(re.match(r"^(\s*0x[0-9a-f]{2}\s*)(,\s*0x[0-9a-f]{2}\s*)*$", string))


def is_json(string: str) -> bool:
    return bool(re.match(r"^(\s*[0-9]{1,3}\s*)(,\s*[0-9]{1,3}\s*)*$", string))


def parse_string(string: str) -> List[int]:
    """
    209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d
    """
    hex_string = string \
        .replace("\n", "") \
        .replace(" ", "")
    hex_strings = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    return [int(s, 16) for s in hex_strings if s]


def parse_c(c: str) -> List[int]:
    """
    0x209577bdu, 0xa6bf4b58u, 0x04bd46f8u, 0x621580ddu, 0x6d4e8bfau, 0x2d190e1cu, 0x50e93249u, 0x2baca07du
    """
    four_hex_strings = c \
        .replace("\n", "") \
        .replace(" ", "") \
        .split(",")
    hex_strings = [s[2:-1][i:i+2] for s in four_hex_strings for i in range(0, 8, 2)]
    return [int(s, 16) for s in hex_strings if s]


def parse_coq(coq: str) -> List[int]:
    """
    32%Z; 149%Z; 119%Z; 189%Z; 166%Z; 191%Z; 75%Z; 88%Z; 4%Z; 189%Z; 70%Z; 248%Z; 98%Z; 21%Z; 128%Z; 221%Z; 109%Z; 78%Z; 139%Z; 250%Z; 45%Z; 25%Z; 14%Z; 28%Z; 80%Z; 233%Z; 50%Z; 73%Z; 43%Z; 172%Z; 160%Z; 125%Z
    """
    hex_strings = coq \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("%Z", "") \
        .split(";")
    return [int(s) for s in hex_strings if s]


def parse_rust(rust: str) -> List[int]:
    """
    0x20, 0x95, 0x77, 0xbd, 0xa6, 0xbf, 0x4b, 0x58, 0x04, 0xbd, 0x46, 0xf8, 0x62, 0x15, 0x80, 0xdd, 0x6d, 0x4e, 0x8b, 0xfa, 0x2d, 0x19, 0x0e, 0x1c, 0x50, 0xe9, 0x32, 0x49, 0x2b, 0xac, 0xa0, 0x7d
    """
    hex_strings = rust \
        .replace("\n", "") \
        .replace(" ", "") \
        .split(",")
    return [int(s[2:], 16) for s in hex_strings if s]


def parse_json(json: str) -> List[int]:
    """
    32, 149, 119, 189, 166, 191, 75, 88, 4, 189, 70, 248, 98, 21, 128, 221, 109, 78, 139, 250, 45, 25, 14, 28, 80, 233, 50, 73, 43, 172, 160, 125
    """
    hex_strings = json \
        .replace("\n", "") \
        .replace(" ", "") \
        .split(",")
    return [int(s) for s in hex_strings if s]


def parse_auto(string: str) -> Optional[List[int]]:
    if is_c(string):
        return parse_c(string)
    elif is_coq(string):
        return parse_coq(string)
    elif is_rust(string):
        return parse_rust(string)
    elif is_json(string):
        return parse_json(string)
    elif is_string(string):
        return parse_string(string)
    else:
        return None


def format_string(lst: List[int]) -> str:
    return "".join([f"{x:02x}" for x in lst])


def format_c(lst: List[int]) -> str:
    return ", ".join([f"0x{lst[i]:02x}{lst[i+1]:02x}{lst[i+2]:02x}{lst[i+3]:02x}u" for i in range(0, len(lst), 4)])


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
        s = format_rust(lst)
    elif args.to_rust:
        s = format_coq(lst)
    elif args.to_json:
        s = format_json(lst)
    elif args.to_c:
        s = format_c(lst)
    else:
        s = format_string(lst)

    print(s)


if __name__ == "__main__":
    main()
