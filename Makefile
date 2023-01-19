.PHONY: black
black:
	black ./picar-x --line-length=120

.PHONY: flake8
flake8:
	flake8 picar-x --count --show-source --statistics

.PHONY: format
format:
	make black
	make flake8