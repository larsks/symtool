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

## Configuration

You can set the device and speed on the command line using the
`--device` and `--speed` options (aka `-d` and `-s`), or you can set
the `SYMTOOL_DEVICE` and `SYMTOOL_SPEED` variables in your
environment.

The SYM_1 supports baud rates from 110bps to 4800bps.

## Commands

### Dump memory

```
Usage: symtool dump [OPTIONS] ADDRESS [COUNT]

Options:
  -h, --hex / -d, --disassemble
  -o, --output FILENAME
  --help                         Show this message and exit.
```

You can dump binary output:

```
$ symtool dump 0x400 16 -o somefile.bin
```

You can generate a hexdump:

```
$ symtool dump 0x400 16 -h
00000000: A2 FF A0 FF CA D0 FD 88  D0 FA 20 72 89 4C 00 04  .......... r.L..
```

You can disassemble the memory:

```
$ symtool dump 0x400 16 -d
$0400   a2 ff       LDX #$FF
$0402   a0 ff       LDY #$FF
$0404   ca          DEX
$0405   d0 fd       BNE $FD
$0407   88          DEY
$0408   d0 fa       BNE $FA
$040a   20 72 89    JSR $8972
$040d   4c 00 04    JMP $0400
```

### Load memory

```
Usage: symtool load [OPTIONS] ADDRESS [INPUT]

Options:
  -s, --seek PREFIXED_INT
  -c, --count PREFIXED_INT
  --help                    Show this message and exit.
```

To load `asm/beeper.bin` into memory at location `$400`:

```
$ symtool -v load 0x400 asm/beeper.bin
INFO:symtool.symtool:using port /dev/ttyUSB2
INFO:symtool.symtool:connecting to sym1...
INFO:symtool.symtool:connected
INFO:symtool.symtool:loading 16 bytes of data at $400
```

### Fill memory

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

### Show registers

```
Usage: symtool registers [OPTIONS]

Options:
  --help  Show this message and exit.
```

Example usage:


```
$ symtool registers
s ff (11111111)
f b1 (10110001) +carry -zero -intr -dec -oflow +neg
a 80 (10000000)
x 00 (00000000)
y 50 (01010000)
p b0ac (1011000010101100)
```

### Jump to address

```
Usage: symtool go [OPTIONS] ADDRESS

Options:
  --help  Show this message and exit.
```

To run a program at location `$400`:

```
$ symtool go 0x400
```

## Compiling assembly programs

The assembly programs in the `asm` directory are written to be
compatible with the [ca65 assembler][]. The `Makefile` in that
directory will compile the source to `.bin` files that can be loaded
to your SYM-1 using the `symtool load` command.

[ca65]: https://cc65.github.io/doc/ca65.html
