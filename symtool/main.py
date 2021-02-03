import click
import hexdump
import logging
import sys

import symtool.disasm
import symtool.symtool


@click.group(context_settings=dict(auto_envvar_prefix='SYMTOOL'))
@click.option('--device', '-d', default='/dev/ttyS0')
@click.option('--speed', '-s', default=4800, type=int)
@click.option('--verbose', '-v', count=True)
@click.pass_context
def main(ctx, device, speed, verbose):
    debug = verbose > 1

    try:
        loglevel = ['WARNING', 'INFO', 'DEBUG'][verbose]
    except IndexError:
        loglevel = 'DEBUG'

    logging.basicConfig(level=loglevel)

    ctx.obj = symtool.symtool.SYM1(device, speed, timeout=1, debug=debug)


def prefixed_int(v):
    if isinstance(v, int):
        return v
    elif v.startswith('$'):
        return int(v[1:], 16)
    else:
        return int(v, 0)


@main.command()
@click.option('--hex/--disassemble', '-h/-d', 'ascii_mode', default=None)
@click.option('--output', '-o', type=click.File(mode='wb'), default=sys.stdout.buffer)
@click.argument('address', type=prefixed_int)
@click.argument('count', type=prefixed_int, default=1)
@click.pass_context
def dump(ctx, ascii_mode, output, address, count):
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
@click.option('--seek', '-s', type=prefixed_int)
@click.option('--count', '-c', type=prefixed_int)
@click.argument('address', type=prefixed_int)
@click.argument('input', type=click.File(mode='rb'), default=sys.stdin.buffer)
@click.pass_context
def load(ctx, seek, address, count, input):
    sym = ctx.obj
    sym.connect()

    with input:
        if seek:
            input.seek(seek)
        data = input.read(count)
        sym.load(address, data)


@main.command()
@click.argument('address', type=prefixed_int)
@click.argument('fillbyte', type=prefixed_int)
@click.argument('count', type=prefixed_int, default=1)
@click.pass_context
def fill(ctx, address, fillbyte, count):
    sym = ctx.obj
    sym.connect()
    sym.fill(address, fillbyte, count)


@main.command()
@click.pass_context
def registers(ctx):
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
def go(ctx, address):
    sym = ctx.obj
    sym.connect()
    sym.go(address)


if __name__ == '__main__':
    main()
