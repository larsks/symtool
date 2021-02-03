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


def disasm(data, base=0):
    def _disasm_one_line(data):
        addr, opcode = next(data)

        line = {
            'addr': addr,
            'hex': [],
            'asm': None,
        }

        mnemonic = mnemonics[opcode]
        addrmode = addressing[opcode]
        line['hex'].append(opcode)

        if addrmode in ['imp', 'acc']:
            line['asm'] = mnemonic
            return line

        operand = next(data)[1]
        line['hex'].append(operand)

        if addrmode == 'imm':
            line['asm'] = f'{mnemonic} #${operand:02X}'
            return line
        elif addrmode in ['rel', 'zpg']:
            line['asm'] = f'{mnemonic} ${operand:02X}'
            return line
        elif addrmode == 'zpx':
            line['asm'] = f'{mnemonic} ${operand:02X},X'
            return line
        elif addrmode == 'zpy':
            line['asm'] = f'{mnemonic} ${operand:02X},Y'
            return line
        elif addrmode == 'inx':
            line['asm'] = f'{mnemonic} (${operand:02X},X)'
            return line
        elif addrmode == 'zpy':
            line['asm'] = f'{mnemonic} (${operand:02X}),Y'
            return line

        op2 = next(data)[1]

        line['hex'].append(op2)
        operand = (op2 << 8) + operand

        if addrmode == 'ind':
            line['asm'] = f'{mnemonic} (${operand:04X})'
            return line
        elif addrmode == 'abs':
            line['asm'] = f'{mnemonic} ${operand:04X}'
            return line
        elif addrmode == 'abx':
            line['asm'] = f'{mnemonic} ${operand:04X},X'
            return line
        elif addrmode == 'aby':
            line['asm'] = f'{mnemonic} ${operand:04X},Y'
            return line

    data = enumerate(data, base)
    lines = []

    while True:
        try:
            lines.append(_disasm_one_line(data))
        except StopIteration:
            break

    return lines


def format(lines):
    buf = []

    for line in lines:
        hex = ' '.join(f'{x:02x}' for x in line['hex'])
        buf.append(f'${line["addr"]:04x}   {hex:12}{line["asm"]}\n')

    return ''.join(buf)
