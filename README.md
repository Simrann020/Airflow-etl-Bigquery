# Airflow ETL with BigQuery

This project implements an **ETL (Extract, Transform, Load) pipeline** using **Apache Airflow** and **Google BigQuery**.  
It is designed to automate data ingestion, transformation, and loading processes for scalable analytics.

---

## Features
- **Apache Airflow** DAGs to orchestrate ETL workflows  
- Integration with **Google BigQuery** for storage and querying  
- **Dockerized environment** with `docker-compose` for easy local setup  
- Configurable via `.env` and externalized secrets (not committed to Git)  
- Modular structure for adding new DAGs and plugins  

---

## 📂 Project Structure
```
airflow-etl-bigquery/
│── dags/                  # Airflow DAG definitions
│── data/                  # Raw/processed data (local only, not in Git)
│── include/               # Helper scripts and configs
│   └── gcp-key.json       # GCP service account key
│── logs/                  # Airflow logs
│── plugins/               # Custom Airflow operators & hooks
│── .env                   # Environment variables
│── docker-compose.yml     # Dockerized Airflow setup
│── Dockerfile             # Custom Airflow image
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Simrann020/Airflow-etl-Bigquery.git
cd airflow-etl-bigquery
```

### 2. Setup Environment Variables
- Copy `.env.example` to `.env`
- Fill in required environment variables (BigQuery project ID, dataset, etc.)

### 3. Start Airflow
```bash
docker-compose up --build
```

Airflow UI will be available at [http://localhost:8080](http://localhost:8080).

### 4. Run a DAG
- Trigger DAGs from Airflow UI  
- Monitor logs and execution status
