STYLE = bath
NAME  = biblatex-$(STYLE)
SHELL = bash
PWD   = $(shell pwd)
TEMP := $(shell mktemp -d -t tmp.XXXXXXXXXX)
TDIR  = $(TEMP)/$(NAME)
VERS  = $(shell ltxfileinfo -v $(NAME).dtx)
LOCAL = $(shell kpsewhich --var-value TEXMFLOCAL)
UTREE = $(shell kpsewhich --var-value TEXMFHOME)

.PHONY: source clean distclean inst install uninst uninstall zip ctan

all:	$(NAME).pdf clean
	@exit 0

source:	$(NAME).dtx
	tex -interaction=batchmode $(NAME).dtx >/dev/null

$(STYLE).bbx $(STYLE).cbx $(STYLE).dbx american-$(STYLE).lbx british-$(STYLE).lbx $(NAME).bib: source

$(NAME).pdf: source
	lualatex -interaction=batchmode $(NAME).dtx >/dev/null
	biber $(NAME) >/dev/null
	latexmk -silent -lualatex -interaction=batchmode $(NAME).dtx >/dev/null

clean:
	rm -f $(NAME).{aux,bbl,bcf,blg,doc,fdb_latexmk,fls,glo,gls,hd,idx,ilg,ind,listing,log,nav,out,run.xml,snm,synctex.gz,tcbtemp,toc,vrb}
	rm -rf _markdown_$(NAME)

distclean: clean
	rm -f $(NAME).{pdf,bib,ins} $(STYLE).{b,c,d}bx {american,british}-$(STYLE).lbx


inst: all
	mkdir -p $(UTREE)/{source,tex,doc}/latex/$(NAME)
	cp $(NAME).dtx $(NAME).ins $(UTREE)/source/latex/$(NAME)
	cp $(NAME).{bib,pdf} $(UTREE)/doc/latex/$(NAME)
	cp $(STYLE).{b,c,d}bx {american,british}-$(STYLE).lbx $(UTREE)/tex/latex/$(NAME)
	mktexlsr

uninst:
	rm -r $(UTREE)/{source,tex,doc}/latex/$(NAME)
	mktexlsr

install: all
	sudo mkdir -p $(LOCAL)/{source,tex,doc}/latex/$(NAME)
	sudo cp $(NAME).dtx $(NAME).ins $(LOCAL)/source/latex/$(NAME)
	sudo cp $(NAME).{bib,pdf} $(LOCAL)/doc/latex/$(NAME)
	sudo cp $(STYLE).{b,c,d}bx {american,british}-$(STYLE).lbx $(LOCAL)/tex/latex/$(NAME)
	mktexlsr

uninstall:
	sudo rm -r $(UTREE)/{source,tex,doc}/latex/$(NAME)
	mktexlsr

zip: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,bib,pdf} $(STYLE).{b,c,d}bx {american,british}-$(STYLE).lbx README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)

ctan: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,pdf} README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)
