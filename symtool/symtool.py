import functools
import logging
import serial
import time

LOG = logging.getLogger(__name__)


def onlybytes(func):
    @functools.wraps(func)
    def wrapper(self, data, **kwargs):
        if not isinstance(data, bytes):
            raise ValueError(f'expected bytes, got: {data!r}')

        return func(self, data, **kwargs)

    return wrapper


class SYM1 (serial.Serial):
    character_interval = 0.1

    def __init__(self, *args, debug=None, **kwargs):
        super().__init__(*args, **kwargs)
        LOG.info('using port %s', self.port)

        self._debug = debug

    def read(self, count):
        data = super().read(count)
        if self._debug:
            print('R', repr(data))
        return data

    @onlybytes
    def write(self, data):
        if self._debug:
            print('W', repr(data))

        nbytes = 0
        for ch in data:
            nbytes += super().write(bytes([ch]))
            time.sleep(self.character_interval)

        return nbytes

    @onlybytes
    def read_until(self, data):
        return super().read_until(data)

    def connect(self):
        while True:
            LOG.info('trying to connect...')
            self.write(b'q')
            ch = self.read(1)
            if ch != b'':
                break

            time.sleep(1)

        LOG.info('connected')

        if ch == 'q':
            self.write(b'\r')

        self.return_to_prompt()

    def registers(self):
        self.write(b'r\r')
        self.read_until(b',')

        reg = {}
        for regname in ['s', 'f', 'a', 'x', 'y', 'p']:
            self.write(b'>')
            self.read_until(b'>')
            res = self.read_until(b',')
            data = res.strip().split(b',')[0]
            _regname, val = data.split()
            if _regname.decode().lower() != regname:
                raise KeyError(f'unexpected register name ({_regname} != {regname}')
            reg[regname] = val

        self.return_to_prompt()
        return reg

    def return_to_prompt(self):
        self.write(b'\r')
        self.read_until(b'.')

    def dump(self, addr, count=1):
        self.write(f'm{addr:x}\r'.encode())
        data = []
        for i in range(count):
            self.read_until(b'\n')
            addr = self.read_until(b',')
            val = self.read_until(b',')
            data.append(int(val[:-1], 16))
            self.write(b'>')

        self.return_to_prompt()
        return bytes(data)

    def load(self, addr, data):
        self.write(f'd{addr:x}\r'.encode())
        for val in data:
            self.write(f'{val:02x}'.encode())

        self.return_to_prompt()


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    s = SYM1('/dev/ttyUSB2', 2400, timeout=1, debug=True)
    s.connect()
