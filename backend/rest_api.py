# Basic Flask REST API
from flask import Flask, jsonify, request, abort
from make_rag_request import make_request, close as close_weaviate
from get_sentiment import get_sentiment
from flask_cors import CORS
# Allow CORS

app = Flask(__name__)
CORS(app)

# Generating sample tweets and sentiment
@app.route('/tweet_data/<string:topic>', methods=['GET'])
def get_items(topic):
    sample_tweets = make_request(topic)
    sentiment = get_sentiment(topic)
    return jsonify({"tweets": make_request(topic), "sentiment": sentiment})

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

# Error handler for 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
