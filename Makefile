# inspired from: https://towardsdatascience.com/ultimate-setup-for-your-next-python-project-179bda8a7c2c

MODULE := src
BLUE='\033[0;34m'
NC='\033[0m' # No Color

run:
	python src/__main__.py

test:
	nosetests

format:
	black src; \
	black test; \

lint:
	pylint --rcfile=setup.cfg src; \
	pylint --rcfile=setup.cfg test; \
	flake8; \

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

.PHONY: clean test
