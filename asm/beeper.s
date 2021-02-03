; beep periodically until a key is pressed
;
        .include        "monitor.s"

main:   ldx             #$ff
        ldy             #$ff

loop:   dex                             ; for y in range(0xff):
        bne             loop            ;    for x in range(0xff):
        dey                             ;        pass
        bne             loop

        jsr             BEEP
        clc
        jsr             KYSTAT
        bcc             main
        rts
