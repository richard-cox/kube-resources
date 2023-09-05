# Deprecated

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
 # name must match the spec fields below, and be in the form: <plural>.<group>
 name: myplatforms.mycrd.com
spec:
 # group name to use for REST API: /apis/<group>/<version>
 group: mycrd.com
 names:
   # plural name to be used in the URL: /apis/<group>/<version>/<plural>
   plural: myplatforms
   # singular name to be used as an alias on the CLI and for display
   singular: myplatform
   # kind is normally the CamelCased singular type. Your resource manifests use this.
   kind: MyPlatform
   # shortNames allow shorter string to match your resource on the CLI
   shortNames:
   - myp
 # either Namespaced or Cluster
 scope: Namespaced
 versions:
   - name: v1alpha1
     # Each version can be enabled/disabled by Served flag.
     served: true
     # One and only one version must be marked as the storage version.
     storage: true
     deprecated: true
     # This overrides the default warning returned to API clients making v1alpha1 API requests.
     deprecationWarning: "im deprecated!"
     schema:
       openAPIV3Schema:
         type: object
         properties:
           spec:
             type: object
             properties:
               appId:
                 type: string
               language:
                 type: string
                 enum:
                 - csharp
                 - python
                 - go
               os:
                 type: string
                 enum:
                 - windows
                 - linux
               instanceSize:
                 type: string
                 enum:
                   - small
                   - medium
                   - large
               environmentType:
                 type: string
                 enum:
                 - dev
                 - test
                 - prod
               replicas:
                 type: integer
                 minimum: 1
             required: ["appId", "language", "environmentType"]
         required: ["spec"]
```

Search for `myplatform` resource type

Create as YAML

```
apiVersion: mycrd.com/v1alpha1
kind: MyPlatform
metadata:
  name: aaaaa
  namespace: default
#  annotations:  key: string
#  labels:  key: string
spec:
  appId: "string"
  environmentType: "dev"
  instanceSize: "small"
  language: "csharp"
  os: "linux"
  replicas: 1
```

# Additional Columns

https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#additional-printer-columns

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.stable.example.com
spec:
  group: stable.example.com
  scope: Namespaced
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
    shortNames:
    - ct
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              cronSpec:
                type: string
              image:
                type: string
              replicas:
                type: integer
    additionalPrinterColumns:
    - name: Spec
      type: string
      description: The cron spec defining the interval a CronJob is run
      jsonPath: .spec.cronSpec
    - name: Replicas
      type: integer
      description: The number of jobs launched by the CronJob
      jsonPath: .spec.replicas
    - name: Age
      type: date
      jsonPath: .metadata.creationTimestamp
```
