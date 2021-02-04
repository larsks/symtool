#!/usr/bin/awk E

# convert vice labels file to flags for radare2

BEGIN {print "fs symbols"}
{printf "f sym.%s=0x%s\n", substr($3, 2), $2}
