# Purpose

Load an individual Kubernetes cluster with enough resources (4,000 Deployments) to reproduce performance issues with the Rancher UI.

# Usage

```
kubectl apply -f make-4000-deployments.yaml
```

# Customization

To customize the 4000 resources, you would edit `make-4000-deployments.py` and then run:

```
python3 make-4000-deployments.py
```
That regenerates the YAML file. Then create the Deployments again:

```
kubectl apply -f make-4000-deployments.yaml
```

# Notes

After loading ~700 Deployments, I started to see some lagging, with about 4 seconds to load a new page of Deployments.

The Deploymnents have the `node: nonexistent` node selector so that they never get scheduled. This is intentional because we don't need to actually schedule the Deployments. We just need to test how the UI deals with watching long lists of resources, so I think it is OK to create unschedulable Deployments for this purpose.

I tried loading 1000 Secrets and it didn't affect performance at all. 