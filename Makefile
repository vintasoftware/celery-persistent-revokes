.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## check style with prospector
	pipenv run prospector

test: ## run tests quickly with the default Python
	pipenv run python runtests.py tests

test-all: ## run tests on every Python version with tox
	pipenv run tox

coverage: ## check code coverage quickly with the default Python
	pipenv run coverage run --source celery_persistent_revokes runtests.py tests
	pipenv run coverage report -m
	pipenv run coverage html
	open htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/celery-persistent-revokes.rst
	rm -f docs/modules.rst
	pipenv run sphinx-apidoc -o docs/ celery_persistent_revokes
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

release: clean ## package and upload a release
	pipenv run python setup.py sdist upload
	pipenv run python setup.py bdist_wheel upload

sdist: clean ## package
	pipenv run python setup.py sdist
	ls -l dist