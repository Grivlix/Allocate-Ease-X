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
            <p><strong>Available Hours Per Week:</strong> ${profile.available_hours_per_week}</p>
            <p><strong>Utilization:</strong> ${profile.utilization * 100} %</p>
            <p><strong>Contact Info:</strong> ${profile.contact_info}</p>
            <p><strong>Upcoming Leave:</strong> ${profile.upcoming_leave}</p>
            <h4>Skills:</h4>
            <ul>
                ${profile.skills.map(skill => `<li>${skill.skill_name} (${skill.proficiency_level})</li>`).join('')}
            </ul>
            <h4>Active Projects:</h4>
            <ul>
                ${profile.active_projects.map(project => `<li>${project}</li>`).join('')}
            </ul>
            <h4>Previous Projects:</h4>
            <ul>
                ${profile.previous_projects.map(project => `<li>${project}</li>`).join('')}
            </ul>
            <div id="calendar-container-${profile.name}" class="calendar-container">
                <!-- Placeholder for the calendar -->
                <div class="calendar-header">
                    <button class="calendar-btn prev-month" onclick="changeMonth('${profile.name}', -1)">&#10094;</button>
                    <h3 class="calendar-month" id="calendar-month-${profile.name}"></h3>
                    <button class="calendar-btn next-month" onclick="changeMonth('${profile.name}', 1)">&#10095;</button>
                </div>
                <div class="calendar-grid" id="calendar-grid-${profile.name}"></div>
            </div>
        </div>
    `;
}

function initializeCalendar(profileName) {
    const calendarMonth = document.getElementById(`calendar-month-${profileName}`);
    const calendarGrid = document.getElementById(`calendar-grid-${profileName}`);
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();

    renderCalendar(profileName, currentMonth, currentYear);
}

function renderCalendar(profileName, month, year) {
    const calendarMonth = document.getElementById(`calendar-month-${profileName}`);
    const calendarGrid = document.getElementById(`calendar-grid-${profileName}`);
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    calendarMonth.innerText = `${monthNames[month]} ${year}`;
    calendarGrid.innerHTML = ''; // Clear the calendar grid

    // Fill in the days of the month
    for (let i = 0; i < firstDay; i++) {
        calendarGrid.innerHTML += '<div class="calendar-day empty"></div>';
    }

    for (let i = 1; i <= daysInMonth; i++) {
        calendarGrid.innerHTML += `<div class="calendar-day">${i}</div>`;
    }
}

function changeMonth(profileName, direction) {
    const calendarMonth = document.getElementById(`calendar-month-${profileName}`);
    let [currentMonth, currentYear] = calendarMonth.innerText.split(' ');

    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    let newMonth = monthNames.indexOf(currentMonth) + direction;
    let newYear = parseInt(currentYear);

    if (newMonth < 0) {
        newMonth = 11;
        newYear -= 1;
    } else if (newMonth > 11) {
        newMonth = 0;
        newYear += 1;
    }

    renderCalendar(profileName, newMonth, newYear);
}
