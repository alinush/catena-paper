TEXNAME=catena-paper
PDFNAME=catena-paper

all: pdf

pdf: clean eps svg latexmk

svg: figs/overview.pdf figs/bitcoin.pdf figs/txfee-estimates.pdf figs/communication.pdf figs/non-equiv.pdf figs/refunding.pdf

eps: figs/overview.eps figs/bitcoin.eps figs/txfee-estimates.eps figs/communication.eps figs/non-equiv.eps figs/refunding.eps

figs/%.eps: figs/%.svg
	inkscape -D -z --file=$(realpath $<) --export-eps=$(realpath .)/$@

figs/%.pdf: figs/%.svg
	inkscape -D -z --file=$(realpath $<) --export-dpi=300 --export-pdf=$(realpath .)/$@

latexmk: latexmk_clean
	# For some reason using -auxdir=build/ will result in failed builds
	latexmk -pdf ${TEXNAME}
	mv ${TEXNAME}.pdf ${PDFNAME}.pdf

texi2pdf: texi2pdf_clean
	texi2pdf --build-dir=build/ ${TEXNAME}.tex -o ${PDFNAME}.pdf

clean: texi2pdf_clean latexmk_clean
	rm -f ${PDFNAME}.pdf
	rm -f catena-paper-diffjay-revision*

latexmk_clean:
	rm -f *.fls *.fdb_latexmk *.dvi *.synctex.gz *.bcf

texi2pdf_clean:
	rm -rf build/
	rm -f *.aux *.blg *.lof *.lot *.log *.bbl *.blg *.toc *.out

open:
	xdg-open ${PDFNAME}.pdf
