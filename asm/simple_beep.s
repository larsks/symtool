; simple_beep.s
; beep periodically until a key is pressed
;
; part of symtool (https://github.com/larsks/symtool)

        .import         BEEP,KYSTAT

main:   ldx             #$ff
        ldy             #$ff

loop:   jsr		delay
        jsr             BEEP
        clc
	jsr             KYSTAT		; check for key down
	bcc             main		; continue if no key down

	ldy		#$ff
	jsr		delay
	jsr		BEEP		; two short beeps to confirm
	ldy		#$01		; exit
	jsr		delay
	jsr		BEEP
        rts

delay:  dex                             ; for i in range(Y):
	bne             delay           ;    for j in range(X):
	dey                             ;        ...
	bne             delay
	rts
