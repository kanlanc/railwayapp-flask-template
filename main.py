from flask import Flask, request, jsonify
from datetime import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return "Webhook URL: <your-domain>/webhook"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get form data
        parsed_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'email_details': {
                'from': request.form.get('from'),
                'to': request.form.get('To'),
                'subject': request.form.get('subject'),
                'body_plain': request.form.get('body-plain'),
                'body_html': request.form.get('body-html'),
                'stripped_text': request.form.get('stripped-text')
            },
            'attachments': {
                'count': request.form.get('attachment-count'),
                'files': [f'attachment-{i}' for i in range(1, int(request.form.get('attachment-count', 0)) + 1)]
            },
            'headers': dict(request.headers),
            'additional_variables': {
                'message_headers': request.form.get('message-headers'),
                'content_id_map': request.form.get('content-id-map'),
                'recipient': request.form.get('recipient')
            }
        }

        # Log the parsed data
        logger.info("Webhook received:")
        logger.info(f"From: {parsed_data['email_details']['from']}")
        logger.info(f"Subject: {parsed_data['email_details']['subject']}")
        logger.info(f"Attachments: {parsed_data['attachments']['count']}")

        return jsonify({
            "status": "success",
            "message": "Webhook received",
            "parsed_data": parsed_data
        })

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
