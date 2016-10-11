NAME  = biblatex-bath
BBX   = bath.bbx
SHELL = bash
PWD   = $(shell pwd)
TEMP := $(shell mktemp -d -t tmp.XXXXXXXXXX)
TDIR  = $(TEMP)/$(NAME)
VERS  = $(shell ltxfileinfo -v $(NAME).dtx)
LOCAL = $(shell kpsewhich --var-value TEXMFLOCAL)
UTREE = $(shell kpsewhich --var-value TEXMFHOME)

.PHONY: source clean distclean inst install uninst uninstall zip ctan

all:	$(NAME).pdf $(BBX) clean
	@exit 0

source:	$(BBX) $(NAME).bib

$(BBX) $(NAME).bib: $(NAME).dtx
	tex -interaction=batchmode $(NAME).dtx >/dev/null

$(NAME).pdf: $(NAME).dtx $(BBX) $(NAME).bib
	lualatex -interaction=batchmode $(NAME).dtx >/dev/null
	biber $(NAME) >/dev/null
	latexmk -silent -lualatex -interaction=batchmode $(NAME).dtx >/dev/null

clean:
	rm -f $(NAME).{aux,bbl,bcf,blg,doc,fdb_latexmk,fls,glo,gls,hd,idx,ilg,ind,listing,log,nav,out,run.xml,snm,synctex.gz,tcbtemp,toc,vrb}
	rm -rf _markdown_$(NAME)

distclean: clean
	rm -f $(NAME).{pdf,bib,ins} $(BBX)


inst: all
	mkdir -p $(UTREE)/{source,tex,doc}/latex/$(NAME)
	cp $(NAME).dtx $(NAME).ins $(UTREE)/source/latex/$(NAME)
	cp $(NAME).{bib,pdf} $(UTREE)/doc/latex/$(NAME)
	cp $(BBX) $(UTREE)/tex/latex/$(NAME)
	mktexlsr

uninst:
	rm -r $(UTREE)/{source,tex,doc}/latex/$(NAME)
	mktexlsr

install: all
	sudo mkdir -p $(LOCAL)/{source,tex,doc}/latex/$(NAME)
	sudo cp $(NAME).dtx $(NAME).ins $(LOCAL)/source/latex/$(NAME)
	sudo cp $(NAME).{bib,pdf} $(LOCAL)/doc/latex/$(NAME)
	sudo cp $(BBX) $(LOCAL)/tex/latex/$(NAME)
	mktexlsr

uninstall:
	sudo rm -r $(UTREE)/{source,tex,doc}/latex/$(NAME)
	mktexlsr

zip: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,bib,pdf} $(BBX) README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)

ctan: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,pdf} README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)
