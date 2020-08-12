# Before you begin

## Prepare your local keys directory

```bash
mkdir -p ./keys
sudo cp /var/lib/rancher/k3s/server/tls/client-admin.crt /var/lib/rancher/k3s/server/tls/client-admin.key /var/lib/rancher/k3s/server/tls/server-ca.crt ~/.ssh/id_rsa ./keys/
sudo chown $USER:$USER ./keys/*
```

# Running the proxy locally (Development)

## Deploy openalpr pods

```bash
sudo kubectl create deployment openalpr --image=$HOST_IP:27443/demo_openalpr
sudo kubectl scale deployments/openalpr --replicas 120
```

## Start the proxy server in a local machine
```bash
(cd src && flask run --port=4570 --host=0.0.0.0)
```

## Query an image

```bash
# In tower
time curl -F 'imagefile=@/home/diego/Sources/openalpr/image_0001.jpg' localhost:4570/forward/recognize

# In perl
time curl -F 'imagefile=@/home/ngd/Sources/openalpr/In-Situ-Data1.2_B/image_0001.jpg' localhost:4570/forward/recognize
```

# Running the proxy as a kubernetes service (ngd)

## Build and deploy the proxy in a local registry

```bash
docker build . -t openalpr-proxy-weight:v1
docker tag openalpr-proxy-weight:v1 $HOST_IP:27443/openalpr-proxy-weight:v1
docker push $HOST_IP:27443/openalpr-proxy-weight:v1
```

## Assign weights to your nodes

```bash
# For newports and raspberries
sudo kubectl label node --all weight=4 --overwrite

# For perl
sudo kubectl label node perl weight=104 --overwrite

# For tower
sudo kubectl label node perl weight=320 --overwrite
```

## Deploy the proxy in the cluster using the deploy script

```bash
sudo kubectl apply -f deployment_openalpr-proxy-weight.yaml
```

## Deploy Pods with openalpr app

```bash
# Manual deploy (hybrid)
sudo kubectl create deployment openalpr --image=$HOST_IP:27443/demo_openalpr
sudo kubectl scale deployments/openalpr --replicas 120

# Using one of the deploy scripts for extra configurations
sudo kubectl apply -f deployment_openalpr_csd.yaml
sudo kubectl apply -f deployment_openalpr_hybrid.yaml
sudo kubectl apply -f deployment_openalpr_perl.yaml
```

## Expose the proxy using a service

```bash
sudo kubectl expose deployment/openalpr-proxy-weight --type="LoadBalancer" --port 4570
```

## Query an image

```bash
time curl -F 'imagefile=@/home/diego/Sources/openalpr/image_0001.jpg' localhost:4570/forward/recognize
```
