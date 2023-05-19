help:
	@echo
	@grep -E '^[ .a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo

dev:  ## Run both the Flask service and the React app at once
	make -j4 serve web

serve:  ## Run the server
	python server.py run

web:  ## Watch the JS directory for changes while running the frontend server
	yarn watch

lint:  ## Run linting on the project
	ruff src/
	black src/
	yarn format

mypy:  ## Check typing
	mypy src/

.PHONY: serve
