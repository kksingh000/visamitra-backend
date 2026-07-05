# Visamitra Backend

Backend service for **Visamitra** — a platform for stock price prediction and AI-based crypto trading analysis. Built with Python and containerized for easy deployment.

## Features

- REST API for stock price prediction models
- Crypto trading data processing and analysis endpoints
- Environment-based configuration for secure deployments
- Docker support for consistent local and production environments

## Tech Stack

- **Language:** Python
- **Containerization:** Docker
- **Deployment:** Render
- **Dependencies:** See `requirements.txt`

## Project Structure -

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- Docker (optional, for containerized run)

### Local Setup

```bash
git clone https://github.com/kksingh000/visamitra-backend.git
cd visamitra-backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Fill in your actual environment values
python app/main.py         # Adjust entry point as needed
```

### Docker Setup

```bash
docker build -t visamitra-backend .
docker run -p 8000:8000 --env-file .env visamitra-backend
```

## Environment Variables

Copy `.env.example` to `.env` and configure the required values (API keys, database URLs, secret keys, etc.) before running the app.

## Deployment

This backend is deployed on [Render](https://render.com). Push changes to the `main` branch to trigger deployment (if auto-deploy is configured).

## Contributing

This is an academic project by Krishna Kumar Singh. Contributions, issues, and feature requests are welcome.

## License

This project is currently unlicensed. Add a `LICENSE` file if you plan to open-source it.
