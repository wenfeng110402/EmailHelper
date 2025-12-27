# Personal Email Background

This is a small email tool.

- `mail_manager.py` runs a simple web page.
- `email-designer.html` is the editor UI.

## What you need

- Python 3
- Flask

## Install

If you want, make a venv first.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
python mail_manager.py
```

Open:

- http://127.0.0.1:5000/

## SMTP (for sending)

Set these env vars:

- `SMTP_HOST`
- `SMTP_PORT` (587 or 465)
- `SMTP_USER`
- `SMTP_PASS`
- `SMTP_FROM` (optional)

Then fill the "to" and "subject" in the page and click send.
