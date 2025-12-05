# NLP ETL Pipeline & Search System

This project consists of three main components:
1.  **NLP ETL Pipeline (PySpark)**: Processes documents from Hive/Files, cleans, chunks, embeds, and stores them.
2.  **Backend API (FastAPI)**: Provides vector search capabilities over the processed data.
3.  **Frontend App (React)**: A user interface to search and view documents.

## Prerequisites
- Python 3.8+
- Java 8+ (for PySpark)
- Node.js 16+
- SQLite (with `sqlite-vec` extension recommended for optimal performance)

## Setup & Running

### 1. Data Generation
Generate sample data for the pipeline:
```bash
python data/generate_data.py
```

### 2. ETL Pipeline
Install dependencies:
```bash
pip install pyspark sentence-transformers pandas pyarrow pyyaml
```

Run the pipeline:
```bash
export PYTHONPATH=$PYTHONPATH:.
python etl_pipeline/main.py
```
This will process data from `data/raw` and save outputs to `data/processed` and `data/processed/vector_db.sqlite`.

### 3. Backend API
Install dependencies:
```bash
pip install fastapi uvicorn pydantic-settings
```

Run the API:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
API Docs: http://localhost:8000/docs

### 4. Frontend Application
Install dependencies:
```bash
cd frontend
npm install
```

Run the App:
```bash
npm run dev
```
Open http://localhost:5173 to use the search interface.

## Architecture
- **ETL**: PySpark (Hive/File -> Preprocessing -> Chunking -> Embedding -> Local/SQLite)
- **Backend**: FastAPI + SQLite (Vector Search)
- **Frontend**: React + MUI
