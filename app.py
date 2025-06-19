from flask import Flask, jsonify
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/stream")
def get_stream_url():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        page = requests.get("https://tvlibreonline.org/en-vivo/tyc-sports/", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        iframe = soup.find("iframe")
        if iframe and "src" in iframe.attrs:
            iframe_src = "https://tvlibreonline.org" + iframe["src"]
            inner_page = requests.get(iframe_src, headers=headers)
            m3u8_match = re.search(r'https://[^"]+\.m3u8', inner_page.text)
            if m3u8_match:
                return jsonify({"url": m3u8_match.group()})
        return jsonify({"error": "No se encontró el stream"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def root():
    return "Servidor de Stream funcionando"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
