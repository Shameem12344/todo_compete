console.log('main.js is running');

// Creates the function to create a sparkle effect
function createSparkle(x, y) {
    console.log('Creating sparkle at', x, y);
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    sparkle.style.left = `${x}px`;
    sparkle.style.top = `${y}px`;
    document.body.appendChild(sparkle);

    setTimeout(() => {
        sparkle.remove();
    }, 1000);
}

// Adds gray sparkles on click, more like ash
document.addEventListener('click', (e) => {
    console.log('Click detected at', e.clientX, e.clientY);
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            createSparkle(e.clientX, e.clientY);
        }, i * 50);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;

    // Checks for saved dark mode preference depedning on the toggle
    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }

    darkModeToggle.addEventListener('change', () => {
        if (darkModeToggle.checked) {
            body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
        } else {
            body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'disabled');
        }
    });

    // Updates greeting based on time of day
    const greeting = document.getElementById('greeting');
    if (greeting) {
        const username = greeting.dataset.username;
        const hour = new Date().getHours();
        let message = 'Hello';
        if (hour < 12) message = `Good Morning, ${username}`;
        else if (hour < 18) message = `Good Afternoon, ${username}`;
        else message = `Good Evening, ${username}`;
        greeting.textContent = message;
    }
});

console.log('main.js finished loading');
