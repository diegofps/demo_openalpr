all: certs awob

keys:
	mkdir -p ./keys
	sudo cp /var/lib/rancher/k3s/server/tls/client-admin.crt /var/lib/rancher/k3s/server/tls/client-admin.key /var/lib/rancher/k3s/server/tls/server-ca.crt ~/.ssh/id_rsa ./keys/
	sudo chown ${USER}:${USER} ./keys/*

build:
	docker build . -t demo-proxy:v1
	docker tag demo-proxy:v1 10.1.1.1:27443/demo-proxy:v1
	docker push 10.1.1.1:27443/demo-proxy:v1
w: build
	(cd /home/ngd/Sources/demo_openalpr/tools && ./expose_w.sh)

m: build
	(cd /home/ngd/Sources/demo_openalpr/tools && ./expose_m.sh)

aw: build
	(cd /home/ngd/Sources/demo_openalpr/tools && ./expose_aw.sh)

wob: build
	(cd /home/ngd/Sources/demo_openalpr/tools && ./expose_wob.sh)

awob: build
	(cd /home/ngd/Sources/demo_openalpr/tools && ./expose_awob.sh)

