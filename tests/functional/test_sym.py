import os
import pytest

from symtool import symtool


@pytest.fixture
def sym():
    dev = os.environ['SYMTOOL_DEVICE']
    s = symtool.SYM1(dev)
    s.connect()
    return s


def test_load_dump(sym):
    orig = list(range(8))
    sym.load(0x200, orig)
    res = sym.dump(0x200, 8)

    assert len(res) == len(orig)
    assert all(x == y for x, y in zip(orig, res))


def test_go_dump(sym):
    # lda #$cc
    # sta $10
    # rts
    sym.load(0x200, [0xa9, 0xcc, 0x85, 0x10, 0x60])
    sym.go(0x200)
    sym.return_to_prompt()
    res = sym.dump(0x10)
    assert res[0] == 0xcc


def test_fill_dump(sym):
    sym.fill(0x200, fillbyte=0xcc, count=8)
    res = sym.dump(0x200, 8)
    assert all(x == 0xcc for x in res)


def test_registers(sym):
    res = sym.registers()
    assert (x in res for x in ['a', 'x', 'y', 'p', 'f', 's'])
