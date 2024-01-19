from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

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

def get_random_posts(api_key, blog_id, labels_to_fetch):
    url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?key={api_key}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            all_posts = response.json().get('items', [])
            
            # Filter posts based on labels
            filtered_posts = [post for post in all_posts if any(label.lower() in [l.lower() for l in post.get('labels', [])] for label in labels_to_fetch)]
            
            # Shuffle the filtered posts randomly
            random.shuffle(filtered_posts)
            
            # Return a subset of shuffled posts (adjust as needed)
            num_posts_to_return = 5
            return filtered_posts[:num_posts_to_return]
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/get_labels', methods=['GET'])
def get_labels():
    api_key = request.args.get('api_key')
    blog_id = request.args.get('blog_id')
    post_url = request.args.get('post_url')

    labels = extract_post_labels(api_key, blog_id, post_url)

    if labels is not None:
        response = jsonify({'post_labels': labels})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        return jsonify({'error': 'Failed to retrieve labels'}), 500

@app.route('/get_random_posts', methods=['GET'])
def get_random_posts_route():
    api_key = request.args.get('api_key')
    blog_id = request.args.get('blog_id')
    labels_to_fetch = request.args.getlist('labels_to_fetch')

    posts = get_random_posts(api_key, blog_id, labels_to_fetch)

    if posts is not None:
        response = jsonify({'random_posts': posts})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        return jsonify({'error': 'Failed to retrieve random posts'}), 500

if __name__ == '__main__':
    app.run(debug=True)
