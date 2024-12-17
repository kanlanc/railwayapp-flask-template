from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Store recent webhooks in memory (for demonstration)
webhook_history = []

@app.route('/')
def index():
    # Show instructions and webhook URL
    webhook_url = request.url_root + 'webhook'
    return jsonify({
        "message": "Webhook Testing Service",
        "webhook_url": webhook_url,
        "instructions": "Send POST requests to the webhook_url to test",
        "view_logs": request.url_root + 'logs'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request_data = {
        'timestamp': timestamp,
        'headers': dict(request.headers),
        'data': request.get_data(as_text=True),
        'remote_addr': request.remote_addr
    }
    
    # Log the webhook
    logger.info(f"New webhook received at {timestamp}")
    logger.info(f"Headers: {request_data['headers']}")
    logger.info(f"Data: {request_data['data']}")
    
    # Store in history
    webhook_history.append(request_data)
    if len(webhook_history) > 10:  # Keep only last 10 requests
        webhook_history.pop(0)
    
    return jsonify({
        "message": "Webhook received successfully",
        "timestamp": timestamp,
        "request_info": request_data
    })

@app.route('/logs')
def view_logs():
    return jsonify({
        "message": "Recent webhook history",
        "count": len(webhook_history),
        "webhooks": webhook_history
    })

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
