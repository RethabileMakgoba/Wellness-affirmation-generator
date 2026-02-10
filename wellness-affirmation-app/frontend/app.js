/**
 * AI Wellness Affirmation Generator - Frontend JavaScript
 * Connects the HTML interface to the Python Flask backend
 */

// Configuration
const API_URL = 'http://localhost:5000';

// DOM Elements
const moodSelect = document.getElementById('mood');
const situationInput = document.getElementById('situation');
const generateBtn = document.getElementById('generateBtn');
const newAffirmationBtn = document.getElementById('newAffirmationBtn');
const resultSection = document.getElementById('resultSection');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const affirmationText = document.getElementById('affirmationText');
const errorText = document.getElementById('errorText');

// Event Listeners
generateBtn.addEventListener('click', handleGenerateAffirmation);
newAffirmationBtn.addEventListener('click', resetForm);

// Handle Enter key in situation input
situationInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleGenerateAffirmation();
    }
});

/**
 * Main function to generate affirmation
 * This is where the frontend connects to the backend!
 */
async function handleGenerateAffirmation() {
    const mood = moodSelect.value;
    const situation = situationInput.value;
    
    // Validation
    if (!mood) {
        showError('Please select how you\'re feeling');
        return;
    }
    
    // Show loading state
    hideAllSections();
    loadingSection.classList.remove('hidden');
    generateBtn.disabled = true;
    
    try {
        // THIS IS THE KEY PART: Frontend calling Backend API
        const response = await fetch(`${API_URL}/api/generate-affirmation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mood: mood,
                situation: situation
            })
        });
        
        // Check if request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse the JSON response from backend
        const data = await response.json();
        
        if (data.success) {
            // Display the affirmation
            displayAffirmation(data.affirmation);
        } else {
            throw new Error(data.error || 'Failed to generate affirmation');
        }
        
    } catch (error) {
        console.error('Error generating affirmation:', error);
        showError('Unable to connect to the server. Please make sure the backend is running.');
    } finally {
        generateBtn.disabled = false;
    }
}

/**
 * Display the generated affirmation
 */
function displayAffirmation(affirmation) {
    hideAllSections();
    affirmationText.textContent = affirmation;
    resultSection.classList.remove('hidden');
}

/**
 * Show error message
 */
function showError(message) {
    hideAllSections();
    errorText.textContent = message;
    errorSection.classList.remove('hidden');
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        errorSection.classList.add('hidden');
    }, 5000);
}

/**
 * Hide all sections
 */
function hideAllSections() {
    resultSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

/**
 * Reset form to initial state
 */
function resetForm() {
    hideAllSections();
    moodSelect.value = '';
    situationInput.value = '';
    moodSelect.focus();
}

/**
 * Test backend connection on page load
 */
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_URL}/`);
        const data = await response.json();
        console.log('✅ Backend connection successful:', data);
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        console.log('Make sure to run: python app.py in the backend folder');
    }
}

// Test connection when page loads
testBackendConnection();

console.log('🚀 Frontend loaded successfully');
console.log('📡 Connecting to backend at:', API_URL);
