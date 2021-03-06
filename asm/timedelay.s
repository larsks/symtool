; timedelay.s
; implement a time delay using 6532 timer
;
; part of symtool (https://github.com/larsks/symtool)

                .import         ACCESS,SCAND,KYSTAT
                .include        "segments.s"

IFR             =               $A405           ; read interrupt flag
WTIMER1         =               $A41C
WTIMER8         =               $A41D
WTIMER64        =               $A41E
WTIMER1024      =               $A41F

                ; The 6532 timer can be divided by 1, 8, 64, or 1024
                ; (WTIMER1 through WTIMER1024). With WTIMER1, one timer
                ; interval is one clock cycle. At 1Mhz, one clock
                ; cycle is 1μs.
                ;
                ; At WTIMER1024, one timer interval is 1024 clock cycles,
                ; or approx. 1ms.
                ;
                ; That means the longest period will be $FF timer
                ; intervals at WTIMER1024, for a total of 261,120 clock
                ; cycles, or about 0.3 seconds.

                .segment        "ZEROPAGE"
flag:           .byte           0

                .segment        "CODE"

                jsr             ACCESS          ; write-enable system ram
                jsr             show            ; load display buffer
                lda             #$00
                sta             flag

outside:        lda             #$ff            ; initialize timer count
                sta             WTIMER1024      ; start timer
                dec             flag
inside:         lda             flag            ; check bit 0 of flag
                and             #1
                beq             noshow          ; only show message when == 1
                jsr             SCAND           ; flash display

noshow:         bit             IFR             ; check for timer interrupt
                bpl             inside          ; repeat inner loop if no interrupt

                jsr             KYSTAT
                bcs             exit
                jmp             outside         ; repeat outside loop

exit:           rts

show:           lda             #OO     ; O
                sta             D6
                lda             #OD     ; D
                sta             D5
                sta             D4
                lda             #OB     ; B
                sta             D3
                lda             #OI     ; I
                sta             D2
                lda             #OT     ; T
                sta             D1
                rts
