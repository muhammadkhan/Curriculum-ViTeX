LC=pdflatex
NAME=Curriculum-ViTeX

all: $(NAME).pdf

%.pdf: %.tex
	$(LC) $<

.PHONY: clean

clean:
	rm *.aux
	rm *.log
	rm *.out
	rm $(NAME).pdf
