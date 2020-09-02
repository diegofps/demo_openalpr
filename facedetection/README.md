# Build the container

```bash
# For multiple architectures (recommended)
docker buildx build --platform linux/amd64,linux/arm64 --push=true -t $HOST_IP:27443/demo_facedetection:v1 .

# For just the current architecture
docker build -t demo_facedetection:v1 .
```
