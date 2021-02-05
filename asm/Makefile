CA65 = ca65
LD65 = ld65
AWK = awk
ENSCRIPT = enscript

PRGS = \
       simple_beep.bin \
       message.bin \
       countdown.bin \
       timedelay.bin \
       beeper.bin

SOURCES = \
	simple_beep.s \
	countdown.s \
	libsym.s \
	message.s \
	monitor.s \
	segments.s \
	timedelay.s \
	beeper.s

DEPS = $(SOURCES:.s=.d)

GENERATED = \
	$(PRGS)

# make with V=1 to enable verbose output
ifeq ($(V),1)
	Q=
	ECHO=@:
else
	Q=@
	ECHO=@echo
endif

%.o %.lst: %.s
	$(ECHO) "ASSEMBLE $^ -> $@"
	$(@)$(CA65) $(CA65FLAGS) -g -t none -o $@ -l $(@:.o=.lst) $<

%.x: %.s genexports.awk
	$(ECHO) "EXPORTS $^ -> $@"
	$(Q)$(AWK) -f genexports.awk $< > $@ || { rm -f $@; false; }

%.d: %.s
	$(ECHO) "DEPS $^ -> $@"
	$(Q)$(CA65) --create-dep $@ $<

%.r: %.lbl genflags.awk
	$(ECHO) "FLAGS $^ -> $@"
	$(Q)$(AWK) -f genflags.awk $< > $@ || { rm -f $@; false; }

%.ps: %.lst
	$(ECHO) "PS $^ -> $@"
	$(Q)$(ENSCRIPT) -o $@ -r $<

%.bin: %.o libsym.o
	$(ECHO) "LINK $^ -> $@"
	$(Q)$(LD65)  $(LD65FLAGS) \
		-C sym1.cfg \
		-Ln $(<:.o=.lbl) \
		-o $@ $^

all: $(GENERATED)

clean:
	rm -f $(GENERATED) *.lst *.lbl *.o *.x *.d *.r

.PRECIOUS: libsym.o

libsym.d: monitor.x

include $(DEPS)
