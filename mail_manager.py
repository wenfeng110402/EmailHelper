from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=str(Path(__file__).parent))
BASE_DIR = Path(__file__).parent
EMAIL_FILE = BASE_DIR / "email-template.html"
DESIGNER_FILE = BASE_DIR / "email-designer.html"


def load_email_html() -> str:
    if not EMAIL_FILE.exists():
        return ""
    return EMAIL_FILE.read_text(encoding="utf-8")


def save_email_html(html: str) -> None:
    EMAIL_FILE.write_text(html, encoding="utf-8")


def build_message(to_address: str, subject: str, html: str) -> EmailMessage:
    msg = EmailMessage()
    from_address = os.getenv("SMTP_FROM", os.getenv("SMTP_USER", ""))
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content("This email requires an HTML-capable client.")
    msg.add_alternative(html, subtype="html")
    return msg


@app.route("/")
def serve_designer():
    return send_from_directory(BASE_DIR, DESIGNER_FILE.name)


@app.route("/api/email", methods=["GET", "POST"])
def email_template():
    if request.method == "GET":
        return jsonify({"html": load_email_html()})

    data = request.get_json(force=True, silent=True) or {}
    html = data.get("html", "")
    save_email_html(html)
    return jsonify({"status": "saved"})


@app.route("/api/send", methods=["POST"])
def send_email():
    data = request.get_json(force=True, silent=True) or {}
    to_address = data.get("to") or ""
    subject = data.get("subject") or "Untitled"
    html = data.get("html") or load_email_html()

    if not to_address:
        return jsonify({"error": "Missing recipient"}), 400

    msg = build_message(to_address, subject, html)

    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASS", "")

    try:
        if port == 465:
            with smtplib.SMTP_SSL(host, port) as server:
                if username:
                    server.login(username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                if username:
                    server.login(username, password)
                server.send_message(msg)
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500

    return jsonify({"status": "sent"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
