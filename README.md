# SafeHer — Women Safety Support System (Student SPI Project)

A small full-stack demonstration project built with FastAPI, HTML, CSS, and JavaScript.

## Features
- Demo SOS alert recording
- Optional browser geolocation capture
- Safety check-in form
- Incident report form with category, description, and optional location
- Alert history for the current server session
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
This is an educational demo, not a real emergency-response service. It does not send SMS, make calls, or notify police or trusted contacts. Activity is stored in memory and is cleared when the server restarts. Browser geolocation generally requires user permission and a secure context (localhost is supported for development).


## CSS troubleshooting

- Keep `index.html`, `style.css`, and `app.js` inside the `static/` folder.
- The HTML loads the stylesheet from `/static/style.css?v=2` so browsers refresh a cached stylesheet.
- Run the app from the project folder with `uvicorn main:app --reload`, then open `http://127.0.0.1:8000` (do not open `index.html` directly as a `file://` URL).
- If styling still looks old, hard-refresh the page with `Ctrl+F5` or `Cmd+Shift+R`.
