from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from typing import Optional
from http import HTTPStatus
import os

from .translator import get_translator



# Configure static files handling
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
app = Flask(__name__, static_folder=None)  # We'll handle static files manually
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://translator-api-843246270197.us-central1.run.app",
            "http://localhost:3000",
            "http://localhost:5000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.before_request
def log_request_info():
    app.logger.debug('Request Path: %s', request.path)
    if os.path.exists(static_folder):
        app.logger.debug('Static folder contents: %s', os.listdir(static_folder))

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory(static_folder, filename)
    except Exception as e:
        app.logger.error(f"Error serving static file {filename}: {str(e)}")
        return f"Error serving static file: {str(e)}", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    try:
        # Special case for /static/ paths
        if path.startswith('static/'):
            static_file = path[7:]  # Remove 'static/' prefix
            if os.path.isfile(os.path.join(static_folder, static_file)):
                return send_from_directory(static_folder, static_file)
        
        # Try to serve as-is if file exists
        if path and os.path.isfile(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)
        
        # Default to serving index.html
        return send_from_directory(static_folder, 'index.html')
    except Exception as e:
        app.logger.error(f"Error serving file {path}: {str(e)}")
        # Always fall back to index.html
        return send_from_directory(static_folder, 'index.html')
    except Exception as e:
        app.logger.error(f"Error serving file: {str(e)}")
        return send_from_directory(static_folder, 'index.html')

@app.route('/_ah/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({"status": "healthy"}), HTTPStatus.OK

@app.route('/translate', methods=['POST'])
def translate():
    req = request.get_json()
    if not req or 'text' not in req:
        return jsonify({"error": "Missing 'text' field"}), HTTPStatus.BAD_REQUEST
    
    max_length = req.get('max_length', 256)
    translator = get_translator()
    
    try:
        out = translator.translate(req['text'], max_length=max_length)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    return jsonify({"translation": out}), HTTPStatus.OK

if __name__ == '__main__':
    # Cloud Run will set PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
