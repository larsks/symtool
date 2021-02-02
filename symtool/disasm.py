from io import StringIO

mnemonics = [
  'BRK', 'ORA', '???', '???', '???', 'ORA', 'ASL', '???', 'PHP', 'ORA', 'ASL', '???', '???', 'ORA', 'ASL', '???',
  'BPL', 'ORA', '???', '???', '???', 'ORA', 'ASL', '???', 'CLC', 'ORA', '???', '???', '???', 'ORA', 'ASL', '???',
  'JSR', 'AND', '???', '???', 'BIT', 'AND', 'ROL', '???', 'PLP', 'AND', 'ROL', '???', 'BIT', 'AND', 'ROL', '???',
  'BMI', 'AND', '???', '???', '???', 'AND', 'ROL', '???', 'SEC', 'AND', '???', '???', '???', 'AND', 'ROL', '???',
  'RTI', 'EOR', '???', '???', '???', 'EOR', 'LSR', '???', 'PHA', 'EOR', 'LSR', '???', 'JMP', 'EOR', 'LSR', '???',
  'BVC', 'EOR', '???', '???', '???', 'EOR', 'LSR', '???', 'CLI', 'EOR', '???', '???', '???', 'EOR', 'LSR', '???',
  'RTS', 'ADC', '???', '???', '???', 'ADC', 'ROR', '???', 'PLA', 'ADC', 'ROR', '???', 'JMP', 'ADC', 'ROR', '???',
  'BVS', 'ADC', '???', '???', '???', 'ADC', 'ROR', '???', 'SEI', 'ADC', '???', '???', '???', 'ADC', 'ROR', '???',
  '???', 'STA', '???', '???', 'STY', 'STA', 'STX', '???', 'DEY', '???', 'TXA', '???', 'STY', 'STA', 'STX', '???',
  'BCC', 'STA', '???', '???', 'STY', 'STA', 'STX', '???', 'TYA', 'STA', 'TXS', '???', '???', 'STA', '???', '???',
  'LDY', 'LDA', 'LDX', '???', 'LDY', 'LDA', 'LDX', '???', 'TAY', 'LDA', 'TAX', '???', 'LDY', 'LDA', 'LDX', '???',
  'BCS', 'LDA', '???', '???', 'LDY', 'LDA', 'LDX', '???', 'CLV', 'LDA', 'TSX', '???', 'LDY', 'LDA', 'LDX', '???',
  'CPY', 'CMP', '???', '???', 'CPY', 'CMP', 'DEC', '???', 'INY', 'CMP', 'DEX', '???', 'CPY', 'CMP', 'DEC', '???',
  'BNE', 'CMP', '???', '???', '???', 'CMP', 'DEC', '???', 'CLD', 'CMP', '???', '???', '???', 'CMP', 'DEC', '???',
  'CPX', 'SBC', '???', '???', 'CPX', 'SBC', 'INC', '???', 'INX', 'SBC', 'NOP', '???', 'CPX', 'SBC', 'INC', '???',
  'BEQ', 'SBC', '???', '???', '???', 'SBC', 'INC', '???', 'SED', 'SBC', '???', '???', '???', 'SBC', 'INC', '???']

addressing = [
  'imp', 'inx', 'imp', 'imp', 'imp', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'imp', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'abs', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imp', 'inx', 'imp', 'imp', 'imp', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imp', 'inx', 'imp', 'imp', 'imp', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'acc', 'imp', 'ind', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imp', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imp', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'zpx', 'zpx', 'zpy', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'imp', 'imp',
  'imm', 'inx', 'imm', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'zpx', 'zpx', 'zpy', 'imp', 'imp', 'aby', 'imp', 'imp', 'abx', 'abx', 'aby', 'imp',
  'imm', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp',
  'imm', 'inx', 'imp', 'imp', 'zpg', 'zpg', 'zpg', 'imp', 'imp', 'imm', 'imp', 'imp', 'abs', 'abs', 'abs', 'imp',
  'rel', 'iny', 'imp', 'imp', 'imp', 'zpx', 'zpx', 'imp', 'imp', 'aby', 'imp', 'imp', 'imp', 'abx', 'abx', 'imp']


class once:
    def __init__(self):
        self.ran = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.ran:
            raise StopIteration()

        self.ran = True


def disasm(data, base=0):
    def _disasm_one_line():
        nonlocal pos

        line = {
            'addr': base+pos,
            'hex': [],
            'asm': ''
        }

        for i in once():
            opcode = data[pos]
            mnemonic = mnemonics[opcode]
            addrmode = addressing[opcode]
            pos += 1

            line['hex'].append(opcode)

            if addrmode in ['imp', 'acc']:
                line['asm'] = mnemonic
                break

            operand = data[pos]
            line['hex'].append(operand)
            pos += 1

            if addrmode == 'imm':
                line['asm'] = f'{mnemonic} #${operand:02X}'
                break
            elif addrmode in ['rel', 'zpg']:
                line['asm'] = f'{mnemonic} ${operand:02X}'
                break
            elif addrmode == 'zpx':
                line['asm'] = f'{mnemonic} ${operand:02X},X'
                break
            elif addrmode == 'zpy':
                line['asm'] = f'{mnemonic} ${operand:02X},Y'
                break
            elif addrmode == 'inx':
                line['asm'] = f'{mnemonic} (${operand:02X},X)'
                break
            elif addrmode == 'zpy':
                line['asm'] = f'{mnemonic} (${operand:02X}),Y'
                break

            op2 = data[pos]

            line['hex'].append(op2)
            operand = (op2 << 8) + operand
            pos += 1

            if addrmode == 'ind':
                line['asm'] = f'{mnemonic} (${operand:04X})'
                break
            elif addrmode == 'abs':
                line['asm'] = f'{mnemonic} ${operand:04X}'
                break
            elif addrmode == 'abx':
                line['asm'] = f'{mnemonic} ${operand:04X},X'
                break
            elif addrmode == 'aby':
                line['asm'] = f'{mnemonic} ${operand:04X},Y'
                break

        return line

    pos = 0
    lines = []

    while pos < len(data):
        try:
            line = _disasm_one_line()
        except IndexError:
            break
        else:
            lines.append(line)

    return lines


def format(lines):
    buf = StringIO()

    for line in lines:
        hex = ' '.join(f'{x:02x}' for x in line['hex'])
        buf.write(f'${line["addr"]:04x}   {hex:12}{line["asm"]}\n')

    return buf.getvalue()


sample_hex = 'a9 01 8d 00 02 a9 05 8d 01 02 a9 08 8d 02 02'
sample_bin = bytes([int(x, 16) for x in sample_hex.split()])
sample_code = '''
LDA #$01
STA $0200
LDA #$05
STA $0201
LDA #$08
STA $0202
'''
