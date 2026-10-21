MINI DARLING BACKEND
===================

Folder contents:
- main.py: FastAPI application
- requirements.txt: Python dependencies
- .env.example: environment variable template

IMPORTANT:
This starter keeps the message queue in RAM. Messages can be lost when the server restarts,
and the queue is not shared across multiple server workers. Use one worker for this version.
The device endpoint requires DEVICE_TOKEN to be configured.

Windows setup:
1. Extract this folder into your project.
2. Open CMD in the MINI_DARLING_BACKEND folder.
3. Run: python -m venv venv
4. Run: venv\Scripts\activate
5. Run: python -m pip install -r requirements.txt
6. Set a secret token in the terminal before starting the server:
   set DEVICE_TOKEN=choose-a-long-random-secret
   set WEBSITE_ORIGIN=https://mini-darling-web.vercel.app
7. Start: python -m uvicorn main:app --host 0.0.0.0 --port 8000

Local test:
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

POST /api/message JSON body:
{"text":"Hi Darling"}

ESP32 polls GET /api/device/next using request header:
X-Device-Token: the same DEVICE_TOKEN value

The online Vercel frontend still needs to call POST /api/message, and the backend must be
deployed to a public HTTPS host before the online site and ESP32 can reach it.
Do not put DEVICE_TOKEN in public frontend JavaScript.
