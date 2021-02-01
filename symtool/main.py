import binascii
import click
import logging
import sys

import symtool.symtool


@click.group()
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
@click.option('--hex', '-h', 'print_hex', is_flag=True)
@click.option('--output', '-o', type=click.File(mode='wb'), default=sys.stdout.buffer)
@click.argument('address', type=prefixed_int)
@click.argument('count', type=prefixed_int)
@click.pass_context
def dump(ctx, print_hex, output, address, count):
    sym = ctx.obj
    data = sym.dump(address, count)

    with output:
        if print_hex:
            output.write(binascii.hexlify(data, sep='\n', bytes_per_sep=16))
        else:
            output.write(data)


if __name__ == '__main__':
    main()

