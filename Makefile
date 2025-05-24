# Makefile for Airbnb Automation Task

# Variables
IMAGE_NAME=airbnb-test
CONTAINER_NAME=airbnb-test-container

.PHONY: install build run test clean

install:
	pip install -r requirements.txt
	python -m playwright install

build:
	docker build -t $(IMAGE_NAME) -f docker/Dockerfile .

run:
	docker run --rm --name $(CONTAINER_NAME) $(IMAGE_NAME)

test:
	docker run --rm --name $(CONTAINER_NAME) $(IMAGE_NAME) pytest tests/ -s

clean:
	-docker rmi $(IMAGE_NAME)
	-rm -rf __pycache__ .pytest_cache temp/*.json
