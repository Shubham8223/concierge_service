# Concierge Service

A full-stack concierge service application with FastAPI backend and Streamlit frontend.

## Architecture

- **Backend**: FastAPI with LangGraph and LangChain (managed by Poetry)
- **Frontend**: Streamlit interface (managed by Poetry)
- **Default LLM**: Claude 3.7 via AWS Bedrock
- **Supported Providers**: AWS Bedrock, Together AI, Groq
- **Supported Models**: Anthropic (Claude) and Meta models

## Installation

### Prerequisites

- Python 3.9+
- Poetry
- Docker (optional - each service has its own Dockerfile)

### Setup

1. Clone the repository

2. **Backend Setup**:

   ```bash
   cd concierge_service_backend
   cp .env.template .env
   # Edit .env with your configuration
   poetry install --no-interaction --no-ansi --no-root
   ```

3. **Frontend Setup**:
   ```bash
   cd concierge_service_frontend
   cp .env.template .env
   # Edit .env with your configuration
   poetry install --no-interaction --no-ansi --no-root
   ```

### Running the Application

1. **Start the Backend**:

   ```bash
   cd concierge_service_backend
   poetry run uvicorn server.main:app --host 0.0.0.0 --port 8080 --reload
   ```

2. **Start the Frontend** (in a new terminal):
   ```bash
   cd concierge_service_frontend
   poetry run streamlit run app.py
   ```

## Configuration

Each service has its own `.env.template` file:

- `concierge_service_backend/.env.template` - Backend configuration
- `concierge_service_frontend/.env.template` - Frontend configuration

Copy these templates to `.env` files and fill in your specific values.

### LLM Configuration

The application uses **Claude 3.7** via **AWS Bedrock** by default. You can configure different providers and models:

- **AWS Bedrock**: Anthropic Claude models
- **Together AI**: Various Anthropic and Meta models
- **Groq**: Fast inference for supported models

Update your `.env` files to switch between providers and models as needed.

## Services

- **Backend API**: http://localhost:8080
- **Frontend Interface**: http://localhost:8501 (default Streamlit port)
- **API Endpoint**: http://localhost:8080/api/v1/agent/call-concierge-service

## Example Usage

Note: All example inputs and outputs in example.json were generated on 25-05-25 at 7:51 IST
Refer to example.json for sample API requests and responses.
