# System Architecture

This document provides high-level diagrams for the NLP ETL Pipeline, Backend API, and Frontend Application.

## 1. ETL Pipeline

### 1.1 High-Level Process Flow
```mermaid
graph TD
    Start([Start]) --> Config[Load Configuration]
    Config --> InitSpark[Initialize Spark Session]
    InitSpark --> SourceDecide{Source Type?}
    
    SourceDecide -- Hive --> HiveSource[Read from Hive]
    SourceDecide -- File --> FileSource[Read from CSV/JSON]
    
    HiveSource --> Preprocess[Preprocessing\n(Clean Text, Remove URLs)]
    FileSource --> Preprocess
    
    Preprocess --> Chunking[Chunking\n(Fixed Size + Smoothing)]
    Chunking --> Embedding[Embedding Generation\n(Sentence-T5-Base)]
    
    Embedding --> Targets{Save Targets}
    Targets --> Local[Local Storage\n(Pickle/Parquet)]
    Targets --> SQLite[SQLite Vector DB\n(Data + Embeddings)]
    
    Local --> Stop([End])
    SQLite --> Stop
```

### 1.2 High-Level Sequence Diagram
```mermaid
sequenceDiagram
    participant Main
    participant Pipeline
    participant SourceFactory
    participant Preprocessor
    participant Chunker
    participant Embedder
    participant TargetFactory
    
    Main->>Pipeline: run()
    activate Pipeline
    
    Pipeline->>SourceFactory: get_source(config)
    SourceFactory-->>Pipeline: Source Instance
    Pipeline->>SourceInstance: read()
    SourceInstance-->>Pipeline: Raw DataFrame
    
    Pipeline->>Preprocessor: process(Raw DF)
    Preprocessor-->>Pipeline: Cleaned DataFrame
    
    Pipeline->>Chunker: process(Cleaned DF)
    Chunker-->>Pipeline: Chunked DataFrame
    
    Pipeline->>Embedder: process(Chunked DF)
    Embedder-->>Pipeline: Embedded DataFrame
    
    Pipeline->>TargetFactory: get_target(config)
    TargetFactory-->>Pipeline: Target Instance
    Pipeline->>TargetInstance: write(Embedded DF)
    TargetInstance-->>Pipeline: Success
    
    deactivate Pipeline
    Main->>Main: Stop Spark
```

## 2. Backend API

### 2.1 High-Level Process Flow
```mermaid
graph TD
    Request([Client Request]) --> Router[FastAPI Router]
    Router --> RouteDecide{Route?}
    
    RouteDecide -- POST /search --> SearchService[Search Service]
    SearchService --> Embed[Embed Query\n(Sentence-T5)]
    Embed --> VectorSearch[Vector Search\n(Cosine Similarity in SQLite)]
    VectorSearch --> Format[Format Results]
    Format --> Response([Return JSON])
    
    RouteDecide -- GET /document/{id} --> DocService[Document Service]
    DocService --> DBQuery[Query SQLite by ID]
    DBQuery --> DocResponse([Return Document])
```

### 2.2 High-Level Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant API_Endpoint
    participant SearchService
    participant EmbeddingModel
    participant SQLite_DB
    
    Client->>API_Endpoint: POST /search (query="...")
    activate API_Endpoint
    
    API_Endpoint->>SearchService: search(query)
    activate SearchService
    
    SearchService->>EmbeddingModel: encode(query)
    EmbeddingModel-->>SearchService: query_vector
    
    SearchService->>SQLite_DB: execute(SELECT ... ORDER BY vector_distance)
    SQLite_DB-->>SearchService: rows (chunks + scores)
    
    SearchService-->>API_Endpoint: List[SearchResult]
    deactivate SearchService
    
    API_Endpoint-->>Client: 200 OK (JSON)
    deactivate API_Endpoint
```

## 3. Frontend Application

### 3.1 High-Level Process Flow
```mermaid
graph TD
    UserOpen([User Opens App]) --> Render[Render App Component]
    Render --> RenderSearch[Render SearchBar]
    Render --> RenderGrid[Render ResultsGrid]
    
    UserAction{User Action}
    
    UserAction -- Type Query --> InputState[Update Query State]
    UserAction -- Click Search --> CallAPI[Call searchDocuments()]
    
    CallAPI --> Overlay[Show Loading Overlay]
    Overlay --> Axios[Axios POST /search]
    Axios --> Receive[Receive Data]
    Receive --> UpdateResults[Update Results State]
    UpdateResults --> HideOverlay[Hide Overlay]
    HideOverlay --> ReRenderGrid[Re-Render ResultsGrid]
    
    UserAction -- Click Result --> OpenViewer[Open DocumentViewer]
    OpenViewer --> FetchDoc[Call getDocument()]
    FetchDoc --> ShowDoc[Display Full Text]
```

### 3.2 High-Level Sequence Diagram
```mermaid
sequenceDiagram
    actor User
    participant App_Component
    participant SearchBar
    participant API_Service
    participant Backend_API
    
    User->>SearchBar: Types "Project Plan"
    User->>SearchBar: Clicks "Search"
    
    SearchBar->>App_Component: onSearch("Project Plan")
    activate App_Component
    
    App_Component->>App_Component: setSearching(true)
    App_Component->>API_Service: searchDocuments("Project Plan")
    activate API_Service
    
    API_Service->>Backend_API: POST /search
    Backend_API-->>API_Service: JSON Response
    
    API_Service-->>App_Component: SearchResult[]
    deactivate API_Service
    
    App_Component->>App_Component: setResults(data)
    App_Component->>App_Component: setSearching(false)
    
    App_Component-->>User: Displays Results Cards
    deactivate App_Component
```

## 4. Class Diagrams

### 4.1 ETL Pipeline & Backend Classes
```mermaid
classDiagram
    %% ETL Pipeline Classes
    namespace ETL_Pipeline {
        class Pipeline {
            +SparkSession spark
            +Dict config
            +run()
        }
        
        class DataSourceFactory {
            +get_source(type, config)
        }
        
        class DataSource {
            <<interface>>
            +read() DataFrame
        }
        
        class FileSource {
            +read() DataFrame
        }
        
        class HiveSource {
            +read() DataFrame
        }
        
        class TextCleaner {
            +process(df) DataFrame
        }
        
        class FixedSizeChunker {
            +process(df) DataFrame
        }
        
        class T5Embedder {
            +process(df) DataFrame
        }
        
        class TargetFactory {
            +get_target(type, config)
        }
        
        class SQLiteSink {
            +write(df, stage)
        }
    }

    %% Backend Classes
    namespace Backend {
        class SearchRequest {
            +str query
            +int limit
        }
        
        class SearchResult {
            +str doc_id
            +str chunk_id
            +str text
            +float score
        }
        
        class SearchService {
            +SentenceTransformer model
            +search(query) List~SearchResult~
            +get_document(doc_id) Dict
        }
        
        class Database {
            +get_db_connection()
        }
    }

    %% Relationships
    Pipeline --> DataSourceFactory
    DataSourceFactory ..> DataSource
    DataSource <|-- FileSource
    DataSource <|-- HiveSource
    
    Pipeline --> TextCleaner
    Pipeline --> FixedSizeChunker
    Pipeline --> T5Embedder
    Pipeline --> TargetFactory
    TargetFactory ..> SQLiteSink
    
    SearchService --> Database : uses
    SearchService ..> SearchRequest : consumes
    SearchService ..> SearchResult : produces
```
