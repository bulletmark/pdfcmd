NAME = $(shell basename $(CURDIR))
PYNAME = $(subst -,_,$(NAME))

check:
	ruff check $(NAME)/*.py $(NAME)/commands/*.py
	mypy $(NAME)/*.py $(NAME)/commands/*.py
	pyright $(NAME)/*.py $(NAME)/commands/*.py
	vermin -vv --exclude importlib.metadata --no-tips -i $(NAME)/*.py $(NAME)/commands/*.py

build:
	rm -rf dist
	python3 -m build

upload: build
	twine3 upload dist/*

doc:
	update-readme-usage

clean:
	@rm -vrf *.egg-info .venv/ build/ dist/ __pycache__/
