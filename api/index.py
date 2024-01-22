from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

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

@app.route('/get_labels', methods=['GET'])
def get_labels():
    api_key = 'AIzaSyBoE_mDhkMHdUgwvpoK3RcKbAPAsOu9Muk'
    blog_id = '6331170148874248090'
    post_url = request.args.get('url')

    labels = extract_post_labels(api_key, blog_id, post_url)

    if labels is not None:
        response = jsonify({'post_labels': labels})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        return jsonify({'error': 'Failed to retrieve labels'}), 500

if __name__ == '__main__':
    app.run(debug=True)
