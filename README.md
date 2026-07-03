# Secure Semantic Search API

A robust, AI-powered semantic search engine that bridges natural language queries with structured SQL data. Built with FastAPI and containerized with Docker, this service ensures secure, high-performance data retrieval.

## Tech Stack
- Framework: FastAPI
- AI Engine: Groq Cloud
- Orchestration: Docker & Docker Compose
- Database: SQLite

## Project Structure
```text
secure_semantic_search/
├── app/                  # Core application logic (Security, Engine, DB)
├── company_data.db       # Local SQLite database
├── Dockerfile            # Blueprint for the container image
├── docker-compose.yml    # Service orchestration
├── requirements.txt      # Project dependencies[cite: 1]
└── .gitignore            # Clean repository management
```

### Getting Started
#### Prerequisites
Docker Desktop installed and running.

#### Installation
1. Clone the repository:
```text
git clone https://github.com/karpagameenal-leo/Secure-Semantic-Search
cd secure_semantic_search
```

2. Launch the Application:
Run this command to build and start the service:
```text
docker compose up -d
```

3. Access the API:
Open your browser and navigate to http://localhost:8000/docs to view the interactive Swagger UI and start testing your queries.

### Security Features
This API includes a custom Security Firewall implemented in security.py. It sanitizes all incoming user prompts, stripping malicious SQL patterns to ensure database integrity.

### Stopping the Service
To stop the background container when you are finished, run:
```text
docker compose down
```