; monitor.s
; monitor routines and constants from the sym-1 reference manual
;
; part of symtool (https://github.com/larsks/symtool)

; ======================================================================
; MONITOR ROUTINES
;

SAVINT          =       $8064           ; save user regs after interrupt
DBOFF           =       $80D3           ; simulates debug off
DBON            =       $80E4           ; simulates debug on
DBNEW           =       $80F6           ; release debug to key control
GETCOM          =       $80FF           ; get command and 0-3 parameters
DISPAT          =       $814A           ; dispatch monitor command
ERMSG           =       $8171           ; if carry set, print ERNN
SAVER           =       $8188           ; save all registers on stack
INBYTE          =       $81D9           ; get two hex digits into A
PSHOVE          =       $8208
PARM            =       $8220
ASCNIB          =       $8275           ; ascii in A to lo nibble of A
OUTPC           =       $82EE
OUTXAH          =       $82F4
OUTBYT          =       $82FA           ; output two hex digits from a
NIBASC          =       $8309           ; lo niblle of A to ascii in A
COMMA           =       $833A
SPACE           =       $8342
CRLF            =       $834D
DELAY           =       $835A
INSTAT          =       $8386           ; check if key down or BREAK
GETKEY          =       $88AF           ; read hex keyboard to A
HDOUT           =       $8900           ; ascii character from A to hex display
SCAND           =       $8906           ; scan display from DISBUF
KEYQ            =       $8923
KYSTAT          =       $896A
BEEP            =       $8972           ; make a sound on onboard beeper
CONFIG          =       $89A5           ; configure i/o
HKEY            =       $89BE           ; get key from hex keyboard and echo in DISBUF
OUTDSP          =       $89C1           ; convert ascii to segment code, put in DISBUF
TEXT            =       $8A06
INCHR           =       $8A1B           ; get character, convert to upper case
NBASOC          =       $8A44
OUTCHR          =       $8A47           ; output ascii from A
INTCHR          =       $8A58
TSTAT           =       $8B3C
ACCESS          =       $8B86
NACCESS         =       $8B9C

; ======================================================================
; SYSTEM RAM
;

RDIG            =       $A645
DISBUF          =       $A640
D1              =       $A645
D2              =       $A644
D3              =       $A643
D4              =       $A642
D5              =       $A641
D6              =       $A640
TECHO           =       $A653           ; terminal echo
SDBYT           =       $A651           ; baud rate
TOUTFL          =       $A654           ; in/out enable flags

; ======================================================================
; VECTORS
;

INVEC           =       $A660           ; input vector
OUTVEC          =       $A663           ; output vector
INSVEC          =       $A666           ; in status vector
URSVEC          =       $A669           ; unrecognized syntax vector
URCVEC          =       $A66C           ; unrecognized command vector
SCNVEC          =       $A66F           ; display scan vector
IRQVEC          =       $A67E           ; interrupt vector


; ======================================================================
; TABLES
;

ASCIITBL        =       $8BEF           ; ASCII codes and hash codes
SEGTBL          =       $8C29           ; LED segment codes

; jump table (for use with monitor "j" command)
JUMPTBL         =       $A620
JTABLE_7        =       $A62E           ; user socket p1
JTABLE_6        =       $A62C           ; user socket p2
JTABLE_5        =       $A62A           ; $300
JTABLE_4        =       $A628           ; $200
JTABLE_3        =       $A626           ; $000
JTABLE_2        =       $A624           ; newdev
JTABLE_1        =       $A622           ; tty
JTABLE_0        =       $A620           ; basic

; ======================================================================
; CONSTANTS
;

; SDBYT
B110            =       $D5
B300            =       $4C
B600            =       $24
B1200           =       $10
B2400           =       $06
B4800           =       $01

; TECHO
F_ECHO          =       %10000000       ; 0=disable echo, 1=enable echo
F_OUTPUT        =       %01000000       ; 0=enable output, 1=disable output

; TOUTFL
F_CRT_IN        =       %10000000
F_TTY_IN        =       %01000000
F_TTY_OUT       =       %00100000
F_CRT_OUT       =       %00010000
