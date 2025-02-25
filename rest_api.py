# Basic Flask REST API
from flask import Flask, jsonify, request, abort
from make_rag_request import make_request, close as close_weaviate

app = Flask(__name__)

# Generating sample tweets
@app.route('/sample_tweets/<string:topic>', methods=['GET'])
def get_items(topic):
    return jsonify(make_request(topic))

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
    app.run(debug=True)
