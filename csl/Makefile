SHELL    = bash
NAME     = bath-csl-test
CSL      = harvard-university-of-bath.csl

.PHONY: clean distclean

all: $(NAME).html

tmp/example_01.tex: $(NAME).tex
	mkdir -p tmp
	awk 'BEGIN {RS = "\n\n\n"} {print $$0 > "tmp/example_" sprintf("%02d", NR) ".tex"}' $<

$(NAME)-raw.html: tmp/example_01.tex $(NAME).yaml $(CSL)
	@echo "<!DOCTYPE html>" > $@
	@echo "<html><head><meta charset=\"UTF-8\"><title>CSL Test Suite of Examples</title><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></head><body>" >> $@
	for file in tmp/*.tex; do sed -i 's/\\@//g' $$file; sed -i 's/\\textup/\\textrm/g' $$file; sed -E -i 's/\\enquote\{([^}]*)\}/‘\1’/g' $$file; pandoc --filter pandoc-citeproc --bibliography $(NAME).yaml --variable lang=en-GB --csl $(CSL) -t html5 $$file >> $@; done
	@echo "</body></html>" >> $@

$(NAME).html: $(NAME)-raw.html check-output.py
	./check-output.py

clean:
	rm -rf tmp/
	rm $(NAME)-raw.html

distclean: clean
	rm -f $(NAME).html
