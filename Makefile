.PHONY: dev docs build

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements/dev.txt

dev:
	python3 dev/manage.py runserver

docs:
	make -C docs html

lint:
	python3 -m pylint sslcommerz_sdk
	python3 -m black --exclude /migrations/* --check sslcommerz_sdk
	rstcheck --report warning *.rst docs/*.rst
	editorconfig-checker --exclude "__pycache__|_build" sslcommerz_sdk docs README.rst

test:
	python3 dev/manage.py test tests/ --keepdb

coverage:
	coverage run --source=sslcommerz_sdk dev/manage.py test tests/ --keepdb
	coverage report

build:
	python3 setup.py sdist bdist_wheel

deploy:
	twine upload --repository testpypi dist/*

deploy-prod:
	twine upload dist/*
