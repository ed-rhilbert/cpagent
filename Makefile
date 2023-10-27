.PHONY: help \
		venv venv-clean venv-create venv-update venv-editable venv-help-activate\
		coverage dist docs install \
		lint  \
		lint-pylint     \
		checks   \
		docs clean-docs  \
		clean clean-build clean-pyc clean-test \
		test \
		build install \
		test-import

# recipes are executed in a single shell
# allows working in activated venvs and no need to escape command lines
.ONESHELL:

.DEFAULT_GOAL := help

VENV_NAME := venv

CURRENT_VENV = $(if $(VIRTUAL_ENV),$(shell basename $(value VIRTUAL_ENV))," ")

ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
endif

ifeq ($(DETECTED_OS),Unknown)
	echo "Unknown OS" && exit 1
endif

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from platform import uname
import distro

from urllib.request import pathname2url

if 'microsoft-standard' in uname().release:
	webbrowser.open('\\\\wsl$$'+'\\'+distro.name()+os.path.abspath(sys.argv[1]).replace('/','\\'))
else:
	webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST) || python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


#############################################################
# Virtual Environment
#############################################################

venv: venv-clean venv-create venv-update venv-editable venv-help-activate ## create virtual environment and install required dependencies

venv-clean: ##remove the virtual environment
	rm -rf $(VENV_NAME)

venv-create: venv-clean ## create an empty virtual environment
	python -m venv $(VENV_NAME) || python3 -m venv $(VENV_NAME)

venv-update: ## install required dependencies from requirements.txt into the virtual environment (note that this does keep existing packages)
ifneq ($(CURRENT_VENV),$(VENV_NAME))
  ifeq ($(DETECTED_OS),Windows)
	./$(VENV_NAME)/Scripts/activate
  else
	. ./$(VENV_NAME)/bin/activate
  endif
endif
	python -m pip install -r requirements.txt --upgrade

venv-editable: ## install package in editable mode
ifneq ($(CURRENT_VENV),$(VENV_NAME))
  ifeq ($(DETECTED_OS),Windows)
	./$(VENV_NAME)/Scripts/activate
  else
	. ./$(VENV_NAME)/bin/activate
  endif
endif
	pip install -e .

venv-help-activate: ## provides the needed commands to manually activate the virtual environment (DOES NOT activate the virtual environment)
ifeq ($(CURRENT_VENV),$(VENV_NAME))
	echo "virtual environment is already activated : $(CURRENT_VENV)"
else
	echo "if you want to change the used virtual environment name, modify the variable VENV_NAME in the Makefile."
	echo "virtual environment must be created using 'make venv' then, manually activated!"
  ifeq ($(DETECTED_OS),Windows)
	echo "To activate virtual environment on windows, run : ./$(VENV_NAME)/Scripts/activate";
  else
	echo "To activate virtual environment on linux, run : . ./$(VENV_NAME)/bin/activate";
  endif
endif

venv-warn:
ifeq ($(CURRENT_VENV)," ")
	echo "Executing with no activated virtual environment!"
endif

venv-error:
ifeq ($(CURRENT_VENV)," ")
	echo "cannot launch with no activated virtual environment!"
	exit 1
endif


#############################################################
# Linting/checking
#############################################################

linters := lint-pylint   

lint: $(linters) ## launch linters

checkers := $(linters) 

checks: $(checkers) ## run all checkers and analyzers


lint-pylint: ## check style with pylint
	pylint --exit-zero src tests











#############################################################
# Docs
#############################################################

docs: venv-warn clean-docs ## generate Sphinx HTML documentation
	$(MAKE) -C docs/sphinx html
	$(BROWSER) docs/sphinx/build/html/index.html



#############################################################
# Test&Cover
#############################################################

test: venv-warn clean-test ## run tests
	python -m pytest

cover: venv-warn clean-test
	pytest --cov src --cov-report html --cov-report term
	$(BROWSER) htmlcov/index.html

test-import: ## tries to install package in a temporary environment and import it
	deactivate || true
	python -m venv temp_import_venv || python3 -m venv temp_import_venv
ifeq ($(DETECTED_OS),Windows)
	./temp_import_venv/Scripts/activate
else
	. ./temp_import_venv/bin/activate
endif
	pip install .
	python -c "import rlway_cpagent"
	deactivate
	rm -rf temp_import_venv

test-installed: ## tries to install package in a temporary environment and run the tests
	deactivate || true
	python -m venv temp_test_venv || python3 -m venv temp_test_venv
ifeq ($(DETECTED_OS),Windows)
	./temp_test_venv/Scripts/activate
else
	. ./temp_test_venv/bin/activate
endif
	pip install .
	pip install pytest
	python -m pytest
	deactivate
	rm -rf temp_test_venv


#############################################################
# Packaging
#############################################################

build: clean ## builds source and wheel package
	python -m build
	ls -l dist

install: venv-error ## install the package to the active Python's site-packages
	pip install .

editable: venv-error ## install the package to the active Python's site-packages (editable mode : reflects source modifications)
	pip install -e .


#############################################################
# Cleaning
#############################################################

clean-docs: ## remove docs artifacts
	$(MAKE) -C docs/sphinx clean


clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
