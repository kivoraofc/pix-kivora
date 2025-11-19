
import os
from flask import Flask, request, jsonify, send_from_directory
import requests

# Caminho absoluto para a pasta public
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'public'))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

PUSHINPAY_BASE = "https://api.pushinpay.com.br"
PUSHINPAY_TOKEN = "43868|KDTirIabgqJOrQHPEeUzkja97Mx18xhlMf8JrQDnb8a5822a"

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

# Endpoint /api/status
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


# Servir index.html na raiz e arquivos estáticos
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)

#Porta dinâmica no final do pix.py:
#Comando de start no Railway: gunicorn pix:app
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))