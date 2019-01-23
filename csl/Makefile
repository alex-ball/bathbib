NAME     = bath-csl-test
SHELL    = bash
NEEDLE    = \n\n\n
HAYSTACK = $(NAME).tex

.PHONY: clean distclean

all: $(NAME).html

$(NAME).html: $(NAME).tex $(NAME).yaml
	mkdir -p tmp
	awk 'BEGIN {RS = "\n\n\n"} {print $$0 > "tmp/example_" sprintf("%02d", NR) ".tex"}' $(NAME).tex
	@echo "<!DOCTYPE html>" > $(NAME).html
	@echo "<html><head><meta charset=\"UTF-8\"><title>CSL Test Suite of Examples</title></head><body>" >> $(NAME).html
	for file in tmp/*.tex; do pandoc --filter pandoc-citeproc --bibliography $(NAME).yaml --csl harvard-university-of-bath.csl -t html5 $$file >> $(NAME).html; done
	@echo "</body></html>" >> $(NAME).html

clean:
	rm -rf tmp/

distclean: clean
	rm -f $(NAME).html
