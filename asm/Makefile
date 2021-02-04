CA65 = ca65
LD65 = ld65
AWK = awk
ENSCRIPT = enscript

PRGS = \
       beeper.bin \
       message.bin \
       countdown.bin \
       timedelay.bin

SOURCES = \
	beeper.s \
	countdown.s \
	libsym.s \
	message.s \
	monitor.s \
	segments.s \
	timedelay.s

DEPS = $(SOURCES:.s=.d)

GENERATED = \
	$(PRGS)

%.o: %.s
	$(CA65) $(CA65FLAGS) -g -t none -o $@ -l $(@:.o=.lst) $<

%.x: %.s genexports.awk
	$(AWK) -f genexports.awk $< > $@ || { rm -f $@; false; }

%.d: %.s gendeps.awk
	$(AWK) -f gendeps.awk $< > $@ || { rm -f $@; false; }

%.pdf: %.lst
	$(ENSCRIPT) -o $@ -r $<

%.bin: %.o libsym.o
	$(LD65)  $(LD65FLAGS) \
		-C sym1.cfg \
		-Ln $(<:.o=.lbl) \
		-o $@ $^

all: $(GENERATED)

clean:
	rm -f $(GENERATED) *.lst *.lbl *.o *.x *.d

.PRECIOUS: libsym.o

libsym.o: monitor.s monitor.x

include $(DEPS)
