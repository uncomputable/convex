# Convex: Hex Converter

Convert between different hex representations.

```bash
$ convex [--from-{c,coq,rust,json,...}] [--to-{c,coq,rust,json,...}] [--reverse] input
```

Ignores whitespaces and newlines.

```bash
$ convex --to-c "
       209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d"
0x209577bdu, 0xa6bf4b58u, 0x04bd46f8u, 0x621580ddu, 0x6d4e8bfau, 0x2d190e1cu, 0x50e93249u, 0x2baca07du
```

Automatically matches the input format using regex.

```bash
$ convex "0x209577bdu, 0xa6bf4b58u, 0x04bd46f8u, 0x621580ddu, 0x6d4e8bfau, 0x2d190e1cu, 0x50e93249u, 0x2baca07du"
209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d
```

```bash
$ convex "32%Z; 149%Z; 119%Z; 189%Z; 166%Z; 191%Z; 75%Z; 88%Z; 4%Z; 189%Z; 70%Z; 248%Z; 98%Z; 21%Z; 128%Z; 221%Z; 109%Z; 78%Z; 139%Z; 250%Z; 45%Z; 25%Z; 14%Z; 28%Z; 80%Z; 233%Z; 50%Z; 73%Z; 43%Z; 172%Z; 160%Z; 125%Z"
209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d
```

Reverses the input if needed.

```bash
$ convex --reverse "209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d"
7da0ac2b4932e9501c0e192dfa8b4e6ddd801562f846bd04584bbfa6bd779520
```

Fuzzed for correctness.

## Supported representations

### String

```bash
$ convex --to-c "209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d"
0x209577bdu, 0xa6bf4b58u, 0x04bd46f8u, 0x621580ddu, 0x6d4e8bfau, 0x2d190e1cu, 0x50e93249u, 0x2baca07du
````

### C

```bash
$ convex --to-coq "0x209577bdu, 0xa6bf4b58u, 0x04bd46f8u, 0x621580ddu, 0x6d4e8bfau, 0x2d190e1cu, 0x50e93249u, 0x2baca07du"
32%Z; 149%Z; 119%Z; 189%Z; 166%Z; 191%Z; 75%Z; 88%Z; 4%Z; 189%Z; 70%Z; 248%Z; 98%Z; 21%Z; 128%Z; 221%Z; 109%Z; 78%Z; 139%Z; 250%Z; 45%Z; 25%Z; 14%Z; 28%Z; 80%Z; 233%Z; 50%Z; 73%Z; 43%Z; 172%Z; 160%Z; 125%Z```
```

### Coq

```bash
$ convex --to-rust "32%Z; 149%Z; 119%Z; 189%Z; 166%Z; 191%Z; 75%Z; 88%Z; 4%Z; 189%Z; 70%Z; 248%Z; 98%Z; 21%Z; 128%Z; 221%Z; 109%Z; 78%Z; 139%Z; 250%Z; 45%Z; 25%Z; 14%Z; 28%Z; 80%Z; 233%Z; 50%Z; 73%Z; 43%Z; 172%Z; 160%Z; 125%Z"
0x20, 0x95, 0x77, 0xbd, 0xa6, 0xbf, 0x4b, 0x58, 0x04, 0xbd, 0x46, 0xf8, 0x62, 0x15, 0x80, 0xdd, 0x6d, 0x4e, 0x8b, 0xfa, 0x2d, 0x19, 0x0e, 0x1c, 0x50, 0xe9, 0x32, 0x49, 0x2b, 0xac, 0xa0, 0x7d
```

### Rust

```bash
$ convex --to-json "0x20, 0x95, 0x77, 0xbd, 0xa6, 0xbf, 0x4b, 0x58, 0x04, 0xbd, 0x46, 0xf8, 0x62, 0x15, 0x80, 0xdd, 0x6d, 0x4e, 0x8b, 0xfa, 0x2d, 0x19, 0x0e, 0x1c, 0x50, 0xe9, 0x32, 0x49, 0x2b, 0xac, 0xa0, 0x7d"
32, 149, 119, 189, 166, 191, 75, 88, 4, 189, 70, 248, 98, 21, 128, 221, 109, 78, 139, 250, 45, 25, 14, 28, 80, 233, 50, 73, 43, 172, 160, 125
```

### JSON

```
$ convex "32, 149, 119, 189, 166, 191, 75, 88, 4, 189, 70, 248, 98, 21, 128, 221, 109, 78, 139, 250, 45, 25, 14, 28, 80, 233, 50, 73, 43, 172, 160, 125"
209577bda6bf4b5804bd46f8621580dd6d4e8bfa2d190e1c50e932492baca07d
```

## Run the script

There are zero dependencies so just run python.

```bash
python convex.py
```

## Install the script using nix

Build the default package.

```bash
nix-build
```

Install the built derivation in your nix profile.

```bash
nix profile install ./result
```

## Install the script using pip

Install the script using pip.

```bash
pip install .
```
