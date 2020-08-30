all: build

build:
	docker buildx build --platform linux/amd64,linux/arm64 --push=true -t ${HOST_IP}:27443/demo_openalpr:v1 .
