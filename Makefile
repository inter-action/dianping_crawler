#created by miaojing-243127395@qq.com on 2016-10-12 00:17:233

# see http://www.ruanyifeng.com/blog/2015/03/build-website-with-make.html
# for more info on Makefile
ENV_PATH = .env
PATH  := $(ENV_PATH)/bin:$(PATH)
SHELL := /bin/bash



# todo add more
.PHONY: virtualenv-test \

# activate virtualenv
virtualenv-test:
	which python
	which pip

virtualenv-create:
	virtualenv .env
	$(MAKE) test-virtualenv

# deactivate
deps-freeze: 
	pip freeze > requirements.txt

deps-install:
	pip install -r requirements.txt

run:
	python -m src.__main__