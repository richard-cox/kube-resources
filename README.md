# Purpose

Load an individual Kubernetes cluster with enough resources to reproduce performance issues with the Rancher UI.

# Usage

```
kubectl apply -f make-700-deployments.yaml -n test-performance
```

It should work on any cluster. I recommend a cluster with three etcd/controlplane nodes.

I also recommend creating them in a non-default namespace for easier cleanup, as the default namespace cannot be deleted.

# Customization

To customize the resources, you would edit `make-700-deployments.py` and then run:

```
python3 make-700-deployments.py
```
That regenerates the YAML file. Then create the Deployments again:

```
kubectl apply -f make-700-deployments.yaml -n test-performance
```

# Notes

After loading ~700 Deployments, I started to see some lagging, with about 4 seconds to load a new page of Deployments.

I tried loading 1000 Secrets and it didn't affect performance at all. 