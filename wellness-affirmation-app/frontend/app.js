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
situationInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleGenerateAffirmation();
});

async function handleGenerateAffirmation() {
    const mood = moodSelect.value;
    const situation = situationInput.value.trim();

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

        if (!response.ok) throw new Error(`Server returned status ${response.status}`);

        const data = await response.json();

        if (data.success) displayAffirmation(data.affirmation);
        else throw new Error(data.error || 'Failed to generate affirmation.');

    } catch (error) {
        console.error('Error:', error);
        showError('Unable to connect to the server. Please try again.');
    } finally {
        generateBtn.disabled = false;
    }
}

function displayAffirmation(affirmation) {
    hideAllSections();
    affirmationText.textContent = affirmation;
    resultSection.classList.remove('hidden');
}

function showError(message) {
    hideAllSections();
    errorText.textContent = message;
    errorSection.classList.remove('hidden');
    setTimeout(() => errorSection.classList.add('hidden'), 5000);
}

function hideAllSections() {
    resultSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

function resetForm() {
    hideAllSections();
    moodSelect.value = '';
    situationInput.value = '';
    moodSelect.focus();
}

// Optional: Test backend connection
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_URL}/`);
        const data = await response.json();
        console.log('✅ Backend connection successful:', data);
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
    }
}

testBackendConnection();
