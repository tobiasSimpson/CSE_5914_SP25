# Basic Flask REST API
from flask import Flask, jsonify, request, abort
from get_tweets_and_sentiment import make_request, close as close_weaviate
from flask_cors import CORS
# Allow CORS

app = Flask(__name__)
CORS(app)

# Generating sample tweets and sentiment
@app.route('/tweet_data/<string:topic>', methods=['GET'])
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
    app.run(debug=True, host="0.0.0.0")

# Close the Weaviate client when the app is stopped
@app.teardown_appcontext
def teardown_appcontext(exception):
    print("Closing the Weaviate client...")
    close_weaviate()
    if exception:
        print(f"An error occurred: {exception}")
    else:
        print("App stopped without errors.")
