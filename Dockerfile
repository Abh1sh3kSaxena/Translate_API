# Build stage for React frontend
FROM node:16-alpine as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Build stage for Python dependencies and model
FROM python:3.11-slim as builder
WORKDIR /app

# Create static directory and copy frontend build
RUN mkdir -p /app/static
COPY --from=frontend-builder /app/frontend/build/static /app/static

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and save only the necessary model files
RUN mkdir -p /app/model && \
    python -c "from transformers import MarianMTModel, MarianTokenizer; \
    model_name='Helsinki-NLP/opus-mt-en-fr'; \
    tokenizer = MarianTokenizer.from_pretrained(model_name); \
    model = MarianMTModel.from_pretrained(model_name); \
    tokenizer.save_pretrained('/app/model'); \
    model.save_pretrained('/app/model')" && \
    rm -rf /root/.cache

# Final stage
FROM python:3.11-slim
WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code

# Expose port 8080 for Cloud Run
EXPOSE 8080
COPY app ./app
COPY --from=frontend-builder /app/frontend/build/* ./static/
COPY --from=builder /app/model ./model
COPY --from=builder /app/static ./static/static

# Set environment variables
ENV MODEL_DIR=/app/model
ENV PYTHONPATH=/app
ENV FLASK_APP=app.main:app
ENV FLASK_ENV=production

# Clean up unnecessary files
RUN find . -type d -name "__pycache__" -exec rm -r {} + && \
    find . -type f -name "*.pyc" -delete

# Start the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port", "8080"]