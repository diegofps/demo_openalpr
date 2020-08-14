# Build the container

```bash
docker build . -t demo_openalpr:v1
docker tag demo_openalpr:v1 $HOST_IP:27443/demo_openalpr:v1
docker push $HOST_IP:27443/demo_openalpr:v1
```
