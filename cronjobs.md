# Cronjobs

Simple job every minute, outputs to std
```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: suspended-cronjob-example
spec:
  schedule: "*/1 * * * *"
  suspend: true
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: debug-container
            image: busybox
            command: ["sh", "-c", "echo 'Hello from the debug CronJob!'"]
          restartPolicy: OnFailure
```
