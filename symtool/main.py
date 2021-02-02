import click
import hexdump
import logging
import sys

import symtool.disasm
import symtool.symtool


@click.group(context_settings=dict(auto_envvar_prefix='SYMTOOL'))
@click.option('--device', '-d', default='/dev/ttyS0')
@click.option('--speed', '-s', default=2400, type=int)
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
    return int(v, 0)


@main.command()
@click.option('--hex/--disassemble', '-h/-d', 'ascii_mode', default=None)
@click.option('--output', '-o', type=click.File(mode='wb'), default=sys.stdout.buffer)
@click.argument('address', type=prefixed_int)
@click.argument('count', type=prefixed_int)
@click.pass_context
def dump(ctx, ascii_mode, output, address, count):
    sym = ctx.obj
    sym.connect()
    data = sym.dump(address, count)

    if count < 1:
        raise ValueError('count must be >= 1')

    with output:
        if ascii_mode is True:
            output.write(hexdump.hexdump(data, result='return').encode('ascii'))
            output.write(b'\n')
        elif ascii_mode is False:
            output.write(symtool.disasm.format(symtool.disasm.disasm(data, base=address)).encode())
        else:
            output.write(data)


@main.command()
@click.pass_context
def registers(ctx):
    sym = ctx.obj
    sym.connect()
    data = sym.registers()

    for reg, val in data.items():
        print(reg, f'{val:x}')


if __name__ == '__main__':
    main()

