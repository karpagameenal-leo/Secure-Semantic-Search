# Secure Semantic Search API

A robust, AI-powered semantic search engine that bridges natural language queries with structured SQL data. Built with FastAPI and containerized with Docker, this service ensures secure, high-performance data retrieval.

## Tech Stack
- Framework: FastAPI[cite: 1]
- AI Engine: Groq Cloud
- Orchestration: Docker & Docker Compose
- Database: SQLite[cite: 3]

## Project Structure
```text
secure_semantic_search/
├── app/                  # Core application logic (Security, Engine, DB)
├── company_data.db       # Local SQLite database
├── Dockerfile            # Blueprint for the container image
├── docker-compose.yml    # Service orchestration
├── requirements.txt      # Project dependencies[cite: 1]
└── .gitignore            # Clean repository management

### Getting Started
#### Prerequisites
Docker Desktop installed and running.

#### Installation
1. Clone the repository:
git clone <your-repo-url>
cd secure_semantic_search

2. Launch the Application:
Run this command to build and start the service:
docker compose up -d

3. Access the API:
Open your browser and navigate to http://localhost:8000/docs to view the interactive Swagger UI and start testing your queries[cite: 3].

### Security Features
This API includes a custom Security Firewall implemented in security.py. It sanitizes all incoming user prompts, stripping malicious SQL patterns to ensure database integrity[cite: 3].

### Stopping the Service
To stop the background container when you are finished, run:
docker compose down