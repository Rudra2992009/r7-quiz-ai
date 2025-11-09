import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load dictionary words
# Assumes dictionary.txt exists with one word per line

def load_dictionary():
    dict_path = "dictionary.txt"
    if not os.path.isfile(dict_path):
        logging.warning(f"Dictionary file {dict_path} not found.")
        return set()
    with open(dict_path, "r", encoding="utf-8") as f:
        words = set(w.strip().lower() for w in f.readlines())
    logging.info(f"Loaded {len(words)} words from dictionary.")
    return words

DICTIONARY_WORDS = load_dictionary()

# Simple in-memory cache to reduce API calls
cached_questions = {}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    subject = data.get('subject', 'General').strip()
    keys = [k.strip() for k in data.get('keys', []) if k.strip()]
    questions = []

    if not subject:
        return jsonify(["Subject cannot be empty."]), 400

    # Use cache key based on subject + keys count
    cache_key = (subject, len(keys))

    if cache_key in cached_questions:
        logging.info(f"Serving cached questions for {subject}")
        return jsonify(cached_questions[cache_key])

    # Fallback scenario if no keys provided
    if not keys:
        if DICTIONARY_WORDS:
            words = list(DICTIONARY_WORDS)[:50]
            questions = [f"Sample question about '{word.capitalize()}' in {subject}" for word in words]
        else:
            questions = ["Please provide at least one Gemini API key to generate questions."]
        cached_questions[cache_key] = questions
        return jsonify(questions)

    # Iterate over keys and try generating with first valid
    for key in keys:
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Generate 50 tough CBSE board style questions for subject: {subject}"}]
            }]
        }
        try:
            resp = requests.post(f"{GEMINI_URL}?key={key}", json=payload, headers=headers, timeout=20)
            if resp.ok:
                res = resp.json()
                texts = []
                candidates = res.get('candidates', [])
                for cand in candidates:
                    content = cand.get('content', {})
                    parts = content.get('parts', [])
                    for part in parts:
                        text = part.get('text','').strip()
                        if text:
                            texts.append(text)
                if texts:
                    questions = texts[:50]
                    cached_questions[cache_key] = questions
                    logging.info(f"Generated questions from Gemini API for {subject}")
                    break
        except Exception as e:
            logging.error(f"Error calling Gemini API with key: {e}")
            continue

    if not questions:
        questions = ["Error generating questions from Gemini API."]
        cached_questions[cache_key] = questions

    return jsonify(questions)

# Extendability placeholders
# TODO: Add routes and handlers for pre-made question sets for 10th and 12th here

if __name__ == "__main__":
    app.run(debug=True)
