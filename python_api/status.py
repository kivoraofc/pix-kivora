import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PUSHINPAY_BASE = os.environ.get('PUSHINPAY_BASE')
PUSHINPAY_TOKEN = os.environ.get('PUSHINPAY_TOKEN')

@app.route('/api/status', methods=['GET'])
def status():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'id obrigatório'}), 400
    headers = {
        'authorization': f'Bearer {PUSHINPAY_TOKEN}',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    r = requests.get(f'{PUSHINPAY_BASE}/api/transactions/{id}', headers=headers)
    try:
        resp = r.json()
    except Exception:
        resp = None
    return (jsonify(resp), 200) if r.ok else (jsonify(resp), r.status_code)

if __name__ == '__main__':
    app.run(debug=True)
