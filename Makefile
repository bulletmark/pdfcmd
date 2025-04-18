NAME = $(shell basename $(CURDIR))
PYNAME = $(subst -,_,$(NAME))

check:
	ruff check $(NAME)/*.py $(NAME)/commands/*.py
	mypy $(NAME)/*.py $(NAME)/commands/*.py
	pyright $(NAME)/*.py $(NAME)/commands/*.py
	vermin -vv --exclude importlib.metadata --no-tips -i $(NAME)/*.py $(NAME)/commands/*.py

build:
	rm -rf dist
	uv build

upload: build
	uv-publish

doc:
	update-readme-usage

clean:
	@rm -vrf *.egg-info .venv/ build/ dist/ __pycache__/
