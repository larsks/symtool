import logging
import serial
import time

LOG = logging.getLogger(__name__)


class SYMError(Exception):
    '''Parent class for exceptions raised by this module.'''


class TimeoutError(SYMError):
    '''Indicates a timeout when waiting for serial data.

    Note that this may simply mean that we're out of sync with the
    monitor (e.g., code has called read_until('.') but the monitor
    is waiting for input).
    '''


class CommandError(SYMError):
    '''Raised if we receive an error response from the SYM-1.'''

    def __init__(self, code):
        self.code = code
        super().__init__(f'Error {code}')


def stripped(i):
    return (x.strip() for x in i)


class SYM1 (serial.Serial):
    character_interval = 0.05

    def __init__(self, *args, debug=None, **kwargs):
        super().__init__(*args, **kwargs)
        LOG.info('using port %s', self.port)

        self._debug = debug
        self._last_err = None
        self._last_command = None

    def read(self, count):
        '''Read bytes from the SYM-1.'''

        data = super().read(count)
        if data == b'':
            raise TimeoutError()
        if self._debug:
            print('R', repr(data))
        return data

    def write(self, data):
        '''Write data to the SYM-1.

        This will convert any string data to bytes by calling
        data.encode(). If you don't want that, just call it with
        bytes instead.
        '''

        if isinstance(data, str):
            data = data.encode()

        if self._debug:
            print('W', repr(data))

        nbytes = 0
        for ch in data:
            nbytes += super().write(bytes([ch]))
            time.sleep(self.character_interval)

        return nbytes

    def send_command(self, cmd, *args):
        '''Send a command and parameters to the monitor.'''

        LOG.debug('send command: %s %s', cmd, args)
        self._last_command = (cmd, args)
        self.write(cmd)

        for i, arg in enumerate(args):
            if i != 0:
                self.write(',')
            self.write(arg)

        self.write('\r')
        self.read_until(b'\r\n')

    def return_to_prompt(self, send_cr=False):
        '''Cancel command and return to monitor prompt.

        This send a <cr>, then reads everything until the
        monitor prompt. Returns a list of response lines.
        '''

        LOG.debug('waiting for prompt')

        if send_cr:
            self.write('\r')

        # XXX: single character markers make me nervous. Previously this
        # was read_until(b'\r\n.'), but changed because the 'f' (fill)
        # command returns directly to the prompt, and the '\r\n'
        # is consumed by send_command().
        res = self.read_until(b'.')
        lines = [line for line in stripped(res.splitlines()) if line]
        for line in lines:
            if line.startswith(b'ER '):
                code = int(line.strip().split()[1], 16)
                self._last_err = code
                raise CommandError(code)

        # return everything but the prompt
        return lines[:-1]

    def connect(self):
        '''Intiailize connection to the SYM-1.

        Send a 'q' character out the serial port to trigger the SYM-1
        auto baud detection. Handle any error response if the SYM-1
        serial prompt was already active.
        '''

        LOG.info('connecting to sym1...')

        while True:
            self.write('q')
            ch = self.read(1)
            if ch != b'':
                break

            LOG.warning('failed to connect on %s; retrying...',
                        self.port)
            time.sleep(1)

        LOG.info('connected')

        if ch == b'q':
            self.write('\r')

        # We expect a CommandError here, since if the SYM-1 was
        # already connected we just send the invalid "q" command.
        try:
            self.return_to_prompt()
        except CommandError as err:
            if err.code == 51:
                pass

        # Flush input buffer. This takes care of any extra output caused
        # by the monitor being in an unknown state when we started.
        try:
            self.read_all()
        except TimeoutError:
            pass

    def registers(self):
        '''Read register contents.'''

        self.send_command('r')
        self.read_until(b',')

        reg = {}
        for regname in ['s', 'f', 'a', 'x', 'y', 'p']:
            self.write('>')
            self.read_until(b'>')
            res = self.read_until(b',')
            data = res.strip().split(b',')[0]
            _regname, val = data.split()
            if _regname.decode().lower() != regname:
                raise KeyError(f'unexpected register name ({_regname} != {regname}')
            reg[regname] = int(val, 16)

        self.return_to_prompt(True)
        return reg

    def dump(self, addr, count=1):
        '''Read bytes from memory.'''

        LOG.info('reading %d bytes of data from $%X', count, addr)
        self.send_command('m', f'{addr:x}'.encode())
        data = []
        for i in range(count):
            addr = self.read_until(b',')
            val = self.read_until(b',')
            data.append(int(val[:-1], 16))
            self.write('>')
            self.read_until(b'\r\n')

        self.return_to_prompt(True)
        return bytes(data)

    def load(self, addr, data):
        '''Write bytes to memory'''

        LOG.info('loading %d bytes of data at $%X', len(data), addr)
        self.send_command('d', f'{addr:x}'.encode())
        for val in data:
            self.write(f'{val:02x}'.encode())
            self.read_until(b' ')

        self.return_to_prompt(True)

    def go(self, addr):
        '''Start executing at addr.'''

        LOG.info('jump to subroutine at %X', addr)
        self.send_command('g', f'{addr:x}'.encode())

    def fill(self, addr, fillbyte=0, count=1):
        '''Fill memory with the specified fillbyte (default 0).'''

        LOG.info('fill %d bytes of memory at $%X with %r',
                 count, addr, fillbyte)
        end = addr + (count-1)
        self.send_command('f', f'{fillbyte:x}', f'{addr:x}', f'{end:x}')
        self.return_to_prompt()
