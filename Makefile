# Einzelne Typst-Abbildungen als PNG für HDLab erzeugen.
TYPST ?= typst
PPI ?= 180
SOURCES := $(wildcard diagrams/*.typ)
IMAGES := $(patsubst diagrams/%.typ,images/generated/%.png,$(SOURCES))
LIBRARIES := $(wildcard diagrams/lib/*.typ)

.PHONY: all images rebuild clean
.DELETE_ON_ERROR:
all: images
images: $(IMAGES)

images/generated/%.png: diagrams/%.typ $(LIBRARIES) Makefile | images/generated
	$(TYPST) compile --root . --format png --ppi $(PPI) "$<" "$@"

images/generated:
	mkdir -p "$@"

# Bei geänderter Exportauflösung oder Schriftinstallation vollständig neu bauen.
rebuild:
	$(MAKE) -B images

# Nur abgeleitete Bilder entfernen; ursprüngliche Bilder und Quellen behalten.
clean:
	rm -f $(IMAGES)
