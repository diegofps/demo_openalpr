# Build the container (for multiple architectures)

```bash
# For multiple architectures (recommended)
docker buildx build --platform linux/amd64,linux/arm64 --push=true -t $HOST_IP:27443/demo_openalpr:v1 .

# For just the current architecture
docker build -t demo_openalpr:v1 .
```
