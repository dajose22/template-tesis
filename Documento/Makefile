# Document options
DOCUMENT?=main

# LaTeX options
LATEX?=/usr/bin/pdflatex
LATEX_OPT?=-interaction nonstopmode -shell-escape $(DOCUMENT)
LATEX_TEMPLATE?=template.tex
LATEX_RST?=../rst2TECtex/rst2TECxetex
LATEX_RST_OPT?=--traceback --template=$(LATEX_TEMPLATE) --documentclass=book --no-doc-title  --smart-quotes=yes $(DOCUMENT).rst


DOTFILES = $(wildcard fig/*.dot)
GPLOTFILES = $(wildcard fig/*.gplot)
EGPLOTFILES = $(patsubst %.gplot,%.pdf,$(GPLOTFILES))
EDOTFILES = $(patsubst %.dot,%.pdf,$(DOTFILES))
PDFFILES = $(wildcard fig/*.pdf)  $(EDOTFILES)   $(EGPLOTFILES)

# for pdf from graphviz files
fig/%.pdf : fig/%.dot
	@echo "Generating $@ from $< " ; \
	dot -Tpdf $< > $@

# for pdf from gplot files
fig/%.pdf : fig/%.gplot
	@echo "Generating $@ from $< " ; \
	cd fig; gnuplot ../$<


all:  $(PDFFILES) pdf

clean:
	rm -rf $(DOCUMENT).tex *.lot *.toc *.lof *.out *.aux *.bbl *.blg *.log acta.pdf
	@cd fig; \
	for i in `find . -name "*.dot"` ; do \
	  b=`basename $$i .dot`.pdf ;\
	  if [ -f $$b ] ; then \
	    rm $$b ;\
	  fi ;\
	done
	@cd fig; \
	for i in `find . -name "*.gplot"` ; do \
	  b=`basename $$i .gplot`.pdf ;\
	  if [ -f $$b ] ; then \
	    rm $$b ;\
	  fi ;\
	done ;\

clean-all: clean
	rm -f $(DOCUMENT).pdf

pdf:
	libreoffice --headless --convert-to pdf acta.doc
	# Convert reStructuredText to LaTeX (xelatex)
	$(LATEX_RST) $(LATEX_RST_OPT) > $(DOCUMENT).tex
	# Compile LaTeX
	$(LATEX) $(LATEX_OPT); \
	bibtex main.aux; \
	$(LATEX) $(LATEX_OPT); \
	$(LATEX) $(LATEX_OPT)




