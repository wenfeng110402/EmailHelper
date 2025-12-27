import os
import smtplib
from email.message import EmailMessage

from flask import Flask, jsonify, request, send_from_directory

# 尽量简单的写法，少封装，方便看懂和改。
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMAIL_FILE = os.path.join(BASE_DIR, "email-template.html")
DESIGNER_FILE = os.path.join(BASE_DIR, "email-designer.html")


def load_email_html():
    if not os.path.exists(EMAIL_FILE):
        return ""
    with open(EMAIL_FILE, "r", encoding="utf-8") as f:
        return f.read()


def save_email_html(html):
    with open(EMAIL_FILE, "w", encoding="utf-8") as f:
        f.write(html)


def build_message(to_address, subject, html):
    msg = EmailMessage()
    from_address = os.getenv("SMTP_FROM") or os.getenv("SMTP_USER") or ""
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content("This email requires an HTML-capable client.")
    msg.add_alternative(html, subtype="html")
    return msg


@app.route("/")
def serve_designer():
    # 直接返回可视化编辑器页面
    return send_from_directory(BASE_DIR, os.path.basename(DESIGNER_FILE))


@app.route("/api/email", methods=["GET", "POST"])
def email_template():
    if request.method == "GET":
        return jsonify({"html": load_email_html()})

    # 简单处理：获取 body 里的 html 字段并保存
    data = request.get_json(silent=True) or {}
    html = data.get("html", "")
    save_email_html(html)
    return jsonify({"status": "saved"})


@app.route("/api/send", methods=["POST"])
def send_email():
    data = request.get_json(silent=True) or {}
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
            server = smtplib.SMTP_SSL(host, port)
        else:
            server = smtplib.SMTP(host, port)
            server.starttls()

        if username:
            server.login(username, password)

        server.send_message(msg)
        server.quit()
    except Exception as exc:
        # 初学者常见的直接返回错误字符串
        return jsonify({"error": str(exc)}), 500

    return jsonify({"status": "sent"})


if __name__ == "__main__":
    # 用最基本的方式启动，开启 debug 便于调试
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
