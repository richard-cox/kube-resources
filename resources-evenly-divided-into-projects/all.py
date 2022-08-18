import os
from string import Template
dirname = os.path.dirname(__file__)

downstream_filename = os.path.join(
    dirname, 'downstream-cluster-resources.yaml')
downstream_file = open(downstream_filename, 'a', encoding="utf-8")

local_cluster_filename = os.path.join(dirname, 'local-cluster-resources.yaml')
local_cluster_file = open(local_cluster_filename, 'a', encoding="utf-8")


local_resource_yaml = """

---
apiVersion: management.cattle.io/v3
description: ""
enabled: true
kind: User
metadata:
  annotations:
    field.cattle.io/creatorId: $userId
    lifecycle.cattle.io/create.mgmt-auth-users-controller: "true"
  finalizers:
  - controller.cattle.io/mgmt-auth-users-controller
  generateName: u-
  generation: 3
  labels:
    cattle.io/creator: norman
  name: $name
password: $2a$10$ozlxua6KD1W2WJxIOMvOX.uBFsubVqiPkivgmwOWz6PhzIoZ3aQKe
spec: {}
username: $name
---

apiVersion: management.cattle.io/v3
kind: Project
metadata:
  annotations:
    authz.management.cattle.io/creator-role-bindings: '{"created":["project-owner"],"required":["project-owner"]}'
    field.cattle.io/creatorId: $name
    lifecycle.cattle.io/create.mgmt-project-rbac-remove: "true"
    lifecycle.cattle.io/create.project-namespace-auth_c-m-9hg7h7h5: "true"
  generateName: p-
  generation: 3
  labels:
    cattle.io/creator: norman
  name: $name
  namespace: $clusterId
spec:
  clusterName: $clusterId
  description: ""
  displayName: $name
  enableProjectMonitoring: false
---

administrative: false
apiVersion: management.cattle.io/v3
builtin: false
clusterCreatorDefault: false
context: project
displayName: $name
external: false
hidden: false
kind: RoleTemplate
locked: false
metadata:
  annotations:
    cleanup.cattle.io/rtUpgradeCluster: "true"
    field.cattle.io/creatorId: $userId
    lifecycle.cattle.io/create.mgmt-auth-roletemplate-lifecycle: "true"
  finalizers:
  - controller.cattle.io/mgmt-auth-roletemplate-lifecycle
  generateName: rt-
  generation: 3
  labels:
    cattle.io/creator: norman
  name: $name
projectCreatorDefault: false
roleTemplateNames:
- project-member
rules: []

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    authz.cluster.cattle.io/rtb-owner-updated: p-lsznf_prtb-pz7zw
    cattle.io/creator: norman
    manager: rancher
    operation: Update
  name: rb-$name
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: $name
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: $name
  
"""


downstream_resource_yaml = """
---
apiVersion: v1
kind: Namespace
metadata:
  name: $name-a
  annotations:
    field.cattle.io/projectId: $clusterId:$name
  labels:
    field.cattle.io/projectId: $name
---
apiVersion: v1
kind: Namespace
metadata:
  name: $name-b
  annotations:
    field.cattle.io/projectId: $clusterId:$name
  labels:
    field.cattle.io/projectId: $name
---
apiVersion: v1
kind: Secret
metadata:
  name: $name-a
  namespace: $name-a
type: Opaque
data:
  username: bWVnYV9zZWNyZXRfa2V5Cg==
  password: cmVhbGx5X3NlY3JldF92YWx1ZTEK
---
apiVersion: v1
kind: Secret
metadata:
  name: $name-b
  namespace: $name-b
type: Opaque
data:
  username: bWVnYV9zZWNyZXRfa2V5Cg==
  password: cmVhbGx5X3NlY3JldF92YWx1ZTEK
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: crashing-test-pod-$name
  namespace: $name-a
spec:
  selector:
    matchLabels:
      app: crashing-test-pod-$name
  replicas: 1
  template:
    metadata:
      labels:
        app: crashing-test-pod-$name
    spec:     
      containers:
        - command:
            - bash
            - -c
            - "echo test; sleep 10; exit 1;"
          image: ubuntu
          name: crashing-test-container

---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/name: load-balancer-example
  name: hello-world
  namespace: $name-b
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: load-balancer-example
  template:
    metadata:
      labels:
        app.kubernetes.io/name: load-balancer-example
    spec:
      containers:
      - image: gcr.io/google-samples/node-hello:1.0
        name: hello-world
        ports:
        - containerPort: 8080
"""


for x in range(1):
    downstream_clusterId = "c-m-gnvvtdhl"
    creator_userId = "user-th54t"

    local_template = Template(local_resource_yaml)
    local_substituted = local_template.safe_substitute({
        "name": 'test' + str(x),
        "userId": creator_userId,
        "clusterId": downstream_clusterId
    })
    local_cluster_file.write(local_substituted)

    downstream_template = Template(downstream_resource_yaml)
    downstream_substituted = downstream_template.safe_substitute({
        "name": 'test' + str(x),
        "clusterId": downstream_clusterId
    })
    downstream_file.write(downstream_substituted)

else:
    print("Finished!")

downstream_file.close()
local_cluster_file.close()
