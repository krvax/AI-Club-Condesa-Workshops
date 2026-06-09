from flask import Flask, render_template, request, send_from_directory
import datetime
import os

app = Flask(__name__)

import json

# ── Load Site Data from JSON ─────────────────────────────────────────
try:
    with open(os.path.join(os.path.dirname(__file__), "site_data.json"), "r", encoding="utf-8") as f:
        SITE_DATA = json.load(f)
except Exception as e:
    print(f"Error loading site_data.json: {e}")
    SITE_DATA = {"en": {}, "es": {}}

# ── Rutas ───────────────────────────────────────────────────────────
@app.route("/")
def home():
    # Detect language from query parameter, default to "en"
    lang = request.args.get("lang", "en")
    if lang not in ["en", "es"]:
        lang = "en"
        
    data = SITE_DATA[lang]
    return render_template(
        "index.html", 
        lang=lang,
        ui=data["ui"],
        profile=data["profile"],
        projects=data["projects"],
        skills=data["skills"],
        datetime=datetime
    )

@app.route("/download-cv")
def download_cv():
    # Since the PDF is already in English, we just serve the existing file.
    # If a Spanish version is added later, we can use the 'lang' parameter to serve different files.
    filename = "CV-Miguel-Carvajal.pdf"
    assets_dir = os.path.join(app.root_path, 'static', 'assets')
    return send_from_directory(assets_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
