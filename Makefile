IMAGE_NAME := my_webservice
IMAGE_VERSION := 0.0.1

IMAGE_NAMESPACE := rory
IMAGE_FULL_NAME := $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_VERSION)
CONTAINER := my_webservice

.PHONY: build
build:
	docker build -t $(IMAGE_FULL_NAME) .

.PHONY: rm
rm:
	docker rm -f $(CONTAINER)

.PHONY: run
run:
	docker run \
		-p 5000:5000 \
		-d --name $(CONTAINER) \
		--env-file ${env} \
		$(IMAGE_FULL_NAME)