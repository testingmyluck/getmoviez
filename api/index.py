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
    r"/get_post_data": {
        "origins": ["https://www.boobstube.xyz", "https://www.hotnippy.com", "https://gettinpostid.vercel.app"]
    }
})


def extract_post_id(api_key, blog_id, post_url):
    post_path = post_url.replace('https://www.hotnippy.com', '')
    url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/bypath?path={post_path}&key={api_key}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            post_data = response.json()
            post_id = post_data.get('id')
            return post_id
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_post_labels(api_key, blog_id, post_url):
    post_path = post_url.replace('https://www.hotnippy.com', '')
    url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/bypath?path={post_path}&key={api_key}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            post_data = response.json()
            post_labels = post_data.get('labels', [])
            return post_labels
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/get_post_data', methods=['POST'])
def get_post_data():
    api_key = 'AIzaSyBoE_mDhkMHdUgwvpoK3RcKbAPAsOu9Muk'
    blog_id = '6331170148874248090'
    
    post_url = request.json.get('post_url')

    post_id = extract_post_id(api_key, blog_id, post_url)
    post_labels = extract_post_labels(api_key, blog_id, post_url)

    if post_id is not None:
        response_data = {
            'post_id': post_id,
            'post_labels': post_labels
        }
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Failed to retrieve post data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
