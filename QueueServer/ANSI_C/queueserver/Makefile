# Makefile

ONTOLOGY_SOURCE := ../../SmartSlog_lib/SmartRoomOntology.c
ONTOLOGY_HEADER := ../../SmartSlog_lib/SmartRoomOntology.h
ONTOLOGY_OBJECT := ../../SmartSlog_lib/SmartRoomOntology.o

pkg_packages := scew smartslog ckpi

PKG_CFLAGS  := $(shell pkg-config --cflags $(pkg_packages))
PKG_LDFLAGS := $(shell pkg-config --libs $(pkg_packages))

INCLUDES :=
LIBS :=

CC    := gcc

DEBUG := -g
EXTRA_FLAGS :=
EXTRA_OPTION := -std=c99

CFLAGS := -c $(DEBUG) $(INCLUDES) $(PKG_CFLAGS) $(EXTRA_FLAGS)
LFLAGS := $(DEBUG) $(PKG_LDFLAGS) $(LIBS)

PROGRAM_NAME := queueserver

targets = main

o_files :=  ./queueserver.o \
		    $(ONTOLOGY_OBJECT)

.PHONY: all
all : $(targets)

main: $(o_files)
	$(CC) $(o_files) -o $(PROGRAM_NAME) $(EXTRA_OPTION) $(LFLAGS)

.c.o:
	$(CC) $(EXTRA_OPTION) $(CFLAGS) -o $@ $<


.PHONY: clean
clean:
	rm -f *.o
	rm -f $(PROGRAM_NAME)
