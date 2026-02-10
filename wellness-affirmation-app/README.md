#  AI Wellness Affirmation Generator

A full-stack web application that generates personalized wellness affirmations based on your current mood and situation. Built to demonstrate frontend-backend integration with AI capabilities.

## Project Purpose

This project showcases:
- **Frontend to Backend Connection**: JavaScript frontend communicating with Python Flask API
- **RESTful API Design**: Clean API endpoints with proper HTTP methods
- **AI Integration**: (Coming in Phase 2) LLM-powered personalized affirmations
- **Full-Stack Development**: Complete application from UI to server logic

## Tech Stack

**Backend:**
- Python 3.x
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)

**Frontend:**
- HTML5
- CSS3 (Modern gradient design)
- Vanilla JavaScript (ES6+)

**Future Additions:**
- MongoDB (Database)
- OpenAI API / Anthropic Claude API (AI Generation)

## Project Structure

```
wellness-affirmation-app/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Styling
│   └── app.js              # JavaScript (connects to backend)
└── README.md               # This file
```

## Setup Instructions

### Step 1: Set Up Backend

1. Open terminal and navigate to backend folder:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
python app.py
```

You should see:
```
 Starting AI Wellness Affirmation API...
 Running on http://localhost:5000
```

### Step 2: Set Up Frontend

1. Open a NEW terminal (keep backend running!)

2. Navigate to frontend folder:
```bash
cd frontend
```

3. Open `index.html` in your browser:
- **Option 1**: Double-click `index.html`
- **Option 2**: Use VS Code Live Server extension
- **Option 3**: Run: `python -m http.server 8000` then visit `http://localhost:8000`

##  How to Use

1. **Select your mood** from the dropdown (e.g., "Anxious", "Stressed")
2. **Optionally describe your situation** (e.g., "preparing for job interview")
3. **Click "Generate My Affirmation"**
4. **Receive your personalized affirmation** 

##  How Frontend Connects to Backend

The key connection happens in `frontend/app.js`:

```javascript
// Frontend sends POST request to backend
const response = await fetch('http://localhost:5000/api/generate-affirmation', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        mood: mood,
        situation: situation
    })
});

// Backend processes request and returns JSON
const data = await response.json();
```

The backend (`backend/app.py`) receives this request, processes it, and sends back a JSON response:

```python
@app.route('/api/generate-affirmation', methods=['POST'])
def generate_affirmation():
    data = request.get_json()
    mood = data.get('mood')
    situation = data.get('situation')
    
    # Generate affirmation (will use AI in Phase 2)
    affirmation = generate_simple_affirmation(mood, situation)
    
    return jsonify({
        "success": True,
        "affirmation": affirmation
    })
```

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/generate-affirmation` | Generate affirmation |
| GET | `/api/affirmations` | View all affirmations |

##  Troubleshooting

**"Failed to connect to server"**
- Make sure backend is running (`python app.py`)
- Check that it's on port 5000
- Look for CORS errors in browser console

**"Module not found" errors**
- Make sure you activated virtual environment
- Run `pip install -r requirements.txt` again

##  Next Steps (Phase 2)

- [ ] Integrate OpenAI or Anthropic Claude API for AI-generated affirmations
- [ ] Add MongoDB database to store affirmations
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render
- [ ] Add user authentication
- [ ] Create mood tracking dashboard

##  Author

**Rethabile Makgoba**
- GitHub: [@RethabileMakgoba](https://github.com/RethabileMakgoba)
- Email: rethabilemakgoba23@gmail.com

##  License

This project is for portfolio purposes.

---

Built with 💜git init for mental wellbeing
