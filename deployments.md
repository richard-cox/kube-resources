# Deployments

A deployment that will generate 10 events every second
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-generator
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: event-generator
  template:
    metadata:
      labels:
        app: event-generator
    spec:
      serviceAccountName: event-generator
      containers:
        - name: event-generator-container
          image: bitnami/kubectl:latest
          command: ["/bin/sh", "-c"]
          args:
            - while true; do
                kubectl create event generic event-burst
                  --type=Normal
                  --reason=StressTest
                  --message="Generating 10 events per second."
                  --namespace=default;
                sleep 0.1;
              done;
```
