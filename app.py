from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import json
import uuid

app = Flask(__name__)
CORS(app)

# Define the Limiter with a key function
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Load or initialize the page visit counts
def load_visit_counts():
    try:
        with open('analytics.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

page_visit_counts = load_visit_counts()

@app.route('/track', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
def track_page_view():
    data = request.get_json()
    path = data['path']
    visitor_id = request.cookies.get('visitor_id')

    if not visitor_id:
        # New visitor - assign a unique ID
        visitor_id = str(uuid.uuid4())
        response = make_response(jsonify({"message": "New visitor logged"}))
        response.set_cookie('visitor_id', visitor_id, max_age=60*60*24*365*2)  # Expires in two years
    else:
        response = make_response(jsonify({"message": "Return visitor logged"}))

    # Increment visit count
    if path not in page_visit_counts:
        page_visit_counts[path] = 1
    else:
        page_visit_counts[path] += 1

    # Save to file
    try:
        with open('analytics.json', 'w') as file:
            json.dump(page_visit_counts, file)
    except Exception as e:
        app.logger.error(f"Failed to write to file: {e}")

    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
