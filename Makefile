run:
	python src/__main__.py

dev:
	python src/__main__.py --local

test:
	nosetests -v

format:
	black src; \
	black test; \

check-format:
	black --check src
	black --check test

lint:
	pylint --rcfile=setup.cfg src; \
	pylint --rcfile=setup.cfg test --disable="W0613";

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

coverage:
	coverage run -m nose
	coverage report

coverage-html:
	coverage run -m nose
	coverage html -d reports/

.PHONY: clean test
