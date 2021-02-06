MODULE := main
BLUE='\033[0;34m'
NC='\033[0m' # No Color

run:
	@python -m $(MODULE)

test:
	@pytest

lint:
	@echo "\n${BLUE}Running Pylint against source files...${NC}\n"
	@pylint --rcfile=setup.cfg main
	@echo "\n${BLUE}Running Pylint against test files...${NC}\n"
	@pylint --rcfile=setup.cfg test

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

.PHONY: clean test