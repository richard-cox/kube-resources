import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'make-2000-namespaces.yaml')
file = open(filename, 'a', encoding="utf-8")

def getNamespace(name):

  return f"""
---
apiVersion: v1
kind: Namespace
metadata:
  name: {name}
"""


i = 1
for x in range(2000):
    
    file.write(getNamespace('namespace' + str(i)))
    i = i + 1
else:
    print("Finished!")

file.close()
print(file.closed)
