#!/usr/bin/awk -E

# Generate Make dependencies for included files

BEGIN {FS="\""}

/\.include/ {
	deps[$2] = $2
}

END {
	obj=gensub("\\.s", ".o", "g", FILENAME)
	depfile=gensub("\\.s", ".d", "g", FILENAME)
	printf("%s %s: %s ", obj, depfile, FILENAME)
	for (dep in deps) {
		printf "%s ", dep
	}
	printf "\n"
}
