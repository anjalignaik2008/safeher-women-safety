# SafeHer — Women Safety Support System (Student SPI Project)

A small full-stack demonstration project built with FastAPI, HTML, CSS, and JavaScript.

## Features
- Demo SOS alert recording
- Optional browser geolocation capture
- Safety check-in form
- Incident report form with category, description, and optional location
- Owner and trusted-contact accounts with separate logins
- One-time trusted-contact invite codes that expire after 24 hours
- Shared, read-only alert history for trusted contacts across devices
- Persistent activity storage (SQLite locally, PostgreSQL on Render)
- Responsive layout for desktop and mobile screens

## Requirements
- Python 3.10 or newer
- pip

## Run on Windows
1. Extract the ZIP file.
2. Open Command Prompt or the VS Code terminal in the extracted `women_safety_spi_project` folder.
3. (Recommended) Create and activate a virtual environment:
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bat
   pip install -r requirements.txt
   ```
5. Start the server:
   ```bat
   uvicorn main:app --reload
   ```
6. Open http://127.0.0.1:8000 in your browser.

## Accounts and trusted contacts

1. Create an owner account with an email address and a password of at least 12 characters.
2. From the owner account, create a trusted-contact invite code and share it privately. The code can be used once and expires after 24 hours.
3. On the trusted contact's device, choose **Join as contact**, enter the code, and create a separate account.
4. The owner and trusted contact can sign in independently from multiple devices. Contacts can view the owner's activity but cannot create or change alerts.

Local accounts and history are stored in `safeher.db` in the project directory. Do not delete or share this file if you need to retain the local data.

## Render deployment

The root `render.yaml` defines the FastAPI web service, a managed PostgreSQL database, and a generated `APP_SECRET` for signed sessions. Push the repository to GitHub, then in Render choose **New + → Blueprint** and select this repository. Once deployed, open the service URL and create an owner account.

Render provisions resources described by the Blueprint; check the plan and pricing shown in your Render workspace before confirming.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000.

## Folder structure
```text
women_safety_spi_project/
├── main.py
├── requirements.txt
├── README.md
├── PROJECT_ABSTRACT.txt
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## Important limitations
This is an educational demo, not a real emergency-response service. It does not send SMS, make calls, or notify police or trusted contacts. Contact access is limited to viewing activity in the app; there are no push notifications, email verification, or password-recovery flow. Use a unique password and share invite codes only with the intended contact. Browser geolocation generally requires user permission and a secure context (localhost is supported for development).


## CSS troubleshooting

- Keep `index.html`, `style.css`, and `app.js` inside the `static/` folder.
- The HTML loads the stylesheet from `/static/style.css?v=2` so browsers refresh a cached stylesheet.
- Run the app from the project folder with `uvicorn main:app --reload`, then open `http://127.0.0.1:8000` (do not open `index.html` directly as a `file://` URL).
- If styling still looks old, hard-refresh the page with `Ctrl+F5` or `Cmd+Shift+R`.
