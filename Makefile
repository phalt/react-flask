help:
	@echo
	@grep -E '^[ .a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo

serve:  ## Run the server
	python server.py run

lint:  ## Run linting on the project
	isort src/
	black src/

mypy:  ## Check typing
	mypy src/

.PHONY: serve
