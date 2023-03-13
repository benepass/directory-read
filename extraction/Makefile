.ONESHELL:

help:
	@echo  'Main targets:'
	@echo  ''
	@echo  '  make clean                   - Clean cached python files and build folder.'
	@echo  '  make format                  - Format code against linting & formatting tools.'
	@echo  '  make watch                   - Launch pyright watcher.'
	@echo  '  make check                   - Check for any formatting or linting issues.'
	@echo  '  make test                    - Run project tests.'
	@echo  '  make test-cov                - Run project tests and generate a coverage report.'
	@echo  '  make local-deploy env=<ENV>  - Build and deploy application to specified stage. (Local)'
	@echo  '  make deploy env=<ENV>        - Build and deploy application to specified stage.'
	@echo  '  make local-update env=<ENV>  - Deploy (w/o building) application to specified stage. (Local)'
	@echo  '  make update env=<ENV>        - Deploy (w/o building) application to specified stage.'
	@echo  '  make local-destroy           - Destroy application from the specified stage. (Local)'
	@echo  '  make destroy                 - Destroy application from the specified stage.'
	@echo  ''
	@echo  'Auxiliary targets (generally dependencies):'
	@echo  ''
	@echo  '  make clean-python            - Clean cached python files from directory tree.'
	@echo  '  make check-isort-format      - Check if code is correctly formatted by isort.'
	@echo  '  make check-black-format      - Check if code is correctly formatted by black.'
	@echo  '  make check-security-issues   - Check if code has any security issues.'
	@echo  '  make check-terraform-format  - Check if terraform files are correctly formatted.'
	@echo  '  make pyright                 - Check if code is correctly linted by pyright.'
	@echo  '  make flake8                  - Check and autofix flake8 indicated issues.'
	@echo  ''

clean-python:
	find . | grep -E "(__pycache__|\.pyc|\.pyo|\.pytest_cache|terraform/builds)" | xargs rm -rf

clean: clean-python

format:
	isort . &  flake8 . & black . & terraform fmt -recursive

check-isort-format:
	isort . --check --profile black

check-black-format:
	black . --check

check-security-issues:
	bandit . -r -q -c pyproject.toml

check-terraform-format:
	terraform fmt -recursive -check

watch:
	pyright -w .

pyright:
	pyright .

flake8:
	flake8 .

check: check-isort-format check-black-format flake8

test:
	pytest -s -vv

test-cov:
	pytest -s -vv --cov .

build-chalice-terraform:
	chalice package --stage $(env) --pkg-format terraform terraform/

deploy: build-chalice-terraform init-terraform update-terraform

local-deploy: build-chalice-terraform init-local-terraform update-local-terraform

init-terraform:
	cd terraform && terraform init && terraform workspace select $(env) || terraform workspace new $(env)

init-local-terraform:
	cd terraform && tflocal init && tflocal workspace select $(env) || tflocal workspace new $(env)

update-terraform:
	cd terraform && terraform validate && terraform apply -auto-approve

update-local-terraform:
	cd terraform && tflocal validate && tflocal apply -auto-approve

destroy:
	cd terraform && terraform destroy -auto-approve

destroy-local:
	cd terraform && tflocal delete --stage $(env) -auto-approve
