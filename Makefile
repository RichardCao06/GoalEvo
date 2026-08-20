.PHONY: install validate decisions freeze-check test all

install:
	python -m pip install -e '.[dev]'

validate:
	python -m goalevo_protocol.cli validate

decisions:
	python -m goalevo_protocol.cli decisions

freeze-check:
	python -m goalevo_protocol.cli freeze-check

test:
	pytest -q

all: validate test decisions
