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

coverage:
	coverage run -m nose
	coverage report

coverage-html:
	coverage run -m nose
	coverage html -d reports/

.PHONY: clean test
