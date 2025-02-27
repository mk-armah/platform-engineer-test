Below is a sample README.md that documents your project. You can adjust details as needed for your final submission.

---

# GitOps & FastAPI Project

This project demonstrates a complete GitOps workflow using Kubernetes, Helm, ArgoCD, and a FastAPI microservice. The objectives are to showcase hands-on skills with Kubernetes deployments (via K3D), GitOps with ArgoCD, FastAPI development, and CI/CD best practices.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Deployments](#deployments)
  - [ArgoCD Installation](#argocd-installation)
  - [Deploying Nginx via GitOps](#deploying-nginx-via-gitops)
  - [FastAPI Service (my-service)](#fastapi-service-my-service)
- [Docker & Helm](#docker--helm)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This project consists of two main components:

1. **Nginx Application:**  
   Deployed via Helm and managed by ArgoCD, serving as a simple web server accessible via `nginx.local`.

2. **FastAPI Microservice (my-service):**  
   A FastAPI-based microservice that:
   - Provides health-check and API endpoints.
   - Interacts with the ArgoCD API to list application statuses and projects.
   - Is containerized using Docker and deployed with Helm, managed by ArgoCD, and exposed via `my-service.local`.

The GitOps approach is implemented by storing all Kubernetes manifests, Helm charts, and configuration files in a GitHub repository. ArgoCD continuously syncs the desired state from Git with the live cluster.

## Prerequisites

Before you begin, ensure you have the following installed and configured on your system:

- **GitHub Account** (for hosting the repository)
- **K3D** (for setting up a local Kubernetes cluster)
- **Poetry** (for Python dependency management)
- **Kubectl** (for interacting with Kubernetes)
- **Docker** (for building container images)
- **Helm** (for managing Kubernetes applications)
- **ArgoCD** (for continuous deployment via GitOps)

## Project Structure

```plaintext
platfrom-engineer-test/
├── infra-k8s/
│   ├── k8s-apps/
│   │   ├── nginx/                  # Helm chart for Nginx
│   │   ├── my-service/             # Helm chart for FastAPI service
│   └── argo-apps/
│       ├── nginx-argo-app.yaml     # ArgoCD application manifest for Nginx
│       └── my-service-argo-app.yaml# ArgoCD application manifest for my-service
├── my-service/                     # FastAPI service code
│   ├── my_service/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── routers/
│   │   │           └── argocd_querier_router.py
│   │   ├── clients/
│   │   │   └── argocd_client.py
│   │   ├── config/
│   │   │   └── config.py
│   │   ├── models/
│   │   │   └── models.py
│   │   ├── utils/
│   │   │   └── logger.py
│   │   ├── main.py                # Application entry point
│   ├── tests/                     # Unit and integration tests
│   │   ├── test_routes.py
│   │   └── test_argocd_client.py
│   └── pyproject.toml             # Poetry & pytest configuration
└── README.md                      # Project documentation (this file)
```

## Environment Setup

### Local Kubernetes Cluster

1. Create your local Kubernetes cluster with K3D using the provided configuration file:
   ```bash
   k3d cluster create -c k3d-config.yaml --registry-config k3d-registries.yaml
   ```
2. Wait for all components to be ready:
   ```bash
   kubectl get pods --all-namespaces --watch
   ```

### Local Container Registry

1. Update your `/etc/hosts` file to include:
   ```plaintext
   127.0.0.1 my-registry.local
   ```
2. Verify your registry is running:
   ```bash
   docker ps | grep registry
   ```

## Deployments

### ArgoCD Installation

1. Install ArgoCD in the `argocd` namespace:
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```
2. Access the ArgoCD UI by port-forwarding the server:
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
3. Log in using default credentials (admin / initial password from the `argocd-server` pod).

### Deploying Nginx via GitOps

1. The Helm chart for Nginx is located in `infra-k8s/k8s-apps/nginx`.
2. The corresponding ArgoCD application manifest (`nginx-argo-app.yaml`) points to this chart in your Git repository.
3. ArgoCD will automatically deploy Nginx and expose it at `nginx.local` via Traefik.

### FastAPI Service (my-service)

1. The FastAPI service code is located in `my-service/my_service`.
2. The Helm chart for my-service is in `infra-k8s/k8s-apps/my-service` and configures:
   - The container to run on port 9000.
   - Health checks on `/healthcheck`.
   - An Ingress that routes traffic from `my-service.local` to the service.
3. The corresponding ArgoCD manifest (`my-service-argo-app.yaml`) ensures the service is deployed via GitOps.
4. The service interacts with ArgoCD’s API using the custom `ArgocdClient`.

## Docker & Helm

- **Docker:**  
  Build and push your FastAPI image to your local registry:
  ```bash
  docker build -t my-registry:5000/my-service:latest .
  docker push my-registry:5000/my-service:latest
  ```
- **Helm:**  
  Use Helm to template and deploy your applications. Example command for my-service:
  ```bash
  helm upgrade --install my-service-release infra-k8s/k8s-apps/my-service --namespace default
  ```
  ArgoCD will monitor the Git repository for changes and sync the cluster accordingly.

## Testing

### Running Tests Locally

Use Poetry to run your tests with coverage:
```bash
make test
```
This command runs:
```bash
poetry run pytest --cov=my_service tests/
```
The test suite includes:
- **Route tests:** Verifying the FastAPI endpoints.
- **ArgocdClient tests:** Using pytest-asyncio and aioresponses to simulate API calls.

### Test Coverage

Current test coverage is approximately 90% across the project. Test files are located under `my-service/tests`.

## Troubleshooting

- **Ingress Not Routing:**  
  Ensure your `/etc/hosts` file maps `nginx.local` and `my-service.local` to the IP addresses of your ingress controller (or use a load balancer IP).
- **Pod Issues:**  
  Check pod logs using:
  ```bash
  kubectl logs <pod-name> -n default
  ```
- **Image Pull Errors:**  
  Verify that your Docker image is correctly pushed to your registry and the image reference in your Helm chart uses the correct registry URL and port.
- **ArgoCD Sync Issues:**  
  Confirm that ArgoCD shows your applications as Synced and Healthy.
