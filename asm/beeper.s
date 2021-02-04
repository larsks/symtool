; beeper.s
;
; This is "Program #1 - Beeper Demo" from page 10 of the SYM-1 "Technical
; Notes" document
; (http://www.6502.org/trainers/synertek/manuals/technotes.pdf)
;
; part of symtool (https://github.com/larsks/symtool)

                .import         CONFIG,IRQVEC,ACCESS

                                                ; registers on 6532
PBDA            =               $A402           ; beeper data register
PBDDR           =               $A403           ; beeper data direction register
IER1            =               $AC0E           ; enable interrupt flag
IFR1            =               $AC0D           ; read interrupt flag
ACR1            =               $AC0B           ; set up timer interrupt
T1LL1           =               $AC06           ; timer low byte
T1CH1           =               $AC05           ; timer high byte

                .segment        "ZEROPAGE"

tone:           .byte           0               ; tone storage
length:         .byte           0               ; note length

                .segment        "CODE"

start:          sei                             ; disable interrupts
                jsr             ACCESS          ; write enable system ram

                lda             #<intrpt        ; store address of intrpt
                sta             IRQVEC          ; in IRQVEC
                lda             #>intrpt
                sta             IRQVEC+1

                lda             #$0f            ; configure DDR
                sta             PBDDR

                lda             #$ff            ; initialize tone
                sta             tone

                lda             #$01            ; initialize tone length
                sta             length

                lda             #$40            ; configure interrupt timer
                sta             ACR1            ; without having square waves

                lda             #$c0            ; enable the interrupt flag
                sta             IER1

                lda             #$40            ; clear any pending flags
                sta             IFR1

                lda             #$20            ; start the timer
                sta             T1LL1
                sta             T1CH1

beeper:         lda             #$0d            ; configure for the beeper
                jsr             CONFIG

                cli                             ; enable interrupts
                                                ; start the "music?"

be1:            lda             #$08            ; turn beeper on
                sta             PBDA
                jsr             be2             ; wait awhile
                lda             #$06            ; turn beeper off
                sta             PBDA
                jsr             be2             ; wait again
                bcc             be1             ; and repeat

be2:            ldy             tone            ; delay routine
be3:            dey                             ; count down
                bne             be3             ; until zero

                rts

intrpt:         pha                             ; save a register
                tya                             ; save y register
                pha

                lda             #$40            ; clear pending interrupt flag
                sta             IFR1

                dec             length          ; count down each note length
                bne             return          ; if not zero return

                lda             #$01            ; restore length
                sta             length

                dec             tone            ; make a higher note
                lda             tone            ; is it high enough?
                cmp             #$10            ; 10 should be a limit
                bcs             return          ; it not 10, go back

                lda             #$ff            ; restore to lowest note
                sta             tone

return:         pla                             ; restore y register
                tay
                pla                             ; restore a register

                rti                             ; return from interrupt
