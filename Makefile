SHELL=/bin/sh

.SHELLFLAGS = -e -c
.ONESHELL:
.PHONY: help

##@ General
help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-50s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Local Development
.PHONY: run
run: makemigrations migrate ## run the app locally with migration process
	python3 manage.py runserver

##@ Continous Deployment
.PHONY: makemigrations
makemigrations: ## generate django migration script
	python3 manage.py makemigrations

.PHONY: migrate 
migrate: ## django migrate 
	python3 manage.py migrate

.PHONY: initiate
initiate: ## initiate small database example
	python3 initiate.py