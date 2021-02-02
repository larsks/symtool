# symtool

Symtool is a tool for interacting with the `SUPERMON` monitor on a
[SYM-1][] microcomputer.

[sym-1]: https://en.wikipedia.org/wiki/SYM-1

## Synopsis

```
Usage: symtool [OPTIONS] COMMAND [ARGS]...

Options:
  -d, --device TEXT
  -s, --speed INTEGER
  -v, --verbose
  --help               Show this message and exit.

Commands:
  dump
  fill
  go
  load
  registers
```

Numbers (such as memory addresses, counts, etc) can be specified
using Python's numeric prefixes:

- Decimal (no prefix): `8192`
- Hexadecimal: `0x2000`
- Octal: `0o20000`
- Binary: `0b10000000000000`

And in order to meet common 6502 conventions, you can also use `$` as
a prefix on hexadecimal numbers (`$2000`).

## Dump memory

```
Usage: symtool dump [OPTIONS] ADDRESS [COUNT]

Options:
  -h, --hex / -d, --disassemble
  -o, --output FILENAME
  --help                         Show this message and exit.
```


## Load memory

```
Usage: symtool load [OPTIONS] [INPUT]

Options:
  -s, --seek PREFIXED_INT
  -a, --address PREFIXED_INT
  -c, --count PREFIXED_INT
  --help                      Show this message and exit.
```

## Fill memory

```
Usage: symtool fill [OPTIONS] ADDRESS FILLBYTE [COUNT]

Options:
  --help  Show this message and exit.
```

To fill memory at `$400` with 16 zeros:

```
$ symtool fill 0x400 0 16
$ symtool dump 0x400 16 -h
00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
```

## Show registers

```
Usage: symtool registers [OPTIONS]

Options:
  --help  Show this message and exit.
```

## Jump to address

```
Usage: symtool go [OPTIONS] ADDRESS

Options:
  --help  Show this message and exit.
```
