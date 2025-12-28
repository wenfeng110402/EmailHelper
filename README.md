# Personal Email Background

A simple email template editor and sender with visual editing capabilities.

## Features

- Visual HTML email editor with drag-and-drop images
- Live preview with full HTML rendering
- SMTP configuration and email sending
- Multiple template management
- Bilingual interface (Chinese/English)

## Requirements

- Python 3.7+
- Flask

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:

```bash
python mail_manager.py
```

Open in your browser:

- http://127.0.0.1:5000/

## SMTP Configuration

You can configure SMTP settings directly in the web interface. Your SMTP credentials will be saved locally in `smtp.json`.

**Important**: The `smtp.json` file contains sensitive information (your SMTP password). Never commit or share this file publicly.

### Common SMTP Settings

**iCloud Mail:**
- Host: `smtp.mail.me.com`
- Port: `587`
- Use your Apple ID email and an [App-Specific Password](https://support.apple.com/en-us/HT204397)

**Outlook/Hotmail:**
- Host: `smtp-mail.outlook.com`
- Port: `587`
- Use your Outlook email and password

**Gmail:**
- Host: `smtp.gmail.com`
- Port: `587`
- Use your Gmail address and an [App Password](https://support.google.com/accounts/answer/185833)

Alternatively, you can set environment variables (same terminal session):

- `SMTP_HOST`
- `SMTP_PORT` (587 or 465)
- `SMTP_USER`
- `SMTP_PASS`
- `SMTP_FROM` (optional)

## Deployment

### GitHub Codespaces

1. Fork this repository
2. Click "Code" → "Codespaces" → "Create codespace on main"
3. Wait for the environment to initialize
4. Run `python mail_manager.py` in the terminal
5. Open the forwarded port in your browser

### Local Deployment

Simply clone the repository and follow the installation steps above.

## Security Notice

- SMTP passwords are stored locally in `smtp.json`
- Keep your `smtp.json` file private (it's already in `.gitignore`)
- Use app-specific passwords when available instead of your main account password

## Files

- `mail_manager.py` - Flask backend server
- `email-designer.html` - Visual editor interface (Chinese, for local use)
- `index.html` - Static preview page (English, for GitHub Pages)
- `email-template.html` - Sample email template
