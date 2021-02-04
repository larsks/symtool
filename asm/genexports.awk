#!/usr/bin/awk -E

# Generate ca65 .export directives for symbols in the source file

/^[A-Z][A-Z0-9]+ += +\$[A-F0-9]+/ {printf "                .export    %s\n", $1}
