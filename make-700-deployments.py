import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'make-700-deployments.yaml')
file = open(filename, 'a', encoding="utf-8")

def getDeployment(number):

  return f"""
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crashing-test-pod{number}
spec:
  selector:
    matchLabels:
      app: crashing-test-pod{number}
  replicas: 10
  template:
    metadata:
      labels:
        app: crashing-test-pod{number}
    spec:     
      containers:
        - command:
            - bash
            - -c
            - "echo test; sleep 10; exit 1;"
          image: ubuntu
          name: crashing-test-container
"""


i = 1
for x in range(700):
    
    file.write(getDeployment(str(i)))
    i = i + 1
else:
    print("Finished!")

file.close()
