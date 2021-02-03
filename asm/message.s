; This is "Program #2 - Rotating Display" from page 12 of the SYM-1 "Technical
; Notes" document (with a modified message).
; (http://www.6502.org/trainers/synertek/manuals/technotes.pdf)

                .include        "monitor.s"

                ; symbol table for the led display

O0              =               $3F
O1              =               $06
O2              =               $5B
O3              =               $4F
O4              =               $66
O5              =               $6D
O6              =               $07
O7              =               $07
O8              =               $7F
O9              =               $67
OBLANK          =               $00
ODOT            =               $80
OA              =               $77
OB              =               $7C
OC              =               $39
OD              =               $5E
OE              =               $79
OF              =               $71
OG              =               $6F
OH              =               $76
OI              =               $06
OJ              =               $1E
OK              =               $74
OL              =               $38
OM1             =               $33
OM2             =               $27
ON              =               $54
OO              =               $3F
OP              =               $73
OQ              =               $67
OR              =               $50
OS              =               $6D
OT              =               $46
OU              =               $3E
OV1             =               $64
OV2             =               $52
OW1             =               $3C
OW2             =               $1F
OX              =               $00
OY              =               $6E
OZ              =               $00


                .segment        "RODATA"
message:        .byte           OO,OD,OD,OB,OI,OT,OBLANK

                .segment        "ZEROPAGE"
count:          .byte           0

                .segment        "CODE"
                jsr             ACCESS          ; write enable system ram
                ldy             #$06            ; take characters from message
one:            lda             message,y       ; and fill the display buffer
                sta             DISBUF,y        ; with them
                dey
                bpl             one

cycle:          lda             #$ff            ; set the number of times we
                sta             count           ; flash the leds with the contents
                                                ; of DISBUF

two:            jsr             SCAND           ; flash the displays
                dec             count           ; until we zero out count
                bne             two

                lda             DISBUF          ; save the top number
                pha                             ; on the stack

                ldy             #$0             ; shift up the remaining
three:          lda             DISBUF+1,y      ; registers by looping and
                sta             DISBUF,y        ; incrementing the y register
                iny
                cpy             #$06            ; check to see if we have looped
                bne             three           ; the right number of times

                pla                             ; place the first register in
                sta             DISBUF+6        ; the last memory location

                jmp             cycle
