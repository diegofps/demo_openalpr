all: local

local:
	(cd src && flask run --port=4570 --host=0.0.0.0)

docker:
	docker build . -t openalpr-proxy-weight:v1
	docker tag openalpr-proxy-weight:v1 192.168.1.134:27443/openalpr-proxy-weight:v1
	docker push 192.168.1.134:27443/openalpr-proxy-weight:v1

keys:
	mkdir -p ./keys
	sudo cp /var/lib/rancher/k3s/server/tls/client-admin.crt /var/lib/rancher/k3s/server/tls/client-admin.key /var/lib/rancher/k3s/server/tls/server-ca.crt ~/.ssh/id_rsa ./keys/
	sudo chown $USER:$USER ../keys/*

