"""
AI Wellness Affirmation Generator - Backend API with FREE Groq AI
A Flask application that generates personalized wellness affirmations using FREE AI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Groq API configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# In-memory storage
affirmations_db = []

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Wellness Affirmation API is running",
        "version": "2.0.0 - FREE AI Edition!",
        "ai_enabled": bool(GROQ_API_KEY)
    })

@app.route('/api/generate-affirmation', methods=['POST'])
def generate_affirmation():
    """
    Generate a personalized affirmation using FREE Groq AI
    
    Expected JSON body:
    {
        "mood": "anxious",
        "situation": "preparing for job interview"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        mood = data.get('mood', '').strip()
        situation = data.get('situation', '').strip()
        
        if not mood:
            return jsonify({"error": "Mood is required"}), 400
        
        # Generate affirmation using AI
        if GROQ_API_KEY:
            affirmation = generate_ai_affirmation(mood, situation)
        else:
            affirmation = generate_simple_affirmation(mood, situation)
            affirmation += " [Add GROQ_API_KEY to .env for AI-powered affirmations]"
        
        # Store in database
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
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/affirmations', methods=['GET'])
def get_affirmations():
    """Get all stored affirmations"""
    return jsonify({
        "success": True,
        "count": len(affirmations_db),
        "affirmations": affirmations_db
    })

def generate_ai_affirmation(mood, situation):
    """
    Generate personalized affirmation using FREE Groq AI
    This is where the magic happens!
    """
    try:
        # Create a thoughtful prompt
        prompt = f"""You are a compassionate mental wellness coach creating personalized affirmations.

A person is currently feeling: {mood}
{f'Their situation: {situation}' if situation else ''}

Create a powerful, personalized affirmation for them. The affirmation should:
- Be 2-3 sentences maximum
- Use "I" statements (first person)
- Be positive and empowering
- Acknowledge their current feeling while offering hope and strength
- Be specific to their situation if provided
- Sound natural and genuine, not generic

Just provide the affirmation itself, nothing else."""

        # Call Groq API
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",  # Fast and free!
            "messages": [
                {
                    "role": "system",
                    "content": "You are a compassionate mental wellness coach. Provide only the affirmation, no explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.8,
            "max_tokens": 150
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        affirmation = result['choices'][0]['message']['content'].strip()
        
        print(f" AI Generated: {affirmation}")
        return affirmation
        
    except Exception as e:
        print(f"AI generation error: {str(e)}")
        # Fallback to simple affirmation if AI fails
        return generate_simple_affirmation(mood, situation)

def generate_simple_affirmation(mood, situation):
    """
    Fallback: Generate a simple affirmation (used when API key is missing)
    """
    affirmations = {
        "anxious": "I am calm and centered. I trust in my ability to handle whatever comes my way.",
        "stressed": "I release tension with each breath. I am capable and resilient.",
        "sad": "I am worthy of love and happiness. This feeling will pass, and brighter days are ahead.",
        "overwhelmed": "I take things one step at a time. I am doing my best, and that is enough.",
        "uncertain": "I trust the journey, even when I cannot see the path. I am exactly where I need to be.",
        "excited": "I embrace this positive energy. I am open to all the wonderful possibilities ahead.",
        "grateful": "I appreciate this moment and all the blessings in my life. I am abundant.",
        "confident": "I believe in myself and my abilities. I am capable of achieving great things."
    }
    
    base_affirmation = affirmations.get(mood.lower(), 
                                       "I am enough. I am worthy. I am capable.")
    
    if situation:
        return f"{base_affirmation} {situation.capitalize()} is an opportunity for growth."
    
    return base_affirmation

if __name__ == '__main__':
    print(" Starting AI Wellness Affirmation API...")
    print(" Running on http://localhost:5000")
    print(f" AI Status: {'ENABLED ✅ (FREE Groq AI)' if GROQ_API_KEY else 'DISABLED - Add GROQ_API_KEY to .env file'}")
    print("\n Endpoints:")
    print("   GET  / - Health check")
    print("   POST /api/generate-affirmation - Generate affirmation")
    print("   GET  /api/affirmations - View all affirmations")
    app.run(debug=True, port=5000)