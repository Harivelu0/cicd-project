# Kubernetes CI/CD Pipeline with Azure DevOps and ArgoCD

This repository demonstrates a complete end-to-end CI/CD pipeline for a microservices-based voting application, leveraging Azure DevOps for continuous integration and ArgoCD for continuous deployment on Azure Kubernetes Service (AKS).

## Project Overview

This project implements a modern DevOps workflow with:

- **Source Control**: Git-based version control
- **CI Pipeline**: Automated builds with Azure DevOps
- **Container Registry**: Azure Container Registry (ACR)
- **Orchestration**: Kubernetes (AKS)
- **GitOps CD**: ArgoCD for declarative deployments
- **Microservices**: Multiple containerized components working together



## Application Architecture
![Untitled Diagram drawio](https://github.com/user-attachments/assets/d42a441b-4086-40b9-b221-09a62cc2b822)

The deployed application is a voting system with the following components:

- **Vote Frontend**: Web UI for casting votes (e.g., "Summer vs Winter")
- **Redis**: In-memory cache for temporary vote storage
- **Worker**: Background processor that handles vote aggregation
- **Database**: Persistent storage for vote data
- **Result App**: Web UI for displaying voting results

## Prerequisites

- Azure subscription
- Azure CLI
- kubectl
- Git
- Docker

## Setup Instructions

### 1. Azure Resources Setup

```bash
# Create resource group
az group create --name cicd --location eastus

# Create AKS cluster
az aks create --resource-group cicd --name azuredevops --node-count 1 --enable-addons monitoring --generate-ssh-keys

# Create Azure Container Registry
az acr create --resource-group cicd --name yourACRname --sku Basic

# Connect AKS to ACR
az aks update -n azuredevops -g cicd --attach-acr yourACRname
```

### 2. Connect to AKS Cluster

```bash
# Get credentials
az aks get-credentials --resource-group cicd --name azuredevops

# Verify connection
kubectl get nodes
```

### 3. ArgoCD Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Verify pods
kubectl get pods -n argocd
```

### 4. Configure ArgoCD for External Access

```bash
# Edit the argocd-server service to use NodePort
kubectl edit svc argocd-server -n argocd
# Change type: ClusterIP to type: NodePort

# Get service details
kubectl get svc -n argocd
```

### 5. Configure Azure DevOps Pipeline

1. Create a new pipeline in Azure DevOps
2. Connect to your Git repository
3. Configure the pipeline YAML with the following stages:
   - Build: Compiles application and creates Docker image
   - Push: Pushes image to Azure Container Registry
   - Update K8s Manifests: Updates image tags in Kubernetes manifests

### 6. Self-Hosted Agent Setup (Optional)

If you encounter parallelism limitations with Azure Pipelines:

```bash
# Create VM for agent
# Install agent software
# Configure as systemd service for background execution

# Example systemd service file
[Unit]
Description=Azure Pipelines Agent
After=network.target

[Service]
ExecStart=/path/to/agent/run.sh
User=yourusername
WorkingDirectory=/path/to/agent
Restart=always

[Install]
WantedBy=multi-user.target
```

### 7. ArgoCD Application Setup

```bash
# Create application in ArgoCD pointing to your Git repository
kubectl apply -f argocd-application.yaml
```

## Deployment Process

1. Developer pushes code changes to Git repository
2. Azure DevOps pipeline automatically triggers:
   - Builds Docker image for changed components
   - Tags and pushes image to ACR
   - Updates Kubernetes manifests with new image tag
3. ArgoCD detects changes in Git repository
4. ArgoCD synchronizes the desired state from Git with the Kubernetes cluster
5. New version of application is deployed to AKS

## Accessing the Application

Access the voting application UI:
```
http://<node-ip>:31000/
```

Access the results:
```
http://<node-ip>:31001/
```

## Automation Scripts

### Container Image Update Script

```bash
#!/bin/bash
# Script to update container image in Kubernetes manifests

# Update the image using yq
yq eval ".spec.template.spec.containers[0].image = \"$4.azurecr.io/$2:$3\"" -i k8s-specifications/$1-deployment.yaml

# Parameters:
# $1: Component name (vote, result, etc.)
# $2: Image name
# $3: Image tag
# $4: ACR name
```

## Troubleshooting

### Common Issues

1. **ArgoCD Sync Failure**
   - Check Git repository accessibility
   - Validate Kubernetes manifests

2. **Pipeline Failures**
   - Verify Azure DevOps agent status
   - Check ACR credentials and permissions

3. **Application Access Issues**
   - Confirm NodePort services are properly configured
   - Verify network security group settings

![Screenshot 2025-03-26 211930](https://github.com/user-attachments/assets/cff5b600-c375-4145-b4bc-38eb8f74def7)


![Screenshot 2025-03-27 010630](https://github.com/user-attachments/assets/f9770b96-8c67-4b51-a041-ac8d255971f1)

![Screenshot 2025-03-27 010603](https://github.com/user-attachments/assets/bd09298a-93b8-4cb7-bf79-34838306fbe4)

![Screenshot 2025-03-27 010402](https://github.com/user-attachments/assets/4820b1b0-fb69-4ed5-9bf7-52169713437e)

![Screenshot 2025-03-27 010326](https://github.com/user-attachments/assets/140cda42-92d2-4d3c-8cbf-b720c47c4d72)
