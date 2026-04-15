# 🌦️ Kubernetes MPI Weather Processing

##  Description

This project demonstrates parallel data processing using MPI (Message Passing Interface) within a Kubernetes (MicroK8s) environment.

Each MPI process handles a weather dataset (CSV file) and computes the total sunshine duration for the year 2022.

---

##  Objectives

- Implement distributed computing using MPI  
- Deploy applications using Kubernetes (MicroK8s)  
- Containerize workloads using Docker  
- Process real-world datasets efficiently  

---

##  Architecture

- Kubernetes cluster (MicroK8s)
- Docker container with Python, OpenMPI, mpi4py
- MPI processes distributed across Pods
- Shared dataset directory

---

##  Features

- Parallel processing using MPI  
- Execution inside Kubernetes Pods  
- Docker-based reproducible environment  
- Weather dataset analysis  

---

##  Workflow

1. Each MPI process processes one dataset  
2. Filters data for the year 2022  
3. Computes sunshine duration  
4. Results are aggregated by the master process  

---

##  Main Script

app/mpi_sunshine_2022.py

---

##  Execution

### 1. Verify dataset

```bash
ls -l ~/k8s-mpi-weather/weather-data
```

### 2. Build Docker image
```bash
docker build -t ubuntu-mpi-py:latest .
```
### 3. Tag and push to MicroK8s registry
```bash
docker tag ubuntu-mpi-py:latest localhost:32000/ubuntu-mpi-py:latest
docker push localhost:32000/ubuntu-mpi-py:latest
```

### 4. Deploy Kubernetes resources
```bash
microk8s kubectl apply -f ~/k8s-mpi-weather/k8s-mpi.yaml
```
### 5. Check pods
```bash
microk8s kubectl get pods -o wide
```
### 6. Run MPI inside pod
```bash
microk8s kubectl exec -it mpi-pod-1 -- bash -c "mpirun --allow-run-as-root --oversubscribe -np 10 python3 /app/mpi_sunshine_2022.py"
```
## Technologies
- Kubernetes (MicroK8s)
- Docker
- MPI (OpenMPI, mpi4py)
-Python
## project structure
```
Kubernetes-MPI-Weather/
├── app/
│   └── mpi_sunshine_2022.py
├── Dockerfile
├── start.sh
├── k8s-mpi.yaml
├── weather-pods.yaml
├── weather-pv.yaml
├── weather-data/
└── README.md
```
## Dataset
- Source: Kaggle – Weather Data 2000–2023
- Only year 2022 is processed

## Author
- Chaimae Ababri
- Master Sécurité IT & Big Data – FST Tanger
