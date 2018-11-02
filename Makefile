SHELL:=/bin/bash

include .env

.PHONY: clean
clean:
	make  -f Makefile.targets $(MAKECMDGOALS) $(MAKEFLAGS)
	
.PHONY: lint test test-unit test-integration check coverage
lint test test-unit test-integration check coverage:
	docker-compose run --rm app make  -f Makefile.targets $(MAKECMDGOALS) $(MAKEFLAGS)

