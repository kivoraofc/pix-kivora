import os
from flask import Flask, request, jsonify, send_from_directory
import requests

# Configuração fixa da PushinPay
PUSHINPAY_TOKEN = os.getenv("PUSHINPAY_TOKEN", "43868|KDTirIabgqJOrQHPEeUzkja97Mx18xhlMf8JrQDnb8a5822a")
PUSHINPAY_BASE = os.getenv("PUSHINPAY_BASE", "https://api.pushinpay.com.br")
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

def auth_headers():
    if not PUSHINPAY_TOKEN:
        return None
    return {
        "authorization": f"Bearer {PUSHINPAY_TOKEN}",
        "accept": "application/json",
        "content-type": "application/json",
    }

@app.post("/api/pix")
def gerar_pix():
    headers = auth_headers()
    if headers is None:
        return jsonify({"error": "PUSHINPAY_TOKEN não configurado"}), 500

    data = request.get_json(silent=True) or {}
    value_raw = data.get("value") or data.get("amountBRL")
    try:
        value_num = float(str(value_raw).replace(",", "."))
    except Exception:
        value_num = None
    if value_num is None or value_num <= 0:
        return jsonify({"error": "amountBRL obrigatório"}), 400  # mantém a msg que você viu

    webhook_url = data.get("webhook_url")
    split_rules = data.get("split_rules", [])

    # PushinPay pede amountBRL
    payload = {
        "amountBRL": round(value_num, 2),
        "split_rules": split_rules
    }
    if webhook_url:
        payload["webhook_url"] = webhook_url

    try:
        r = requests.post(f"{PUSHINPAY_BASE}/api/pix/cashIn", json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        return jsonify({"error": "falha ao contatar PushinPay", "detail": str(e)}), 502

    try:
        resp = r.json()
    except ValueError:
        resp = {"error": "resposta inválida da PushinPay", "raw": r.text}
    return jsonify(resp), r.status_code


@app.get("/api/status")
def status():
    headers = auth_headers()
    if headers is None:
        return jsonify({"error": "PUSHINPAY_TOKEN não configurado"}), 500

    tx_id = request.args.get("id")
    if not tx_id:
        return jsonify({"error": "id obrigatório"}), 400

    try:
        r = requests.get(f"{PUSHINPAY_BASE}/api/transactions/{tx_id}", headers=headers, timeout=30)
    except requests.RequestException as e:
        return jsonify({"error": "falha ao contatar PushinPay", "detail": str(e)}), 502

    try:
        resp = r.json()
    except ValueError:
        resp = {"error": "resposta inválida da PushinPay", "raw": r.text}
    return jsonify(resp), r.status_code

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
# This code is part of a Flask application that interacts with the PushinPay API to generate PIX transactions and check their status.
# It includes endpoints for creating a PIX transaction and checking the status of a transaction by its ID.
# The application serves static files from a public directory and handles errors gracefully.    