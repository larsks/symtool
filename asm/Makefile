CA65 = ca65
LD65 = ld65

PRGS = \
       beeper.bin \
       message.bin \
       countdown.bin \
       timedelay.bin

GENERATED = \
	$(PRGS)

%.o: %.s
	$(CA65) $(CA65FLAGS) -g -t none -o $@ -l $(@:.o=.lst) $<

%.bin: %.o
	$(LD65)  $(LD65FLAGS) \
		-C sym1.cfg \
		-Ln $(<:.o=.lbl) \
		-o $@ $^

all: $(GENERATED)

clean:
	rm -f $(GENERATED) *.lst *.lbl *.o
