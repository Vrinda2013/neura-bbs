from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/emails', methods=['GET'])
def get_emails():
    try:
        # Check if we have credentials
        if not os.path.exists('token.pkl'):
            return jsonify({
                "error": "Not authenticated",
                "message": "Please complete Gmail OAuth setup",
                "setup_required": True
            }), 401
        
        # Try to fetch emails
        from fetch_emails import fetch_emails
        emails = fetch_emails()
        return jsonify(emails)
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Gmail API error - check your credentials",
            "setup_required": True
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "Backend is running",
        "gmail_authenticated": os.path.exists('token.pkl')
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
