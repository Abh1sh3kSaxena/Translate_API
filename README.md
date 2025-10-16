# Offline English→French Translator API

This is a small FastAPI service that translates English text into French using an offline Hugging Face MarianMT model (or a locally cached model).

Features
- FastAPI HTTP API with POST /translate
- Uses Transformers MarianMT model for EN->FR
- Supports loading model from a local directory (for offline environments)

Quick start (PowerShell)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Download the model (one-time, requires internet). Example using Hugging Face model `Helsinki-NLP/opus-mt-en-fr`:

```powershell
python -c "from transformers import MarianTokenizer, MarianMTModel; MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-fr', cache_dir='./model_cache'); MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-en-fr', cache_dir='./model_cache')"
```

This will save model files into `./model_cache` which you can later move to an offline machine.

3. Run the app and point `MODEL_DIR` to the cache if needed:

```powershell
$env:MODEL_DIR = "${PWD}\model_cache"; uvicorn app.main:app --reload --port 8000
```

4. Example request:

```powershell
curl -X POST http://localhost:8000/translate -H "Content-Type: application/json" -d '{"text":"Hello, how are you?"}'
```

Notes
- If you have no internet when starting the server, set `MODEL_DIR` to a local directory containing the model files (tokenizer.json, pytorch_model.bin, config.json, etc.).
- Model selection: the code defaults to `Helsinki-NLP/opus-mt-en-fr`. You can change `MODEL_NAME` env var.

License: MIT
