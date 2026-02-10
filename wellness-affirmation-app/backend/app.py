"""
AI Wellness Affirmation Generator - Backend API
A Flask application that generates personalized wellness affirmations using AI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to connect from different origin

# In-memory storage for now (we'll add MongoDB later)
affirmations_db = []

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Wellness Affirmation API is running",
        "version": "1.0.0"
    })

@app.route('/api/generate-affirmation', methods=['POST'])
def generate_affirmation():
    """
    Generate a personalized affirmation based on user's mood/situation
    
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
        
        # TODO: We'll integrate AI here in the next step
        # For now, return a simple affirmation
        affirmation = generate_simple_affirmation(mood, situation)
        
        # Store in our simple database
        entry = {
            "id": len(affirmations_db) + 1,
            "mood": mood,
            "situation": situation,
            "affirmation": affirmation,
            "timestamp": datetime.now().isoformat()
        }
        affirmations_db.append(entry)
        
        return jsonify({
            "success": True,
            "affirmation": affirmation,
            "mood": mood,
            "id": entry["id"]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/affirmations', methods=['GET'])
def get_affirmations():
    """Get all stored affirmations"""
    return jsonify({
        "success": True,
        "count": len(affirmations_db),
        "affirmations": affirmations_db
    })

def generate_simple_affirmation(mood, situation):
    """
    Generate a simple affirmation (placeholder before AI integration)
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
    print(" Endpoints:")
    print("   GET  / - Health check")
    print("   POST /api/generate-affirmation - Generate affirmation")
    print("   GET  /api/affirmations - View all affirmations")
    app.run(debug=True, port=5000)
