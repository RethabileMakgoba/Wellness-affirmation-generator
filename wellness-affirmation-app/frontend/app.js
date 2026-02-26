/**
 * AI Wellness Affirmation Generator - Frontend JavaScript
 * Connects the HTML interface to the Python Flask backend on Render
 */

// 🔥 LIVE backend URL
const API_URL = 'https://wellness-affirmation-generator.onrender.com';

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
 */
async function handleGenerateAffirmation() {
    const mood = moodSelect.value;
    const situation = situationInput.value.trim();

    // Validation
    if (!mood) {
        showError("Please select how you're feeling.");
        return;
    }

    hideAllSections();
    loadingSection.classList.remove('hidden');
    generateBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/api/generate-affirmation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mood, situation })
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            displayAffirmation(data.affirmation);
        } else {
            throw new Error(data.error || 'Failed to generate affirmation.');
        }

    } catch (error) {
        console.error('Error:', error);
        showError('Unable to connect to the server. Please try again.');
    } finally {
        generateBtn.disabled = false;
    }
}

/**
 * Display the generated affirmation on the page
 */
function displayAffirmation(affirmation) {
    hideAllSections();
    affirmationText.textContent = affirmation;
    resultSection.classList.remove('hidden');
}

/**
 * Show an error message on the page
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
 * Hide all UI sections
 */
function hideAllSections() {
    resultSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

/**
 * Reset the form to initial state
 */
function resetForm() {
    hideAllSections();
    moodSelect.value = '';
    situationInput.value = '';
    moodSelect.focus();
}

/**
 * Optional: Test backend connection on page load
 */
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_URL}/`);
        const data = await response.json();
        console.log('✅ Backend connection successful:', data);
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
    }
}

// Test backend on page load
testBackendConnection();
