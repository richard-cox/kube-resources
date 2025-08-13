# Deployments

A deployment that will generate 10 events every second
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: event-generator
  namespace: spam
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: event-creator
  namespace: spam
rules:
  - apiGroups: [""] # The core API group
    resources: ["events"]
    verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: event-creator-binding
  namespace: spam
subjects:
  - kind: ServiceAccount
    name: event-generator
    namespace: spam
roleRef:
  kind: Role
  name: event-creator
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-generator
  namespace: spam
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
          image: curlimages/curl:latest
          command: ["/bin/sh", "-c"]
          args:
            - |
              while true; do
                # Construct the JSON payload and pipe it directly to curl
                echo '{"apiVersion":"v1","kind":"Event","metadata":{"name":"event-burst-'$(date +%s%N)'-'$RANDOM'","namespace":"spam"},"involvedObject":{"kind":"Deployment","name":"event-generator","namespace":"spam"},"reason":"StressTest","message":"Generating 10 events per second via API.","type":"Normal","source":{"component":"event-generator-pod"}}' | \
                curl -s -k -X POST \
                  --header "Content-Type: application/json" \
                  --header "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
                  --data @- \
                  "https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT}/api/v1/namespaces/spam/events"
                sleep 1;
              done;
```
