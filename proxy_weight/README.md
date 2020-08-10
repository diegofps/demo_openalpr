# Before you begin

## Prepare your local keys directory

```bash
mkdir -p ./keys
sudo cp /var/lib/rancher/k3s/server/tls/client-admin.crt /var/lib/rancher/k3s/server/tls/client-admin.key /var/lib/rancher/k3s/server/tls/server-ca.crt ~/.ssh/id_rsa ./keys/
sudo chown $USER:$USER ../keys/*
```

# Running the proxy locally

## Deploy openalpr pods

```bash
sudo kubectl create deployment openalpr --image=$HOST_IP:27443/demo_openalpr
sudo kubectl scale deployments/openalpr --replicas 120
```

## Start the local proxy server
```bash
(cd src && flask run --port=4570 --host=0.0.0.0)
```

## Query an image

```bash
time curl -F 'imagefile=@/home/diego/Sources/openalpr/image_0001.jpg' localhost:4570/forward/recognize
```

# Running the proxy as a kubernetes service

## Deploy the proxy in a local registry

```bash
docker build . -t openalpr-proxy-weight:v1
docker tag openalpr-proxy-weight:v1 192.168.1.134:27443/openalpr-proxy-weight:v1
docker push 192.168.1.134:27443/openalpr-proxy-weight:v1
```

## Deploy the proxy in the cluster using the deploy script

```bash
sudo kubectl apply -f deployment_openalpr-proxy.yaml
```

## Deploy openalpr pods

```bash
sudo kubectl create deployment openalpr --image=$HOST_IP:27443/demo_openalpr
sudo kubectl scale deployments/openalpr --replicas 120
```

## Expose the proxy using a service

```bash
sudo kubectl expose deployment/openalpr-proxy-weight --type="LoadBalancer" --port 4570
```


# Query an image

```bash
time curl -F 'imagefile=@/home/diego/Sources/openalpr/image_0001.jpg' localhost:4570/forward/recognize
```
