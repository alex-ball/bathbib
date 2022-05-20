SHELL    = bash
NAME     = bath-csl-test
CSL      = harvard-university-of-bath.csl

.PHONY: clean distclean
.INTERMEDIATE: $(NAME)-raw.html $(NAME)-tmp.yaml $(NAME)-input.json $(NAME)-output.json

all: $(NAME).html $(NAME)-js.html clean

tmp/example_01.tex: $(NAME).tex
	rm -rf tmp/
	mkdir tmp
	awk 'BEGIN {RS = "\n\n\n"} {print $$0 > "tmp/example_" sprintf("%02d", NR) ".tex"}' $<

$(NAME)-tmp.yaml: $(NAME).yaml
	sed 's/@/\\@/g' $(NAME).yaml > $(NAME)-tmp.yaml

$(NAME)-raw.html: tmp/example_01.tex $(NAME)-tmp.yaml $(CSL)
	@echo "<!DOCTYPE html>" > $@
	@echo "<html><head><meta charset=\"UTF-8\"><title>CSL Test Suite of Examples</title><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></head><body>" >> $@
	for file in tmp/*.tex; do sed -i 's/\\textup/\\textrm/g' $$file; sed -E -i 's/\\enquote\{([^}]*)\}/‘\1’/g' $$file; pandoc --wrap=preserve --citeproc --bibliography $(NAME)-tmp.yaml --variable lang=en-GB --csl $(CSL) -t html5 $$file >> $@; done
	@echo "</body></html>" >> $@

$(NAME).html: $(NAME)-raw.html check-output.py
	./check-output.py $< $@

$(NAME)-input.json: $(NAME).yaml $(CSL) yaml2json.py
	./yaml2json.py -o $@ -s $(CSL) $<

$(NAME)-output.json: $(NAME)-input.json
	curl --header "Content-type: application/json" --data @$< -X POST 'http://127.0.0.1:8085?responseformat=json&locale=en-GB&linkwrap=1&citations=1' > $@

$(NAME)-js.html: $(NAME)-output.json $(NAME)-raw.html check-output.py
	./check-output.py $< $@

clean:
	rm -rf tmp/
	rm -f $(NAME)-raw.html $(NAME)-tmp.yaml $(NAME)-input.json $(NAME)-output.json

distclean: clean
	rm -f $(NAME).html $(NAME)-js.html
