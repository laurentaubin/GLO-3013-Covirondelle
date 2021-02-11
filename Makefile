MODULE := src
BLUE='\033[0;34m'
NC='\033[0m' # No Color

run:
	@python -m $(MODULE)

test:
	@pytest

format:
	@echo "\n${BLUE}Running formatter against source files...${NC}\n"
	@black src
	@echo "\n${BLUE}Running formatter against test files...${NC}\n"
	@black test

lint:
	@echo "\n${BLUE}Running Pylint against source files...${NC}\n"
	@pylint --rcfile=setup.cfg src
	@echo "\n${BLUE}Running Pylint against test files...${NC}\n"
	@pylint --rcfile=setup.cfg test
	@echo "\n${BLUE}Running Flake8 against source and test files...${NC}\n"
	@flake8

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

.PHONY: clean test
