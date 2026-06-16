PYTHON ?= python3

.PHONY: install install-dev lint format-check credential-scan test test-api test-e2e report-open quality

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(PYTHON) -m ruff check .

format-check:
	$(PYTHON) -m ruff format --check .

credential-scan:
	detect-secrets scan --baseline .secrets.baseline --all-files \
		--exclude-files '(^\.idea/|^\.pytest_cache/|^\.ruff_cache/|^\.venv/|^allure-results/|^allure-report/|\.png)'

test:
	$(PYTHON) -m pytest --alluredir=allure-results

test-api:
	$(PYTHON) -m pytest tests/system_tests -m api --alluredir=allure-results

test-e2e:
	$(PYTHON) -m pytest tests/e2e_tests -m e2e --alluredir=allure-results

report-open:
	allure serve allure-results

quality: lint format-check credential-scan test-api
