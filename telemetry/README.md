# Build the container

```bash
docker build . -t telemetry:v1
docker tag telemetry:v1 $HOST_IP:27443/telemetry:v1
docker push $HOST_IP:27443/telemetry:v1
```

# Deploy it on every primary machine

```bash
docker run -d --name telemetry -p 4580:4580 -e HOST_HOSTNAME=`hostname` -e REFRESH_SECONDS="5" telemetry:v1
```

