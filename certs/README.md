# Generate cert Secrets that will expire soon

1. Follow https://kubernetes.io/docs/tasks/administer-cluster/certificates/#easyrsa
   - For this purpose, any ip will do
     - Set env vars `MASTER_IP` & `MASTER_CLUSTER_IP`
    - Set `--days=10000` to something better 
2. In Rancher create the secret
   - Nav to `Secret: Create TLS Certificate`
   - Certificate is the cert at the bottom of `pki/issued/server.crt`   
   - Private key is `pki/private/server.key` 