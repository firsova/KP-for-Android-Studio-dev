# Makefile

DIRS := queueserver 

.PHONY: all

all: dirs

dirs:
	for dir in $(DIRS); do $(MAKE) -C$$dir; done

.PHONY: clean

clean:
	for dir in $(DIRS); do $(MAKE) -C$$dir clean; done

