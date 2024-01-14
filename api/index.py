import os
from flask import Flask, request, jsonify
import re
import json
import requests
from flask_cors import CORS

app = Flask(__name__)

# Get the port number from the PORT environment variable, or use a default value (5000)
port = int(os.environ.get("PORT", 5000))

# Configure CORS to allow requests from multiple websites
CORS(app, resources={
    r"/get_post_id": {
        "origins": ["https://www.boobstube.xyz", "https://www.hotnippy.com"]
    }
})

@app.route('/get_post_id', methods=['POST'])
def get_post_id():
    api_key = 'AIzaSyBoE_mDhkMHdUgwvpoK3RcKbAPAsOu9Muk'
    blog_id = '6331170148874248090'

    # Get post_url from the request JSON data
    post_url = request.json.get('post_url')

    post_id = extract_post_id(api_key, blog_id, post_url)

    if post_id:
        return jsonify({'post_id': post_id})
    else:
        return jsonify({'error': 'Failed to retrieve post ID'}), 500


    except Exception as e:
        return jsonify({"error": str(e)}), 500
