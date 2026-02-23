import os
import sys
from flask import Flask, request, jsonify, send_from_directory
import requests

# Adiciona o diretório python_api ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_api'))

# Caminho absoluto para a pasta public
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'public'))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

PUSHINPAY_BASE = "https://api.pushinpay.com.br"
PUSHINPAY_TOKEN = "62784|0VAlLudbixBdW5yjv5xijXrvxRztVrDg15y8bxo7a70ca885"

# Endpoint /api/pix
@app.route('/api/pix', methods=['POST'])
def pix():
    data = request.get_json() or {}
    amountBRL = data.get('amountBRL')
    webhookUrl = data.get('webhookUrl')
    if not amountBRL:
        return jsonify({'error': 'amountBRL obrigatório'}), 400
    try:
        value = round(float(amountBRL) * 100)
    except Exception:
        return jsonify({'error': 'valor inválido'}), 400
    if not isinstance(value, (int, float)) or value < 50:
        return jsonify({'error': 'valor mínimo R$0,50'}), 400
    headers = {
        'authorization': f'Bearer {PUSHINPAY_TOKEN}',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    payload = {
        'value': value,
        'webhook_url': webhookUrl,
        'split_rules': []
    }
    r = requests.post(f'{PUSHINPAY_BASE}/api/pix/cashIn', headers=headers, json=payload)
    try:
        resp = r.json()
    except Exception:
        resp = None
    if not r.ok:
        return jsonify({'error': 'pushinpay_error', 'detail': resp}), r.status_code
    return jsonify({
        'id': resp.get('id'),
        'status': resp.get('status'),
        'emv': resp.get('qr_code'),
        'pngBase64': resp.get('qr_code_base64')
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
