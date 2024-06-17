async function submitPrompt() {
    const promptInput = document.getElementById('prompt-input');
    const prompt = promptInput.value.trim(); // Trim whitespace from input

    if (!prompt) return; // Prevent empty submissions

    const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });

    if (response.ok) {
        const data = await response.json();
        addChatEntry(prompt, data);
        promptInput.value = ''; // Clear the input field
    } else {
        console.error('Failed to get recommendations');
    }
}

function addChatEntry(prompt, data) {
    const chatHistory = document.getElementById('chat-history');

    // Create user prompt entry
    const userEntry = document.createElement('div');
    userEntry.className = 'chat-entry user';
    userEntry.innerHTML = `<p>${prompt}</p>`;
    chatHistory.appendChild(userEntry);

    // Create bot response entry
    const botEntry = document.createElement('div');
    botEntry.className = 'chat-entry bot';
    botEntry.innerHTML = `
        <h2>Top Recommendation</h2>
        ${createProfileCard(data.top)}
        <h2>Other Relevant Options</h2>
        ${data.others.map(profile => createProfileCard(profile)).join('')}
    `;
    chatHistory.appendChild(botEntry);

    // Ensure the chat section scrolls to the bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function createProfileCard(profile) {
    return `
        <div class="profile-card">
            <h3>${profile.name}</h3>
            <p><strong>Experience:</strong> ${profile.experience}</p>
            <p><strong>Availability:</strong> ${profile.availability}</p>
            <p><strong>Skills:</strong> ${profile.skills.join(', ')}</p>
            <p><strong>Previous Projects:</strong> ${profile.previousProjects.join(', ')}</p>
        </div>
    `;
}
