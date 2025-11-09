# r7-quiz-ai

**r7-quiz-ai** is an AI-powered web app to generate 50 CBSE-style tough questions for any selected subject and class (9–12). It uses HTML5, CSS, JS (frontend), Python backend and communicates via JS to generate questions using Gemini 2.5 Flash Lite API (users bring their own keys; at least one required). Fast deployment supported with GitHub workflows for Python and Jekyll integration.

## Features

- Enter subject, Gemini API keys, and generate instant CBSE board-level questions
- Download quiz as .doc file in one click
- Beautiful UI, HTML5/CSS/JS powered
- Python Flask backend for Gemini API communication
- Gemini 2.5 Flash Lite model for toughest question generation
- Supports 3 user-provided Gemini API keys for max reliability
- Real-time generation, no API key storage, privacy-respecting
- Easy GitHub/Jekyll deployment: fast build, static site ready

## Quick Start

1. **Clone** the repo and run the backend:
    ```bash
    git clone https://github.com/Rudra2992009/r7-quiz-ai.git
    cd r7-quiz-ai
    pip install flask requests
    python app.py
    ```
2. **Visit** `http://localhost:5000` in your browser
3. Enter subject, API keys, and generate questions!

## Deployment

- Fork or clone into your GitHub account
- Auto-deployment supported with Python build workflows & Jekyll for static frontend hosting
- Full instructions provided in repo

---
AI-powered. Gemini 2.5 Flash Lite engine. Save, print, deploy anywhere. Built for CBSE board exam practice. <br>
[Live project on GitHub](https://github.com/Rudra2992009/r7-quiz-ai)
