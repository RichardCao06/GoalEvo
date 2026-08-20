.PHONY: install validate decisions pilot-check freeze-check test all

install:
	python -m pip install -e '.[dev]'

validate:
	python -m goalevo_protocol.cli validate

decisions:
	python -m goalevo_protocol.cli decisions

pilot-check:
	python -m goalevo_protocol.cli pilot-check

freeze-check:
	python -m goalevo_protocol.cli freeze-check

test:
	pytest -q

all: validate decisions pilot-check test
