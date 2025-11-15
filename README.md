# English to French Translator

A full-stack application that provides English to French translation using the Helsinki-NLP/opus-mt-en-fr model. The application includes both a REST API and a React-based web interface.

## Features

- ✨ Real-time English to French translation
- 🚀 RESTful API endpoints
- 🌐 React web interface with Material-UI
- 🐳 Docker containerization
- 🔄 Health check endpoint
- ⚡ Fast translation using pre-trained models
- 📱 Responsive design

## Quick Start with Docker

The easiest way to run the application is using Docker:

```bash
# Clone the repository
git clone https://github.com/Abh1sh3kSaxena/Translate_API.git
cd Translate_API

# Build and run with Docker Compose
docker-compose up --build
```

The application will be available at:
- Web Interface: http://localhost:5000
- API Endpoint: http://localhost:5000/translate

## API Documentation

### Health Check
```http
GET /health
```
Returns the health status of the application.

**Response**
```json
{
    "status": "healthy"
}
```

### Translation
```http
POST /translate
```

**Request Body**
```json
{
    "text": "Hello, how are you?",
    "max_length": 256
}
```

**Response**
```json
{
    "translation": "Bonjour, comment allez-vous ?"
}
```

## Development Setup

### Backend Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python -m flask run
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Code Structure

### Backend (Flask)

The main application logic is in `app/main.py`:

```python
# Routes:
GET /health          # Health check endpoint
POST /translate      # Translation endpoint
GET /               # Serves the React frontend
GET /static/*       # Serves static files for frontend
```

Key components:
- Flask web server with CORS support
- MarianMT translation model integration
- Static file serving for React frontend
- Error handling and validation

### Frontend (React)

The React frontend (`frontend/src/App.js`) provides:
- Two-panel interface for input and translation
- Translation button with loading state
- Error handling and user feedback
- Responsive Material-UI design

# Translator API - GCP Permissions Guide

## Required IAM Roles and Permissions

### Service Account Permissions
The following roles need to be granted to your service account:

1. **Artifact Registry**
   - `roles/artifactregistry.writer` - Upload container images
   - `roles/artifactregistry.repositories.uploadArtifacts` - Push artifacts

2. **Cloud Run**
   - `roles/run.admin` - Manage Cloud Run services
   - `roles/run.invoker` - Invoke Cloud Run services

3. **IAM**
   - `roles/iam.serviceAccountUser` - Act as service account
   - `roles/iam.serviceAccountTokenCreator` - Create tokens

4. **Logging**
   - `roles/logging.logWriter` - Write logs to Cloud Logging

## Setup Commands

```bash
# Set your project ID
PROJECT_ID="[your-project-id]"
SERVICE_ACCOUNT="translator-api-sa@[your-project-id].iam.gserviceaccount.com"

# Grant Artifact Registry permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/artifactregistry.writer"

# Grant Cloud Run permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/run.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/run.invoker"

# Grant IAM permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/iam.serviceAccountTokenCreator"

# Grant Logging permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/logging.logWriter"
```

## Deployment Flow
1. Build container image
2. Push to Artifact Registry
3. Deploy to Cloud Run

Each step requires specific permissions as detailed above.

## Environment Variables

- `MODEL_DIR`: Path to store the downloaded model (optional)
- `MODEL_NAME`: HuggingFace model name (default: "Helsinki-NLP/opus-mt-en-fr")
- `FLASK_ENV`: Flask environment (development/production)

## Notes
- First run will download the translation model
- For offline use, set `MODEL_DIR` to a directory containing the model files
- Model files include: tokenizer.json, pytorch_model.bin, config.json
- Default model is `Helsinki-NLP/opus-mt-en-fr`

## License

This project is licensed under the MIT License


