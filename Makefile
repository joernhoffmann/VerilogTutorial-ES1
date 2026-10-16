# Kapitelweise Typst-/SVG-Quellen als PNG für HDLab erzeugen.
TYPST ?= typst
PPI ?= 180
TYPST_SOURCES := $(wildcard diagrams/[0-9][0-9]-*/*.typ)
SVG_SOURCES := $(wildcard diagrams/[0-9][0-9]-*/*.svg)
IMAGES := $(patsubst diagrams/%.typ,images/%.png,$(TYPST_SOURCES)) \
          $(patsubst diagrams/%.svg,images/%.png,$(SVG_SOURCES))
LIBRARIES := $(wildcard diagrams/lib/*.typ)

.PHONY: all images rebuild clean
.DELETE_ON_ERROR:
all: images
images: $(IMAGES)

images/%.png: diagrams/%.typ $(LIBRARIES) Makefile
	mkdir -p "$(@D)"
	$(TYPST) compile --root . --format png --ppi $(PPI) "$<" "$@"

# SVG-Geometrie bleibt als eigenständige, editierbare Quelldatei erhalten.
# Typst rendert sie ohne weiteren Konverter in ein HDLab-kompatibles PNG.
images/%.png: diagrams/%.svg $(LIBRARIES) Makefile
	mkdir -p "$(@D)"
	$(TYPST) compile --root . --input 'svg=/diagrams/$*.svg' --format png --ppi $(PPI) diagrams/lib/svg.typ "$@"

# Bei geänderter Exportauflösung oder Schriftinstallation vollständig neu bauen.
rebuild:
	$(MAKE) -B images

# Nur abgeleitete Bilder entfernen; ursprüngliche Bilder und Quellen behalten.
clean:
	rm -f $(IMAGES)

# Prüfhilfen in die eigenständigen Markdown-Testbenches übernehmen.
.PHONY: testbenches check-testbenches check-testbenches-verilator
testbenches:
	python3 scripts/sync_test_helpers.py

check-testbenches:
	python3 scripts/check_testbenches.py

check-testbenches-verilator:
	python3 scripts/check_testbenches.py --verilator

.PHONY: check check-course check-testbenches-iverilog
check: check-course check-testbenches

check-course:
	python3 scripts/check_course.py

check-testbenches-iverilog:
	python3 scripts/check_testbenches.py --iverilog
