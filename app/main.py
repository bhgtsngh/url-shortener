# app/main.py
from flask import Flask, request, jsonify, redirect
from app.storage import store
from app.services import generate_short_code, is_valid_url

app = Flask(__name__)



@app.route('/')
def root_health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})



@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    url = data.get('url')
    if not url or not is_valid_url(url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = generate_short_code()
    while store.get_url(short_code):  # ensure uniqueness
        short_code = generate_short_code()

    store.save(short_code, url)
    return jsonify({
        'short_code': short_code,
        'short_url': f"http://localhost:5000/{short_code}"
    })

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url = store.get_url(short_code)
    if not url:
        return jsonify({'error': 'Short code not found'}), 404

    store.increment_click(short_code)
    return redirect(url, code=302)

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    stats = store.get_stats(short_code)
    url = store.get_url(short_code)
    if not stats or not url:
        return jsonify({'error': 'Short code not found'}), 404

    return jsonify({
        'url': url,
        'clicks': stats['clicks'],
        'created_at': stats['created_at'].isoformat()
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
