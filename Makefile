SHELL:=/bin/bash

include .env

.PHONY: clean
clean:
	make  -f Makefile.targets $(MAKECMDGOALS) $(MAKEFLAGS)

.PHONY: deps
deps:
	pip install -r ./test/requirements.txt && python setup.py install --prefix=../.local

.PHONY: run
run:
	cat ./test/test_data/bom.com  | python ./src/cli.py

.PHONY: lint test check coverage
lint test check coverage:
	docker-compose run --rm app make  -f Makefile.targets $(MAKECMDGOALS) $(MAKEFLAGS)
