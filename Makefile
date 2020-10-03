# Makefile
TARGETS=ampy.html

.PHONY: all clean

all: $(TARGETS)

clean:
	$(RM) $(TARGETS)

%.html : %.md
	pandoc -s -c mipandoc.css $< -o $@
