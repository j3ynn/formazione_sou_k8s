# Step 2 - Declarative Jenkins Pipeline (Groovy) for Docker Image Build

## Overview

This project implements a declarative Jenkins pipeline that builds a Docker image for a simple Flask "Hello World" web application and pushes it to Docker Hub. The pipeline dynamically determines the Docker image tag based on the Git reference (branch or tag) used to trigger the build.

## Repository Structure

```
.
├── Dockerfile        # Builds the Flask app image
├── app.py            # Flask application returning "Hello World!"
├── Jenkinsfile       # Declarative pipeline definition
└── README.md
```

## Flask Application

The application is a minimal Flask app exposing a single route that returns the string `Hello World!`. It is based on the example provided in the Docker awesome-compose repository (flask/app).

## Dockerfile

The Dockerfile uses a `python:3.10-alpine` base image, sets the working directory, copies `app.py`, installs Flask, and runs the application on port 8000.

## Jenkins Pipeline (Jenkinsfile)

The pipeline is named `flask-app-example-build` and is structured as follows.

### Pipeline Stages

1. **Set Image Tag**

   A `script` block calculates the Docker image tag dynamically based on the `GIT_BRANCH` and `GIT_COMMIT` environment variables provided by Jenkins:

   - If the build originates from the `master` branch, the tag is set to `latest`.
   - If the build originates from the `develop` branch, the tag is set to `develop-` followed by the first 7 characters of the Git commit SHA.
   - Otherwise (build triggered from a Git tag), the tag is set to the Git tag name (`TAG_NAME`).

   The resulting value is stored in the global variable `IMAGE_TAG`, declared at the top of the Jenkinsfile so it remains accessible across all subsequent stages.

2. **Login DockerHub**

   Retrieves Docker Hub credentials from Jenkins (stored as a `usernamePassword` credential, `dockerhub-credentials`) using `withCredentials`, and logs in to Docker Hub. The password is passed via `--password-stdin` rather than as a command-line argument, avoiding exposure of the credential in process listings or logs.

3. **Build**

   Builds the Docker image from the `Step2/` directory, tagging it locally as `flask-hello-world`.

4. **Tag**

   Re-tags the locally built image as `j3ynn/flask-hello-world:${IMAGE_TAG}`, using the dynamic tag computed in the first stage.

5. **Push**

   Pushes the tagged image to Docker Hub under the account `j3ynn`.

### Post Actions

A `post { always { ... } }` block ensures that `docker logout` is executed at the end of the pipeline regardless of whether the build succeeded or failed, preventing credentials from remaining cached on the agent.

## Image Tagging Logic Summary

| Build origin       | Resulting Docker image tag                  |
|---------------------|----------------------------------------------|
| `master` branch     | `latest`                                      |
| `develop` branch     | `develop-<short-commit-SHA>`                 |
| Git tag              | Same as the Git tag name                     |

## Infrastructure Notes

The pipeline runs on a Jenkins instance provisioned through a separate Infrastructure-as-Code setup (Vagrant + Ansible, Rocky Linux 9 VM), where Jenkins itself runs as a Docker container with access to the host's Docker daemon via a mounted socket.

During development, a permission issue was encountered when the Jenkins container attempted to use the Docker socket (`permission denied while trying to connect to the Docker daemon socket`). This was caused by a GID mismatch between the `docker` group inside the Jenkins container and the group owning the Docker socket on the VM host. The fix consisted of aligning the GID of the `docker` group inside the container with that of the host, and adding the `jenkins` user to that group. This fix was made permanent via additional tasks in the Ansible playbook so it is reapplied automatically on provisioning.
