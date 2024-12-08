# HAMF Framework Deployment with Docker
## Overview
This guide explains how to deploy the HAMF framework using Docker containers, manage the framework codebase with GitLab CE, and automate the deployment process using GitLab CI/CD.
***
## Prerequisites
## 1. Docker Installed:
- Install Docker: Docker Installation Guide.
- Install Docker Compose: Compose Installation Guide.
## 2. GitLab CE Installed:
- Self-hosted GitLab CE instance or use GitLab.com.
- Ensure GitLab Runners are configured for CI/CD.
## 3. Environment Configuration:
- Prepare .env files for sensitive data (e.g., API keys, database credentials).

***

## Step 1: Set Up the Framework in GitLab
## 1. Create a Repository:
- Push the HAMF framework to a GitLab repository:
```sh
git init
git remote add origin https://github.com/asmaareda/HAMF.git
git add .
git commit -m "Initial commit"
git push -u origin main
```
## 2. Add a [.gitlab-ci.yml] File: Define a CI/CD pipeline for automated builds and deployments:
```sh
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2

build:
  stage: build
  script:
    - docker build -t hamf-custom-env .
    - docker-compose build
  tags:
    - docker

test:
  stage: test
  script:
    - docker-compose up -d
    - docker-compose exec hamf-custom-env python -m unittest discover
  tags:
    - docker

deploy:
  stage: deploy
  script:
    - docker-compose up -d
  tags:
    - docker
```
***
## Step 2: Docker Compose Multi-Container Setup
1. **Update** docker-compose.yml: Add services for HAMF, GitLab, and additional tools (Grafana, Slack integration):
```sh
version: '3.9'

services:
  hamf-custom-env:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: hamf-custom-env
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    depends_on:
      - grafana

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=securepassword
    volumes:
      - grafana-data:/var/lib/grafana

  gitlab-ce:
    image: gitlab/gitlab-ce:latest
    container_name: gitlab
    ports:
      - "8080:80"
      - "8443:443"
      - "8022:22"
    volumes:
      - gitlab-config:/etc/gitlab
      - gitlab-logs:/var/log/gitlab
      - gitlab-data:/var/opt/gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://localhost:8080'

volumes:
  grafana-data:
  gitlab-config:
  gitlab-logs:
  gitlab-data:
```
***
## Step 3: Build and Deploy with Docker
1. **Start the Containers:**
```sh
docker-compose up -d
```
2. **Access Services:**
```sh
docker logs hamf-custom-env
```
3. **Monitor Deployment:**
```sh
docker ps
```
***
## Step 4: Automate Deployments with GitLab CI/CD
1. **Commit and Push Changes:**
- Any code updates in the repository will trigger the GitLab pipeline.
2. **Monitor CI/CD Pipelines:**
- Access the CI/CD dashboard in GitLab for pipeline execution and logs.
***
## Step 5: Extend with Additional Tools
1. **Slack Notifications:**
- Integrate Slack alerts in the GitLab pipeline by adding webhook configurations in .gitlab-ci.yml.
2. **Documentation with BookStack:**
- Include BookStack for documentation hosting in docker-compose.yml.
3. **Scaling and Optimization:**
- Scale the HAMF environment for larger workloads:
```sh
deploy:
  replicas: 3
```
