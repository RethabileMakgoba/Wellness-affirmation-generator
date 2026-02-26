from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

affirmations_db = []

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "message": "AI Wellness Affirmation API is running",
        "version": "2.0.0 - FREE AI Edition!",
        "ai_enabled": bool(GROQ_API_KEY)
    })

@app.route('/api/generate-affirmation', methods=['POST'])
def generate_affirmation():
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "No data provided"}), 400

        mood = data.get('mood', '').strip()
        situation = data.get('situation', '').strip()
        if not mood: return jsonify({"error": "Mood is required"}), 400

        if GROQ_API_KEY:
            affirmation = generate_ai_affirmation(mood, situation)
        else:
            affirmation = generate_simple_affirmation(mood, situation)
            affirmation += " [Add GROQ_API_KEY to .env for AI-powered affirmations]"

        entry = {
            "id": len(affirmations_db) + 1,
            "mood": mood,
            "situation": situation,
            "affirmation": affirmation,
            "timestamp": datetime.now().isoformat(),
            "ai_generated": bool(GROQ_API_KEY)
        }
        affirmations_db.append(entry)

        return jsonify({
            "success": True,
            "affirmation": affirmation,
            "mood": mood,
            "id": entry["id"],
            "ai_generated": entry["ai_generated"]
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/affirmations', methods=['GET'])
def get_affirmations():
    return jsonify({
        "success": True,
        "count": len(affirmations_db),
        "affirmations": affirmations_db
    })

def generate_ai_affirmation(mood, situation):
    try:
        prompt = f"""You are a compassionate mental wellness coach creating personalized affirmations.

A person is currently feeling: {mood}
{f'Their situation: {situation}' if situation else ''}

Create a 2-3 sentence, first-person, positive, empowering affirmation."""
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system","content": "You are a compassionate mental wellness coach."},
                         {"role": "user","content": prompt}],
            "temperature": 0.8,
            "max_tokens": 150
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"AI generation error: {e}")
        return generate_simple_affirmation(mood, situation)

def generate_simple_affirmation(mood, situation):
    affirmations = {
        "anxious": "I am calm and centered. I trust in my ability to handle whatever comes my way.",
        "stressed": "I release tension with each breath. I am capable and resilient.",
        "sad": "I am worthy of love and happiness. This feeling will pass.",
        "overwhelmed": "I take things one step at a time. I am doing my best.",
        "uncertain": "I trust the journey. I am exactly where I need to be.",
        "excited": "I embrace this positive energy. I am open to possibilities.",
        "grateful": "I appreciate this moment and all the blessings in my life.",
        "confident": "I believe in myself and my abilities. I am capable of great things."
    }
    base = affirmations.get(mood.lower(), "I am enough. I am worthy. I am capable.")
    if situation: return f"{base} {situation.capitalize()} is an opportunity for growth."
    return base

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
