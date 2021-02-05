import click
import functools
import hexdump
import logging
import sys

import symtool.disasm
import symtool.symtool


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except symtool.symtool.SYMError as err:
            raise click.ClickException(str(err))

    return wrapper


@click.group(context_settings=dict(auto_envvar_prefix='SYMTOOL'))
@click.option('--device', '-d', default='/dev/ttyS0',
              help='set serial port (default=/dev/ttyS0)')
@click.option('--speed', '-s', default=4800, type=int,
              help='set port speed (default 4800)')
@click.option('--verbose', '-v', count=True,
              help='enable additional logging')
@click.pass_context
def main(ctx, device, speed, verbose):
    '''Symtool is a tool for interacting with a SYM-1 computer.

    The SYM-1 is a 6502 based single board computer produced by
    Synertek Systems Corp in 1975. Symtool lets you dump memory,
    load programs into memory, display register contents, and
    start executing code.

    The SYM-1 supports  baud rates from 110bps to 4800bps.
    '''

    try:
        loglevel = ['WARNING', 'INFO', 'DEBUG'][verbose]
    except IndexError:
        loglevel = 'DEBUG'

    logging.basicConfig(level=loglevel)

    ctx.obj = symtool.symtool.SYM1(device, speed, timeout=1,
                                   debug=(verbose > 2))


def prefixed_int(v):
    '''Transform a string argument with a numeric prefix into an integer.

    Accepts both standard Python prefixes (0x, 0o, 0b) as well as
    conventional 6502 prefixes ($ for hex, % for binary).
    '''
    if isinstance(v, int):
        return v
    elif v.startswith('$'):
        return int(v[1:], 16)
    elif v.startswith('%'):
        return int(v[1:], 2)
    else:
        return int(v, 0)


@main.command()
@click.option('--hex/--disassemble', '-h/-d', 'ascii_mode', default=None,
              help='output a hexdump (--hex) or disasssembly (--disassemble)')
@click.option('--output', '-o', type=click.File(mode='wb'), default=sys.stdout.buffer,
              help='output to file instead of stdout')
@click.argument('address', type=prefixed_int)
@click.argument('count', type=prefixed_int, default=1)
@click.pass_context
@handle_exceptions
def dump(ctx, ascii_mode, output, address, count):
    '''Dump memory from the SYM-1 to stdout or a file.

    By default, the dump command will dump binary data to stdout. You can
    dump to a file instead with the '-o <filename>' option.

    You can request a hex dump with the --hex option, and a disassembly
    by passing --disasseble.
    '''

    if count < 1:
        raise ValueError('count must be >= 1')

    sym = ctx.obj
    sym.connect()
    data = sym.dump(address, count)

    with output:
        if ascii_mode is True:
            output.write(hexdump.hexdump(data, result='return').encode('ascii'))
            output.write(b'\n')
        elif ascii_mode is False:
            output.write(symtool.disasm.format(symtool.disasm.disasm(data, base=address)).encode())
        else:
            output.write(data)


@main.command()
@click.option('--seek', '-s', type=prefixed_int,
              help='seek this many bytes into input before reading')
@click.option('--count', '-c', type=prefixed_int,
              help='number of bytes to read')
@click.option('--go', '-g', is_flag=True,
              help='jump to address after loading')
@click.argument('address', type=prefixed_int)
@click.argument('input', type=click.File(mode='rb'), default=sys.stdin.buffer)
@click.pass_context
@handle_exceptions
def load(ctx, seek, address, count, go, input):
    '''Load binary data from stdin or a file.

    The load command will read bytes from stdin (or an input file, if
    provided) and write them to the SYM-1 starting at <address>. If you
    specify the --go option, symtool will ask the SYM-1 to jump to <address>
    after loading the file.
    '''

    sym = ctx.obj
    sym.connect()

    with input:
        if seek:
            input.seek(seek)
        data = input.read(count)
        sym.load(address, data)

        if go:
            sym.go(address)


@main.command()
@click.argument('address', type=prefixed_int)
@click.argument('fillbyte', type=prefixed_int)
@click.argument('count', type=prefixed_int, default=1)
@click.pass_context
@handle_exceptions
def fill(ctx, address, fillbyte, count):
    '''Fill memory in the SYM-1 with the given byte value.

    The value should be specified as an integer with an optional
    base prefix.  For example, '$FF' or '0xFF' to fill memory with
    the value 255.
    '''

    sym = ctx.obj
    sym.connect()
    sym.fill(address, fillbyte, count)


@main.command()
@click.pass_context
@handle_exceptions
def registers(ctx):
    '''Dump 6502 registers'''
    flags = [
        'carry',
        'zero',
        'intr',
        'dec',
        None,
        None,
        'oflow',
        'neg',
    ]

    sym = ctx.obj
    sym.connect()
    data = sym.registers()

    for reg, val in data.items():
        print(reg, f'{val:02x} ({val:08b})', end='')
        if reg == 'f':
            for i in range(8):
                if not flags[i]:
                    continue

                print(' {}{}'.format(
                    '+' if val & (1 << i) else '-', flags[i]
                ), end='')
        print()


@main.command()
@click.argument('address', type=prefixed_int)
@click.pass_context
@handle_exceptions
def go(ctx, address):
    '''Start executing at the given address.

    This calls the monitor's "g" command.
    '''

    sym = ctx.obj
    sym.connect()
    sym.go(address)


if __name__ == '__main__':
    main()
