.PHONY: black
black:
	black ./picarx --line-length=120

.PHONY: flake8
flake8:
	flake8 ./picarx --count --show-source --statistics

.PHONY: format
format:
	make black
	make flake8
