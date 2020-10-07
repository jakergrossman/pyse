tests = $(wildcard test/*.py) $(wildcard test/*/*.py)

test:
	python3 -m unittest -v $(tests)

.PHONY: test
