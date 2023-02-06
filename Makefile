.PHONY: black
black:
	black ./picar --line-length=120

.PHONY: flake8
flake8:
	flake8 ./picar --count --show-source --statistics

.PHONY: format
format:
	make black
	make flake8
