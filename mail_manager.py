import os
import json
import smtplib
from email.message import EmailMessage

from flask import Flask, jsonify, request, send_from_directory

# 尽量简单的写法，少封装，方便看懂和改。
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMAIL_FILE = os.path.join(BASE_DIR, "email-template.html")
DESIGNER_FILE = os.path.join(BASE_DIR, "email-designer.html")
SMTP_FILE = os.path.join(BASE_DIR, "smtp.json")


def is_safe_html_name(name):
    # 很简单的文件名校验：只允许当前目录下的 .html 文件
    if not name:
        return False
    if "/" in name or "\\" in name:
        return False
    if name.startswith("."):
        return False
    return name.lower().endswith(".html")


def list_html_templates():
    # 列出当前目录下的 html 文件（排除设计器本身）
    items = []
    for fn in os.listdir(BASE_DIR):
        if not fn.lower().endswith(".html"):
            continue
        if fn.lower() in ["email-designer.html"]:
            continue
        items.append(fn)
    items.sort()
    return items


def load_html_file(name):
    if not is_safe_html_name(name):
        return ""
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_html_file(name, html):
    if not is_safe_html_name(name):
        return False
    path = os.path.join(BASE_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def load_smtp_config():
    # 环境变量优先；没有的话再读 smtp.json
    cfg = {
        "host": os.getenv("SMTP_HOST") or "",
        "port": os.getenv("SMTP_PORT") or "",
        "user": os.getenv("SMTP_USER") or "",
        "pass": os.getenv("SMTP_PASS") or "",
        "from": os.getenv("SMTP_FROM") or "",
    }

    if os.path.exists(SMTP_FILE):
        try:
            with open(SMTP_FILE, "r", encoding="utf-8") as f:
                file_cfg = json.load(f)
            if not cfg["host"]:
                cfg["host"] = str(file_cfg.get("host", ""))
            if not cfg["port"]:
                cfg["port"] = str(file_cfg.get("port", ""))
            if not cfg["user"]:
                cfg["user"] = str(file_cfg.get("user", ""))
            if not cfg["pass"]:
                cfg["pass"] = str(file_cfg.get("pass", ""))
            if not cfg["from"]:
                cfg["from"] = str(file_cfg.get("from", ""))
        except Exception:
            pass

    return cfg


def save_smtp_config(new_cfg):
    # 保存到 smtp.json（只是本地文件，别上传 GitHub）
    old = {}
    if os.path.exists(SMTP_FILE):
        try:
            with open(SMTP_FILE, "r", encoding="utf-8") as f:
                old = json.load(f) or {}
        except Exception:
            old = {}

    merged = dict(old)
    for k in ["host", "port", "user", "pass", "from"]:
        if k in new_cfg and str(new_cfg.get(k, "")).strip() != "":
            merged[k] = new_cfg.get(k)

    with open(SMTP_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)


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


@app.route("/api/smtp", methods=["GET", "POST"])
def smtp_config():
    if request.method == "GET":
        cfg = load_smtp_config()
        # 不把密码明文回传到网页（避免无意泄露）
        cfg["pass"] = ""
        return jsonify(cfg)

    data = request.get_json(silent=True) or {}
    save_smtp_config(data)
    return jsonify({"status": "saved"})


@app.route("/api/email", methods=["GET", "POST"])
def email_template():
    if request.method == "GET":
        return jsonify({"html": load_email_html()})

    # 简单处理：获取 body 里的 html 字段并保存
    data = request.get_json(silent=True) or {}
    html = data.get("html", "")
    save_email_html(html)
    return jsonify({"status": "saved"})


@app.route("/api/templates", methods=["GET"])
def templates_list():
    return jsonify({"templates": list_html_templates()})


@app.route("/api/template", methods=["GET", "POST"])
def template_file():
    # 用 name 指定要读/写哪个 html 文件
    if request.method == "GET":
        name = request.args.get("name") or EMAIL_FILE.split(os.sep)[-1]
        if not is_safe_html_name(name):
            return jsonify({"error": "Bad template name"}), 400
        return jsonify({"name": name, "html": load_html_file(name)})

    data = request.get_json(silent=True) or {}
    name = data.get("name") or EMAIL_FILE.split(os.sep)[-1]
    html = data.get("html", "")
    if not is_safe_html_name(name):
        return jsonify({"error": "Bad template name"}), 400
    ok = save_html_file(name, html)
    if not ok:
        return jsonify({"error": "Save failed"}), 500
    return jsonify({"status": "saved", "name": name})


@app.route("/api/send", methods=["POST"])
def send_email():
    data = request.get_json(silent=True) or {}
    to_address = data.get("to") or ""
    subject = data.get("subject") or "Untitled"
    html = data.get("html") or load_email_html()

    if not to_address:
        return jsonify({"error": "Missing recipient"}), 400

    msg = build_message(to_address, subject, html)

    cfg = load_smtp_config()
    host = cfg.get("host", "")
    username = cfg.get("user", "")
    password = cfg.get("pass", "")
    from_address = cfg.get("from", "")
    port_str = str(cfg.get("port", "")).strip() or "587"
    port = int(port_str)

    # 如果网页里填了 from，就用它覆盖邮件 From
    if from_address:
        if "From" in msg:
            # EmailMessage 不允许重复的 From 头
            msg.replace_header("From", from_address)
        else:
            msg["From"] = from_address

    missing = []
    if not host:
        missing.append("SMTP_HOST")
    if not username:
        missing.append("SMTP_USER")
    if not password:
        missing.append("SMTP_PASS")
    if missing:
        return jsonify({
            "error": "Missing SMTP config: " + ", ".join(missing) + ". Set env vars (same terminal) or create smtp.json, then restart mail_manager.py"
        }), 400

    try:
        if port == 465:
            server = smtplib.SMTP_SSL(host, port)
        else:
            server = smtplib.SMTP(host, port)
            server.ehlo()
            server.starttls()
            server.ehlo()

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
