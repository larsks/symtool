; This is "Program #3 - Count and Beep" from page 14 of the SYM-1 "Technical
; Notes" document (with a modified message).
; (http://www.6502.org/trainers/synertek/manuals/technotes.pdf)

                .import         ACCESS,IRQVEC,SCAND,BEEP,SEGTBL
                .import         D1,D2,D3,D4,D5,D6

                                                ; registers on 6522 #3 (U29)
ACR1            =               $AC0B           ; auxiliary control register
IER1            =               $AC0E           ; interrupt enable register
IFR1            =               $AC0D           ; interrupt flag register
T1CH            =               $AC05           ; T1 high-byte counter
T1LL            =               $AC06           ; T1 low-byte latch

                .segment        "ZEROPAGE"
flag:          .byte           0                ; interrupt counter
flag1:         .byte           0                ; loop counter for beep action
num:           .byte           0                ; current counter value

                .segment        "CODE"
                jsr             ACCESS          ; write enable system ram
                lda             #$20
                sta             flag1
                lda             #<intcnt        ; point irqvec at our intcnt
                sta             IRQVEC          ; routine
                lda             #>intcnt
                sta             IRQVEC+1
                lda             #$40
                sta             ACR1            ; enable T1 continuous interrupts
                lda             #$4e            ; low byte of T1 counter
                sta             T1LL
                lda             #$c0            ; enable T1
                sta             IER1            ; interrupts
                lda             #$00
                sta             flag            ; zero flag variable
                lda             #$20            ; high byte of T1 counter
                sta             T1CH            ; start counting
                clc
                cli

displ:          lda             #$00
                sta             D6              ; blank all displays except
                sta             D5              ; D3 and D4
                sta             D2
                sta             D1
disp:           lda             num
                and             #$0f            ; strip high nibble
                jsr             conv            ; convert to 7-segment code
                sta             D3              ; store it
disp2:          lda             num
                lsr
                lsr
                lsr
                lsr                             ; shift high nibble to low nibble
                jsr             conv            ; convert it
                sta             D4              ; store it
                jsr             SCAND
                jmp             displ

intcnt:         pha                             ; save all registers
                txa
                pha
                tya
                pha
                lda             IFR1
                sta             IFR1            ; clear all pending interrupts
                inc             flag            ; increment interrupt count
                lda             flag
                cmp             #5              ; 5 interrupts yet?
                beq             add             ; yes, increment display
                bvc             restore         ; no, go back and wait

add:            lda             #$00
                sta             flag            ; zero flag variable
                jsr             count
                bvc             restore

conv:           tax                             ; convert value in A to 7-segment code
                lda             SEGTBL,X
                rts

count:          clc                             ; increment counter
                lda             num
                adc             #$01
                clc
                clv
                sta             num
                cmp             #$ff            ; if we reach $ff, sound alarm
                beq             beep
                rts

beep:           lda             #$7c            ; B
                sta             D5
                lda             #$79            ; E
                sta             D4
                sta             D3
                lda             #$73            ; P
                sta             D2
                lda             #$00
                sta             num
delay:          jsr             BEEP            ; display BEEP and play a sound
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                dec             flag1
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                jsr             SCAND
                lda             flag1
                cmp             #$0
                bne             delay
                lda             #$20
                sta             flag1
                rts

restore:        pla                             ; restore all registers
                tay
                pla
                tax
                pla
                rti
