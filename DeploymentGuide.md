# Deployment Guide

## Overview
This guide explains how to deploy the Flask-MySQL application both **locally using Docker Compose** and **in Azure using Azure Container Instances (ACI)**.

# 1️⃣ Local Deployment using Docker Compose

### **Step 1: Configure Environment Variables**
Create a `.env` file at the root of the project and set the following values:
```ini
DB_HOST=mysql-db
DB_PORT=3306
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_NAME=<your_db_name>

MYSQL_ROOT_PASSWORD=<your_root_password>
MYSQL_DATABASE=<your_db_name>
API_USER=<your_api_user>
API_PASSWORD=<your_api_password>
```

### **Step 2: Build and Start Containers**
Run the following command to build and start all services:
```sh
docker-compose up --build -d
```
This will start three containers:
1. **MySQL Database** (`mysql-db`)
2. **Flask API** (`flask-api`)
3. **Frontend App** (`frontend-app`)

### **Step 3: Access the Services**
- **API:** `http://localhost:5000/`
- **Frontend:** `http://localhost:8080/`
- **MySQL:** Connect via `localhost:3307`

### **Step 4: Stop and Remove Containers**
To stop the services, run:
```sh
docker-compose down
```

---

# 2️⃣ Deployment in Azure using ACI

## **1. Build and Push Images to Azure Container Registry (ACR)**
### **Step 1: Log in to Azure ACR**
```sh
az acr login --name <your-acr-name>
```

### **Step 2: Tag and Push Images**
```sh
docker tag flask-api <your-acr-name>.azurecr.io/flask-mysql-app-flask-api:latest
docker tag mysql-db <your-acr-name>.azurecr.io/flask-mysql-app-mysql-db:latest

docker push <your-acr-name>.azurecr.io/flask-mysql-app-flask-api:latest
docker push <your-acr-name>.azurecr.io/flask-mysql-app-mysql-db:latest
```

---

## **2. Deploy Backend & Database in Azure**
Run the following command to deploy the **database and API** in Azure:
```sh
az container create --resource-group <your-resource-group> --file ACI-DB-API.yaml
```

This will:
✅ Deploy MySQL and the Flask API in **Azure Container Instances**.
✅ Expose the API on port **5000**.
✅ Expose MySQL on port **3306**.

Once deployed, get the public IP of the **Flask API**:
```sh
az container show --resource-group <your-resource-group> --name <your-container-group> --query "ipAddress.ip" --output tsv
```
Copy the obtained IP and update `config.js` in the frontend:
```js
const API_BASE_URL = "http://<api-public-ip>:5000";
```

Then, rebuild and push the frontend image:
```sh
docker build -t <your-acr-name>.azurecr.io/flask-mysql-app-frontend-app:latest ./frontend

docker push <your-acr-name>.azurecr.io/flask-mysql-app-frontend-app:latest
```

---

## **3. Deploy Frontend in Azure**
Run the following command to deploy the **frontend** in Azure:
```sh
az container create --resource-group <your-resource-group> --file ACI-FRONT.yaml
```

To check the frontend's public IP:
```sh
az container show --resource-group <your-resource-group> --name <your-frontend-container> --query "ipAddress.ip" --output tsv
```

Access the frontend using the IP shown.

---
