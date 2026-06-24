# appy — Helm Chart for Flask Hello World

A custom Helm chart that deploys the [`j3ynn/flask-hello-world`](https://hub.docker.com/r/j3ynn/flask-hello-world) Docker image onto a Kubernetes cluster. The image tag is fully parameterizable at install/upgrade time, making it easy to release any tag produced by the `flask-app-example-build` Jenkins pipeline.

## Repository layout

```
charts/
└── appy/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── deployment.yaml
        ├── service.yaml
        └── ...
```

## Prerequisites

- [Helm v3](https://helm.sh/docs/intro/install/)
- A running Kubernetes cluster (e.g. minikube)

## Usage

### Install with the default tag (`latest`)

```bash
helm install appy ./charts/appy
```

### Install with a specific image tag

```bash
helm install appy ./charts/appy --set image.tag=develop-abc1234
helm install appy ./charts/appy --set image.tag=v1.0.0
```

### Upgrade a running release

```bash
helm upgrade appy ./charts/appy --set image.tag=v1.1.0
```

### Uninstall

```bash
helm uninstall appy
```

## Verify the deployment

```bash
kubectl get pods
kubectl get svc
```
