from flask import Flask, request, jsonify, render_template, send_from_directory
from openai import OpenAI
import os
from flask_cors import CORS
from waitress import serve
from dotenv import load_dotenv
import logging

# Configuration
load_dotenv()
app = Flask(__name__)

# CORS Configuration for Angular development
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:4200"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

PORT = int(os.getenv('PORT', 5002))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')

# Angular dist directory path
ANGULAR_DIST_DIR = os.path.join(os.path.dirname(__file__), '..', 'angular-dist')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask UI routes
@app.route('/flask-ui')
def flask_ui():
    """Alternative route for original Flask interface"""
    return render_template('index.html')

# Angular serving route (production)
@app.route('/')
def serve_angular():
    if FLASK_ENV == 'production' and os.path.exists(ANGULAR_DIST_DIR):
        return send_from_directory(ANGULAR_DIST_DIR, 'index.html')
    return render_template('index.html')  # Fallback to Flask interface

# Static files route for Angular
@app.route('/<path:path>')
def serve_static(path):
    if FLASK_ENV == 'production' and os.path.exists(ANGULAR_DIST_DIR):
        full_path = os.path.join(ANGULAR_DIST_DIR, path)
        if os.path.exists(full_path):
            return send_from_directory(ANGULAR_DIST_DIR, path)
    return send_from_directory('static', path)

# Chat API endpoint
@app.route('/api/chat', methods=['POST'])
def handle_query():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_query = data.get('query', '').strip()

    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    try:
        # Get response from GPT
        response = get_gpt_response(user_query)
        
        return jsonify({
            "query": user_query,
            "response": response,
            "success": True
        })

    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return jsonify({"error": "Internal server error", "success": False}), 500

def get_gpt_response(prompt: str) -> str:
    """
    Get a response from GPT model for the given prompt
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # You can also use "gpt-3.5-turbo" for a faster, cheaper option
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides accurate and informative responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Balanced between creativity and accuracy
            max_tokens=500    # Adjust based on your needs
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI query failed: {str(e)}")
        return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    if FLASK_ENV == 'development':
        logging.info("Running in development mode (Flask UI)")
        app.run(host='0.0.0.0', port=PORT, debug=DEBUG, use_reloader=False)
    else:
        if os.path.exists(ANGULAR_DIST_DIR):
            logging.info(f"Serving Angular app from {ANGULAR_DIST_DIR}")
        else:
            logging.warning("Angular dist directory not found, falling back to Flask UI")
        
        logging.info(f"\n=== Server running on: http://0.0.0.0:{PORT} ===")
        logging.info(f"=== Access locally via: http://127.0.0.1:{PORT} ===")
        logging.info(f"=== API endpoint: http://127.0.0.1:{PORT}/api/chat ===\n")
        
        serve(app, host='0.0.0.0', port=PORT)