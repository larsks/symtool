import pytest


from symtool.disasm import disasm

samples = [
    # test zero page,x
    [[0xb5, 0x20], [[0xb5, 0x20]], ['LDA     $20,X']],

    # test indirect
    [[0x6c, 0xfe, 0xff], [[0x6c, 0xfe, 0xff]], ['JMP     ($FFFE)']],

    # test immediate
    [[0x29, 0x80], [[0x29, 0x80]], ['AND     #$80']],

    # test short read
    [[0xb5, 0x20, 0x6c, 0xfe],
     [[0xb5, 0x20], [0x6c], [0xfe]],
     ['LDA     $20,X', '.byte   $6C', '.byte   $FE']],

    # test multiline
    [
        [0xa9, 0x01, 0x8d, 0x00, 0x02, 0xa9, 0x05, 0x8d, 0x01, 0x02, 0xa9, 0x08, 0x8d, 0x02, 0x02],
        [
            [0xa9, 0x01],
            [0x8d, 0x00, 0x02],
            [0xa9, 0x05],
            [0x8d, 0x01, 0x02],
            [0xa9, 0x08],
            [0x8d, 0x02, 0x02],
        ],
        [
            'LDA     #$01',
            'STA     $0200',
            'LDA     #$05',
            'STA     $0201',
            'LDA     #$08',
            'STA     $0202',
        ]
    ]
]


@pytest.mark.parametrize('sample_bin,expected_hex,expected_asm', samples)
def test_disasm(sample_bin, expected_hex, expected_asm):
    res = disasm(sample_bin)

    assert len(res) == len(expected_hex)

    for want, have in zip(expected_asm, res):
        assert want == have.asm

    for want, have in zip(expected_hex, res):
        assert want == have.src
