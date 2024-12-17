from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/webhook', methods=['POST'])
def webhook():
    if True:
        data = request.get_json()
        return jsonify({
            "message": "Webhook received",
            "data": data
        }), 200
    return jsonify({"error": "Request must be JSON"}), 400



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
