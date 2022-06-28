import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'make-4000-deployments.yaml')
file = open(filename, 'a', encoding="utf-8")

def getDeployment(number):

  return f"""
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: busybox-deployment{number}
  labels:
    app: busybox
spec:
  replicas: 10
  strategy: 
    type: RollingUpdate
  selector:
    matchLabels:
      app: busybox
  template:
    metadata:
      labels:
        app: busybox
    spec:
      nodeSelector:
        node: nonexistent
      containers:
      - name: busybox
        image: busybox
        imagePullPolicy: IfNotPresent
        
        command: ['sh', '-c', 'echo Container 1 is Running ; sleep 3600']
"""


i = 1
for x in range(4000):
    
    file.write(getDeployment(str(i)))
    i = i + 1
else:
    print("Finished!")

file.close()
