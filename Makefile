tests = $(wildcard test/*.py)

test:
	python3 -m unittest $(tests)

.PHONY: test
