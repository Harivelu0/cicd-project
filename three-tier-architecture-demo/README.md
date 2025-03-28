# Robot Shop E-Commerce Application Deployment on AKS

This repository documents my implementation of the Robot Shop e-commerce application on Azure Kubernetes Service (AKS) The original application was developed by IBM's Instana as a demo microservices application. This project demonstrates a microservices architecture with multiple components working together to provide a complete e-commerce experience.

## Application Overview

The Robot Shop is a sample microservices application originally created by Instana for demonstration purposes. It simulates an e-commerce website that sells robots, providing functionality for:

- User registration and authentication
- Product browsing and catalog service
- Shopping cart management
- Payment processing
- Order shipping and dispatch
- Product ratings

## Architecture

The application consists of multiple microservices, each serving a specific purpose:

- **Web**: Frontend interface built with Node.js
- **Cart**: Shopping cart service (Node.js)
- **Catalogue**: Product catalog and details (Node.js)
- **User**: User account management (Node.js)
- **Shipping**: Shipping cost calculator (Java)
- **Payment**: Payment processor (Python)
- **Ratings**: Product ratings service (PHP)
- **MongoDB**: Database for product catalog and user information
- **MySQL**: Database for payment and shipping information
- **Redis**: In-memory store for shopping cart and session data
- **RabbitMQ**: Message queue for dispatch service

## Pre-requisites

- Azure subscription
- Azure CLI installed
- kubectl installed
- Helm 3 installed
- Basic understanding of Kubernetes concepts

## Deployment Steps

### 1. Create AKS Cluster

```bash
# Create a resource group (if not already created)
az group create --name myResourceGroup --location eastus

# Create AKS cluster
az aks create --resource-group myResourceGroup --name robotShopCluster --node-count 2 --enable-addons monitoring --vm-size Standard_DS2_v2 --generate-ssh-keys

# Get credentials for the cluster
az aks get-credentials --resource-group myResourceGroup --name robotShopCluster

# Verify connection to cluster
kubectl config current-context
```

### 2. Storage Configuration

The default storage classes provided by Azure are sufficient for this deployment. You can check the available storage classes:

```bash
kubectl get storageclass
```

By default, Azure provides:
- `managed-premium` (SSD-based storage)
- `default` (Standard HDD-based storage)

These are used by the persistent volume claims for MongoDB, MySQL, and Redis.

### 3. Deploy Robot Shop Application

Create a namespace for the Robot Shop application:

```bash
kubectl create namespace robot-shop
```

Navigate to the Helm chart directory:

```bash
cd AKS/helm
```

Install the application using Helm:

```bash
helm install robot-shop . --namespace robot-shop
```

Verify all pods are running:

```bash
kubectl get pods -n robot-shop
```

### 4. Configure Ingress Controller

When using Azure CNI Overlay network mode, the Application Gateway Ingress Controller cannot be enabled from the Azure Portal UI. Therefore, we need to install NGINX Ingress Controller manually:

```bash
# Create namespace for the ingress controller
kubectl create namespace ingress-basic

# Add Helm repository for NGINX ingress
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX ingress controller
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-basic \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux
```

Check if the ingress controller is running:

```bash
kubectl get pods -n ingress-basic
```

Get the external IP address of the ingress controller:

```bash
kubectl get services -n ingress-basic
```

### 5. Configure Ingress Rules for Robot Shop

Create or update the ingress.yaml file in the helm directory:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: robot-shop
  namespace: robot-shop
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 8080
```

Note: The `ingressClassName` must match the ingress controller class name. In this case, we're using `nginx` instead of `azure-application-gateway`.

Apply the ingress rule:

```bash
kubectl apply -f ingress.yaml -n robot-shop
```

Verify the ingress resource:

```bash
kubectl get ing -n robot-shop
```

### 6. Access the Application

Once the ingress is successfully configured, you can access the Robot Shop application using the external IP address of the NGINX ingress controller.

```
http://<EXTERNAL-IP>
```

## Network Configuration Details

Understanding the networking model used by your AKS cluster is crucial:

### Azure CNI (Standard)
- Pods get IP addresses directly from the VNet
- Better for integration with other Azure services
- Higher IP address consumption
- Better performance for pod-to-pod communication
- Supports Kubernetes network policies

### Azure CNI Overlay (Used in this deployment)
- Uses overlay networking
- More efficient IP address usage than standard CNI
- Supports larger cluster sizes
- Has limitations with certain add-ons like Application Gateway Ingress Controller

## Troubleshooting

### Ingress Controller Issues

If your ingress is not working, check the ingress controller logs:

```bash
kubectl logs <ingress-controller-pod-name> -n ingress-basic
```

Common issues include:
- Incorrect `ingressClassName` - Make sure it matches the installed ingress controller
- Service name mismatch - Ensure the backend service exists and is correctly named
- Port mismatch - Verify the service port is correct

### Cross-Namespace Communication

The ingress controller in the `ingress-basic` namespace can route traffic to services in the `robot-shop` namespace without any special configuration, as long as the Ingress resource in `robot-shop` specifies the correct `ingressClassName: nginx`.

## References

- [Abhishek Veeramalla's Tutorial](https://www.youtube.com/watch?v=akNSPKX0uIA&list=PLdpzxOOAlwvIcxgCUyBHVOcWs0Krjx9xR&index=20) - Original tutorial followed for this implementation
- [Robot Shop Original Repository](https://github.com/instana/robot-shop) - IBM's Instana demo application
- [Azure Kubernetes Service Documentation](https://docs.microsoft.com/en-us/azure/aks/)
- [NGINX Ingress Controller Documentation](https://kubernetes.github.io/ingress-nginx/)
- [Kubernetes Ingress Documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)



![Screenshot 2025-03-28 143118](https://github.com/user-attachments/assets/7e19ddfa-42d8-49e2-baee-02e85802d2a7)

![Screenshot 2025-03-28 143135](https://github.com/user-attachments/assets/f7af004e-82c1-407e-901b-8b44c7783bd3)

![Screenshot 2025-03-28 143247](https://github.com/user-attachments/assets/ac6d0827-f995-4605-96b1-c41b4280406a)


![Screenshot 2025-03-28 143257](https://github.com/user-attachments/assets/de53f9d4-fdd0-4873-ab42-d687af0ab55f)


![Screenshot 2025-03-28 143620](https://github.com/user-attachments/assets/7911523b-0711-4d72-8547-0ff205aee29e)




