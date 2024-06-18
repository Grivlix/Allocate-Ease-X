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
    let aiName = "Sayj 1.0";
    const botEntry = document.createElement('div');
    botEntry.className = 'chat-entry bot';
    botEntry.innerHTML = `
        <h2>${aiName}: Top Recommendation</h2>
        ${createProfileCard(data.top)}
        <h2>${aiName}: Other Relevant Options</h2>
        ${data.others.map(profile => createProfileCard(profile)).join('')}
    `;
    chatHistory.appendChild(botEntry);

    // Ensure the chat section scrolls to the bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function createProfileCard(profile) {
    return `
        <div class="profile-card">
            <img src=${profile.image}>
            <h3>${profile.name}</h3>
            <p class="profile-role"><strong>Role:</strong> ${profile.job_title}</p>
            <p><strong>Employment Type:</strong> ${profile.employment_type}</p>
            <p><strong>Contact Info:</strong> ${profile.contact_info}</p>
            <p><strong>Available Hours/Week:</strong> ${profile.available_hours_per_week} hours/week</p>
            <p><strong>Utilization:</strong> ${profile.utilization * 100}%</p>
            <p><strong>Skills:</strong> ${profile.skills.map(skill => `${skill.skill_name} (${skill.proficiency_level})`).join(', ')}</p>
            <p><strong>Previous Projects:</strong> ${profile.previous_projects.join(', ')}</p>
            <p><strong>Active Projects:</strong> ${profile.active_projects.join(', ')}</p>
        </div>
    `;
}
