NAME = $(shell basename $(CURDIR))
PYNAME = $(subst -,_,$(NAME))

check:
	ruff check */*.py */*/*.py
	flake8 */*.py */*/*.py
	mypy */*.py */*/*.py
	vermin -vv --exclude importlib.metadata --no-tips -i */*.py */*/*.py

build:
	rm -rf dist
	python3 -m build

upload: build
	twine3 upload dist/*

doc:
	update-readme-usage -a

clean:
	@rm -vrf *.egg-info .venv/ build/ dist/ __pycache__/
