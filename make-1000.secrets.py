import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'make-1000-secrets.yaml')
file = open(filename, 'a', encoding="utf-8")

def getSecret(name):

  return f"""
---
apiVersion: v1
kind: Secret
metadata:
  name: {name}
type: Opaque
data:
  username: bWVnYV9zZWNyZXRfa2V5Cg==
  password: cmVhbGx5X3NlY3JldF92YWx1ZTEK
"""


i = 1
for x in range(1000):
    
    file.write(getSecret('secret' + str(i)))
    i = i + 1
else:
    print("Finished!")

file.close()
print(file.closed)
