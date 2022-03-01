STYLE = bath
NAME  = biblatex-$(STYLE)
TEST  = test-output
COMP  = test-compat
SHELL = bash
PWD   = $(shell pwd)
TEMP := $(shell mktemp -d -t tmp.XXXXXXXXXX)
TDIR  = $(TEMP)/$(NAME)
VERS  = $(shell ltxfileinfo -v $(NAME).dtx)
LOCAL = $(shell kpsewhich --var-value TEXMFLOCAL)
UTREE = $(shell kpsewhich --var-value TEXMFHOME)
AUX   = aux bbl bcf blg fdb_latexmk fls listing log out run.xml

.PHONY: source clean distclean inst install uninst uninstall zip ctan
.INTERMEDIATE: $(TEST).pdf $(COMP).tex $(COMP).pdf

all:	$(NAME).pdf clean
	@exit 0

source:	$(NAME).dtx
	luatex -interaction=batchmode $< >/dev/null

$(STYLE).bbx $(STYLE).cbx $(STYLE).dbx english-$(STYLE).lbx british-$(STYLE).lbx $(NAME).bib: source

$(NAME).pdf: $(NAME).dtx
	latexmk -silent -lualatex -interaction=batchmode $< >/dev/null
	@echo "Compilation complete."

$(TEST).pdf: $(TEST).tex $(STYLE).bbx $(NAME).bib
	latexmk -silent -lualatex -interaction=batchmode $< >/dev/null

$(TEST).bbi: $(TEST).pdf
	pdftotext $< $@

$(COMP).tex: $(TEST).tex
	sed 's/biblatex-bath.bib/..\/bst\/bath-bst.bib/' $< > $@

$(COMP).pdf: $(COMP).tex $(STYLE).bbx
	latexmk -silent -lualatex -interaction=batchmode $< >/dev/null

$(COMP).bbi: $(COMP).pdf
	pdftotext $< $@

clean:
	rm -f $(AUX:%=$(NAME).%) $(NAME).markdown.in
	rm -rf _markdown_$(NAME)
	rm -f $(AUX:%=$(TEST).%) $(AUX:%=$(COMP).%)

distclean: clean
	rm -f $(NAME).{pdf,bib,ins} $(STYLE).{b,c,d}bx {english,british}-$(STYLE).lbx {$(TEST),$(COMP)}.bbi


inst: all
	mkdir -p $(UTREE)/{source,tex,doc}/latex/$(NAME)
	cp $(NAME).dtx $(NAME).ins $(UTREE)/source/latex/$(NAME)
	cp $(NAME).{bib,pdf} $(UTREE)/doc/latex/$(NAME)
	cp $(STYLE).{b,c,d}bx {english,british}-$(STYLE).lbx $(UTREE)/tex/latex/$(NAME)
	mktexlsr

uninst:
	rm -r $(UTREE)/{source,tex,doc}/latex/$(NAME)
	mktexlsr

install: all
	sudo mkdir -p $(LOCAL)/{source,tex,doc}/latex/$(NAME)
	sudo cp $(NAME).dtx $(NAME).ins $(LOCAL)/source/latex/$(NAME)
	sudo cp $(NAME).{bib,pdf} $(LOCAL)/doc/latex/$(NAME)
	sudo cp $(STYLE).{b,c,d}bx {english,british}-$(STYLE).lbx $(LOCAL)/tex/latex/$(NAME)
	mktexlsr

uninstall:
	sudo rm -r $(LOCAL)/{source,tex,doc}/latex/$(NAME)
	mktexlsr

zip: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,bib,pdf} $(STYLE).{b,c,d}bx {english,british}-$(STYLE).lbx README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)

ctan: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,pdf} README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)
