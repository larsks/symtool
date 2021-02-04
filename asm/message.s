; This is "Program #2 - Rotating Display" from page 12 of the SYM-1 "Technical
; Notes" document (with a modified message).
; (http://www.6502.org/trainers/synertek/manuals/technotes.pdf)

                .import         ACCESS,DISBUF,SCAND,KYSTAT
                .include        "segments.s"

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

                clc
                jsr             KYSTAT          ; check if key is pressed
                bcc             cycle           ; cycle if no key
                rts                             ; otherwise exit
