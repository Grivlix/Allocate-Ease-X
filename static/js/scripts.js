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
        <div class="profile-card-container">
            ${data.others.map(profile => createProfileCard(profile)).join('')}
        </div>
    `;
    chatHistory.appendChild(botEntry);

    // Ensure the chat section scrolls to the bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function createProfileCard(profile) {
    const hoursColor = getHoursColor(profile.available_hours_per_week);
    const utilizationColor = getUtilizationColor(profile.utilization);

    return `
        <div class="profile-card">
            <img src=${profile.image}>
            <h3>${profile.name}</h3>
            <p class="profile-role"><strong>Role:</strong> ${profile.job_title}</p>
            <p><strong>Employment Type:</strong> ${profile.employment_type}</p>
            <p><strong>Available Hours Per Week:</strong> <span style="color: ${hoursColor}">${profile.available_hours_per_week}</span></p>
            <div class="utilization-chart" style="background: conic-gradient(${utilizationColor} 0% ${profile.utilization * 100}%, #ddd ${profile.utilization * 100}% 100%)"></div>
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
            <button onclick="openAssignForm(${profile.id})">Assign to Project</button>
        </div>
    `;
}

function getHoursColor(hours) {
    if (hours <= 40) {
        return 'green';
    } else if (hours <= 70) {
        return 'yellow';
    } else {
        return 'red';
    }
}

function getUtilizationColor(utilization) {
    if (utilization <= 0.4) {
        return 'green';
    } else if (utilization <= 0.7) {
        return 'yellow';
    } else {
        return 'red';
    }
}

function openAssignForm(employeeId) {
    const formHtml = `
        <div class="assign-form">
            <h3>Assign Employee to Project</h3>
            <input type="hidden" id="assign-employee-id" value="${employeeId}">
            <label for="project-id">Project ID:</label>
            <input type="number" id="project-id" placeholder="Enter project ID">
            <label for="task-hours">Task Hours:</label>
            <input type="number" id="task-hours" placeholder="Enter task hours">
            <button onclick="assignEmployee()">Assign</button>
            <button onclick="closeAssignForm()">Cancel</button>
        </div>
    `;
    const formContainer = document.getElementById('form-container');
    formContainer.innerHTML = formHtml;
}

function closeAssignForm() {
    const formContainer = document.getElementById('form-container');
    formContainer.innerHTML = '';
}

async function assignEmployee() {
    const employeeId = document.getElementById('assign-employee-id').value;
    const projectId = document.getElementById('project-id').value;
    const taskHours = document.getElementById('task-hours').value;

    const response = await fetch('/assign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            employee_id: employeeId,
            project_id: projectId,
            task_hours: taskHours
        })
    });

    if (response.ok) {
        alert('Employee assigned successfully!');
        closeAssignForm();
    } else {
        console.error('Failed to assign employee');
    }
}
