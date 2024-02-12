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


def parse_string(string: str) -> Optional[List[int]]:
    if not is_string(string):
        return None
    hex_string = string \
        .replace("\n", "") \
        .replace(" ", "")
    hex_strings = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    return [int(s, 16) for s in hex_strings if s]


def parse_c(c: str) -> Optional[List[int]]:
    if not is_c(c):
        return None
    four_hex_strings = c \
        .replace("\n", "") \
        .replace(" ", "") \
        .split(",")
    hex_strings = [s[2:-1][i:i+2] for s in four_hex_strings for i in range(0, 8, 2)]
    return [int(s, 16) for s in hex_strings if s]


def parse_coq(coq: str) -> Optional[List[int]]:
    if not is_coq(coq):
        return None
    hex_strings = coq \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("%Z", "") \
        .split(";")
    return [int(s) for s in hex_strings if s]


def parse_rust(rust: str) -> Optional[List[int]]:
    if not is_rust(rust):
        return None
    hex_strings = rust \
        .replace("\n", "") \
        .replace(" ", "") \
        .split(",")
    return [int(s[2:], 16) for s in hex_strings if s]


def parse_json(json: str) -> Optional[List[int]]:
    if not is_json(json):
        return None
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
    else:
        return parse_string(string)


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
    elif args.to_coq:
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
