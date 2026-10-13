# ACEest Fitness & Gym — DevOps CI/CD Pipeline

**Author:** Gyanendra Sinha  
**Course:** Introduction to DEVOPS (Merged - CSIZG514/SEZG514) (S1-26) — Assignment 1

## Project Overview

This repository contains a modular Flask web application for ACEest Fitness & Gym, supported by an automated CI/CD pipeline. The project uses Git for version control, Pytest for unit testing, Docker for containerization, Jenkins for local build validation, and GitHub Actions for remote pipeline orchestration.

---

## Assignment Execution Steps

The following phases describe the procedure used to build and validate the project.

### Phase 1: Application Setup and Modularization

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python3 app.py
   ```

4. **Access the application:** Open a browser and navigate to `http://127.0.0.1:5000`. Log in using `admin` / `admin`.

### Phase 2: Version Control System (VCS) Strategy

1. **Initialize Git and configure branching:**

   ```bash
   git init
   git branch -M main
   git checkout -b feature/docker-ci-pipeline
   ```

2. **Commit the baseline code and push the feature branch to GitHub:**

   ```bash
   git add .
   git commit -m "feat: initialize Flask application structure and test suite"
   git remote add origin https://github.com/2025tm93008GyanendraSinha/aceest-fitness-devops.git
   git push -u origin feature/docker-ci-pipeline
   ```

### Phase 3: Unit Testing and Validation Framework

1. **Run the Pytest suite and generate a coverage report:**

   ```bash
   python3 -m pytest -v --cov=app tests/
   ```

2. **Run Flake8 to check for selected syntax and code errors:**

   ```bash
   flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics
   ```

### Phase 4: Containerization with Docker

1. **Build the Docker image:**

   ```bash
   docker build -t aceest-fitness-app:latest .
   ```

2. **Run the containerized application:**

   ```bash
   docker run -d -p 5000:5000 --name aceest-container aceest-fitness-app:latest
   ```

### Phase 5: Jenkins Build and Quality Gate

A declarative Jenkins pipeline (`Jenkinsfile`) is configured to handle the primary build and validation phase locally.

1. Jenkins is configured to use **Poll SCM** with the schedule `H/2 * * * *`, checking for repository changes approximately every two minutes.
2. When changes are detected, Jenkins runs a build on the configured agent, installs dependencies, and executes the Pytest suite as an additional validation layer.

### Phase 6: Automated CI/CD with GitHub Actions

The GitHub Actions workflow at `.github/workflows/main.yml` is configured to run on every `push` and `pull_request`. It performs the following stages:

1. **Build and lint:** Provisions an Ubuntu runner, sets up Python 3.9, and runs Flake8 to validate code integrity.
2. **Docker image assembly:** Builds the Docker image using the project `Dockerfile`, a lightweight Python base image, and a non-root user.
3. **Automated container testing:** Starts the newly built Docker container and runs the Pytest suite inside the isolated environment to validate the containerized application.

---

## Repository

[ACEest Fitness DevOps on GitHub](https://github.com/2025tm93008GyanendraSinha/aceest-fitness-devops)
