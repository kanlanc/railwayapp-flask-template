from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
        # Log the request details
        logger.info("Webhook received - Headers: %s", dict(request.headers))
        logger.info("Webhook received - Data: %s", data)
        logger.info("Webhook received - Remote Address: %s", request.remote_addr)
        
        return jsonify({
            "message": "Webhook received",
            "data": data
        }), 200
    
    logger.warning("Non-JSON request received at webhook endpoint")
    return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
