import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    subject = data.get('subject', 'General')
    keys = data.get('keys', [])
    questions = []
    if not keys: return jsonify(["At least one Gemini API key required."])
    # Use first working key and Gemini model
    for key in keys:
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Generate 50 tough CBSE board style questions for subject: {subject}"}]
            }]
        }
        try:
            r = requests.post(f"{GEMINI_URL}?key={key}", json=payload, headers=headers, timeout=20)
            if r.ok:
                res = r.json()
                texts = []
                if 'candidates' in res:
                    for cand in res['candidates']:
                        if 'content' in cand and 'parts' in cand['content']:
                            for part in cand['content']['parts']:
                                t = part.get('text','').strip()
                                if t: texts.append(t)
                    questions = texts[:50]
                break # Use first valid key
        except Exception as e:
            continue
    if not questions: questions = ["Error generating questions from Gemini API."]
    return jsonify(questions)

if __name__ == "__main__":
    app.run(debug=True)
