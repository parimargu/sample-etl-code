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
pip install -r etl_pipeline/requirements.txt
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
pip install -r backend/requirements.txt
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

## Running Tests

### ETL Pipeline Tests
To run unit tests for the ETL pipeline, ensure you are in the project root directory and have `pytest` installed.

```bash
# Install test dependencies if not already done
pip install pytest

# Run tests
export PYTHONPATH=$PYTHONPATH:.
pytest etl_pipeline/tests
```

### Backend API Tests
To run unit tests for the Backend API, navigate to the backend directory.

```bash
cd backend
# Install test dependencies if not already done
pip install pytest httpx

# Run tests
pytest tests
```

## Code Coverage

To generate HTML code coverage reports, you **must** install `pytest-cov`.

### ETL Pipeline Coverage
```bash
# 1. Install dependencies (ensure pytest-cov is installed)
pip install -r etl_pipeline/requirements.txt
# OR explicitly:
pip install pytest-cov

# 2. Run tests with coverage
export PYTHONPATH=$PYTHONPATH:.
pytest --cov=etl_pipeline --cov-report=html etl_pipeline/tests
```
The report will be generated in `htmlcov/index.html`.

### Backend API Coverage
```bash
cd backend
# 1. Install dependencies
pip install -r requirements.txt
# OR explicitly:
pip install pytest-cov

# 2. Run tests with coverage
pytest --cov=app --cov-report=html tests
```
The report will be generated in `backend/htmlcov/index.html`.

## Architecture
- **ETL**: PySpark (Hive/File -> Preprocessing -> Chunking -> Embedding -> Local/SQLite)
- **Backend**: FastAPI + SQLite (Vector Search)
- **Frontend**: React + MUI
