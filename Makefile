help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "build - package"

all: default

default: clean deps test build

build: clean
	python setup.py bdist_wheel --universal

clean: clean-build clean-pyc clean-test

clean-build:
	rm -rf build/
	rm -rf dist/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test:
	rm -f .coverage
	rm -rf htmlcov/

deps:
	pip install -U -r ../requirements.txt

test:
	py.test -vv --cov=thaitokenizer --cov-report term


