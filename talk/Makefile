sources := $(wildcard *.md)
objects := $(sources:.md=.html)

css := presentation.css

all: $(objects)

%.html: %.md
	pandoc \
		-t revealjs \
		-s $< \
		--css=$(css) \
		-o $@

clean:
	rm -f *.html
