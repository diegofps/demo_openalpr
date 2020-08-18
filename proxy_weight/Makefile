all: build

build:
	docker build . -t openalpr-proxy-weight:v1
	docker tag openalpr-proxy-weight:v1 10.1.1.1:27443/openalpr-proxy-weight:v1
	docker push 10.1.1.1:27443/openalpr-proxy-weight:v1
w: build
	(cd /home/ngd/Sources/demo_openalpr/tools && ./expose_w.sh)

m: build
	(cd /home/ngd/Sources/demo_openalpr/tools && ./expose_m.sh)
