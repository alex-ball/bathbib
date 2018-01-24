NAME  = bath-bst
BST   = bath.bst
SHELL = bash
PWD   = $(shell pwd)
TEMP := $(shell mktemp -d -t tmp.XXXXXXXXXX)
TDIR  = $(TEMP)/$(NAME)
VERS  = $(shell ltxfileinfo -v $(NAME).dtx)
LOCAL = $(shell kpsewhich --var-value TEXMFLOCAL)
UTREE = $(shell kpsewhich --var-value TEXMFHOME)

.PHONY: source clean distclean inst install uninst uninstall zip ctan

all:	$(BST) $(NAME)-v1.pdf $(NAME).pdf clean
	@exit 0

source:	$(BST) $(NAME).bib $(NAME)-v1.tex $(NAME)-v1.bib

$(BST) $(NAME).bib  $(NAME)-v1.tex $(NAME)-v1.bib: $(NAME).dtx
	luatex -interaction=batchmode $(NAME).dtx >/dev/null

$(NAME).pdf: $(NAME).dtx $(BST) $(NAME).bib
	latexmk -silent -lualatex -synctex=1 -interaction=batchmode $(NAME).dtx >/dev/null
	@echo "Compilation of main PDF complete."

$(NAME)-v1.pdf: $(NAME)-v1.tex $(BST) $(NAME)-v1.bib
	latexmk -silent -lualatex -synctex=1 -interaction=batchmode $(NAME)-v1.tex >/dev/null
	@echo "Compilation of test PDF complete."

clean:
	rm -f $(NAME){,-v1}.{aux,bbl,bcf,blg,doc,fdb_latexmk,fls,glo,gls,hd,idx,ilg,ind,listing,log,nav,out,run.xml,snm,synctex.gz,tcbtemp,toc,vrb}
	rm -f $(NAME){,-v1}.markdown.in
	rm -rf _markdown_$(NAME)

distclean: clean
	rm -f $(NAME).{pdf,bib,ins} $(BST) $(NAME)-v1.{pdf,bib,tex}

inst: all
	mkdir -p $(UTREE)/{source,doc}/bibtex/$(NAME)
	mkdir -p $(UTREE)/bibtex/bst/$(NAME)
	cp $(NAME).dtx $(NAME).ins $(UTREE)/source/bibtex/$(NAME)
	cp $(NAME).{bib,pdf} $(UTREE)/doc/bibtex/$(NAME)
	cp $(BST) $(UTREE)/bibtex/bst/$(NAME)
	mktexlsr

uninst:
	rm -r $(UTREE)/{source,doc}/bibtex/$(NAME)
	rm -r $(UTREE)/bibtex/bst/$(NAME)
	mktexlsr

install: all
	sudo mkdir -p $(LOCAL)/{source,doc}/bibtex/$(NAME)
	sudo mkdir -p $(LOCAL)/bibtex/bst/$(NAME)
	sudo cp $(NAME).dtx $(NAME).ins $(LOCAL)/source/bibtex/$(NAME)
	sudo cp $(NAME).{bib,pdf} $(LOCAL)/doc/bibtex/$(NAME)
	sudo cp $(BST) $(LOCAL)/bibtex/bst/$(NAME)
	mktexlsr

uninstall:
	sudo rm -r $(UTREE)/{source,doc}/bibtex/$(NAME)
	sudo rm -r $(UTREE)/bibtex/bst/$(NAME)
	mktexlsr

zip: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,bib,pdf} $(BST) README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)

ctan: all
	mkdir $(TDIR)
	cp $(NAME).{dtx,pdf} README.md Makefile $(TDIR)
	cd $(TEMP); zip -Drq $(PWD)/$(NAME)-$(VERS).zip $(NAME)
