SHELL    = bash
NAME     = bath-csl-test
CSL      = harvard-university-of-bath.csl
NEEDLE   = \n\n\n
HAYSTACK = $(NAME).tex

.PHONY: clean distclean

all: $(NAME).html

tmp/example_01.tex: $(NAME).tex
	mkdir -p tmp
	awk 'BEGIN {RS = "\n\n\n"} {print $$0 > "tmp/example_" sprintf("%02d", NR) ".tex"}' $(NAME).tex

$(NAME).html: tmp/example_01.tex $(NAME).yaml $(CSL)
	@echo "<!DOCTYPE html>" > $(NAME).html
	@echo "<html><head><meta charset=\"UTF-8\"><title>CSL Test Suite of Examples</title></head><body>" >> $(NAME).html
	for file in tmp/*.tex; do sed -i 's/\\@//g' $$file; pandoc --filter pandoc-citeproc --bibliography $(NAME).yaml --csl $(CSL) -t html5 $$file >> $(NAME).html; done
	@echo "</body></html>" >> $(NAME).html

clean:
	rm -rf tmp/

distclean: clean
	rm -f $(NAME).html
