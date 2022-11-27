PYTHON_FILES = mopidy_pummeluff
STATIC_FILES = mopidy_pummeluff/webui
BUILD_DIR = build
LINTER_CONFIGS = https://git.confirm.ch/confirm/development-guidelines/raw/master/configs

.PHONY: build

#
# Cleanup
#

clean: clean-test clean-build clean-node clean-venv

clean-test:
	rm -vrf .isort.cfg .pylintrc tox.ini .eslintrc.yml .stylelintrc.yml

clean-build:
	rm -vrf $(BUILD_DIR)

clean-node:
	rm -vrf node_modules package-lock.json

clean-venv:
	rm -vrf .venv

#
# Install
#

venv:
	python3 -m venv .venv

develop-python:
	pip3 install -r requirements.txt -r requirements-dev.txt

develop-node:
	npm install

develop: develop-python develop-node

#
# Development
#

isort:
	curl -sSfo .isort.cfg $(LINTER_CONFIGS)/isort.cfg
	isort $(PYTHON_FILES)

#
# Test
#

test-isort:
	curl -sSfo .isort.cfg $(LINTER_CONFIGS)/isort.cfg
	isort -c --diff $(PYTHON_FILES)

test-pycodestyle:
	curl -sSfo tox.ini $(LINTER_CONFIGS)/tox.ini
	pycodestyle $(PYTHON_FILES)

test-pylint:
	curl -sSfo .pylintrc $(LINTER_CONFIGS)/pylintrc
	pylint $(PYTHON_FILES)

test-eslint:
	curl -sSfo .eslintrc.yml $(LINTER_CONFIGS)/eslintrc.yml
	npx eslint $(STATIC_FILES)/*.js

test-stylelint:
	curl -sSfo .stylelintrc.yml $(LINTER_CONFIGS)/stylelintrc.yml
	npx stylelint $(STATIC_FILES)/*.css

test: test-isort test-pycodestyle test-pylint test-eslint test-stylelint

#
# Build
#

sdist:
	./setup.py sdist -d $(BUILD_DIR)

wheel:
	./setup.py bdist_wheel -d $(BUILD_DIR)

build: sdist wheel
