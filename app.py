import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"

# Load dictionary words from the forked local repo folder or loaded file
# For demo, assuming a plain text dictionary file with one word per line
# You can customize this to JSON, CSV, etc. by adjusting the loader

def load_dictionary():
    dict_path = "dictionary.txt"  # This should be placed or updated with dictionary data
    if not os.path.isfile(dict_path):
        return set()
    with open(dict_path, "r", encoding="utf-8") as f:
        words = set(w.strip().lower() for w in f.readlines())
    return words

DICTIONARY_WORDS = load_dictionary()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    subject = data.get('subject', 'General')
    keys = data.get('keys', [])
    questions = []

    # If no API keys, fallback to predefined questions or dictionary-based questions
    if not keys:
        # For simpler fallback, generate dummy questions by sampling from dictionary
        if DICTIONARY_WORDS:
            words = list(DICTIONARY_WORDS)[:50]
            questions = [f"Sample question about '{word.capitalize()}' in {subject}" for word in words]
        else:
            questions = ["Please provide at least one Gemini API key to generate questions."]
        return jsonify(questions)

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

    if not questions:
        questions = ["Error generating questions from Gemini API."]
    return jsonify(questions)

if __name__ == "__main__":
    app.run(debug=True)
