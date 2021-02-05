import pytest

from unittest import mock

from symtool import symtool


@pytest.fixture
@mock.patch('symtool.symtool.DelayedSerial', autospec=True)
def sym(fake_serial):
    s = symtool.SYM1('TESTDEV')
    return s


def test_connect(sym):
    sym._dev.read.side_effect = [
        b'q',
    ]

    sym._dev.read_until.side_effect = [
        b'\r\n.'
    ]

    sym.connect()
    assert sym._dev.write.call_args_list[0][0] == ('q',)
    assert sym._dev.read_until.call_args_list[0][0] == (b'.',)


def test_connect_unexpected_error(sym):
    sym._dev.read.side_effect = [
        b'q',
    ]

    sym._dev.read_until.side_effect = [
        b'\r\nER 42\r\n.'
    ]

    with pytest.raises(symtool.CommandError):
        sym.connect()


def test_connect_expected_error(sym):
    sym._dev.read.side_effect = [
        b'q',
    ]

    sym._dev.read_until.side_effect = [
        b'\r\nER 51\r\n.'
    ]

    sym.connect()


def test_registers_disconnected(sym):
    with pytest.raises(symtool.DisconnectedError):
        sym.registers()


def test_registers(sym):
    sym._dev.read_until.side_effect = [
        b'\r\n.'
        b'r \r',
        b'\r\n',
        b'\r\nP 1234,',
        b'>',
        b'\r\nS   00,',
        b'>',
        b'\r\nF   01,',
        b'>',
        b'\r\nA   02,',
        b'>',
        b'\r\nX   03,',
        b'>',
        b'\r\nY   04,',
        b'>',
        b'\r\nP 1234,',
        b'\r\n.',
    ]

    sym.connect()
    res = sym.registers()
    assert res['p'] == 0x1234
    assert res['s'] == 0x00
    assert res['f'] == 0x01
    assert res['a'] == 0x02
    assert res['x'] == 0x03
    assert res['y'] == 0x04


def test_dump(sym):
    sym._dev.read_until.side_effect = [
        b'\r\n.'
        b'm 200\r\r\n',
        b'\r\n',
        b'0200,',
        b'01,',
        b'>\r\n',
        b'0201,',
        b'02,',
        b'>\r\n',
        b'0202,',
        b'03,',
        b'>\r\n',
        b'0203,',
        b'04,',
        b'>\r\n',
        b'0204,',
        b'05,',
        b'\r\n.',
    ]

    sym.connect()
    res = sym.dump(0x200, 4)
    assert res == b'\x01\x02\x03\x04'


def test_load(sym):
    sym._dev.read_until.side_effect = [
        b'\r\n.'
        b'd 200\r\r\n',
        b' ',
        b' ',
        b' ',
        b' ',
        b' ',
        b'\r\n.',
    ]

    expected_data = [b'01', b'02', b'03', b'04']

    sym.connect()
    sym.load(0x200, [0x01, 0x02, 0x03, 0x04])
    args_of_interest = sym._dev.write.call_args_list[-5:-1]
    assert [x[0][0] for x in args_of_interest] == expected_data


def test_go(sym):
    sym._dev.read_until.side_effect = [
        b'\r\n.'
        b'g 200\r\r\n',
        b'\r\n.',
    ]

    expected_data = ['g', b'200']

    sym.connect()
    sym.go(0x200)

    args_of_interest = sym._dev.write.call_args_list[-3:-1]
    assert [x[0][0] for x in args_of_interest] == expected_data


def test_fill(sym):
    sym._dev.read_until.side_effect = [
        b'\r\n.'
        b'f 0,200,203\r\r\n',
        b'.',
        b'.',
    ]

    expected_data = ['f', '0', ',', '200', ',', '203']

    sym.connect()
    sym.fill(0x200, fillbyte=0, count=4)

    args_of_interest = sym._dev.write.call_args_list[-7:-1]
    assert [x[0][0] for x in args_of_interest] == expected_data
