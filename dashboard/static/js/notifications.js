// Define showNotification in global scope
let showNotification;

// Create notification container and styles
document.addEventListener('DOMContentLoaded', () => {
    // Create notification container
    const notificationContainer = document.createElement('div');
    notificationContainer.id = 'notification-container';

    // Add styles for the notification container
    notificationContainer.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 40px;
        z-index: 1000;
        min-width: 300px;
        max-width: 400px;
    `;

    // Find the content-section and append the notification container
    const contentSection = document.querySelector('.content-section');
    if (contentSection) {
        // Make sure content-section can handle absolute positioning
        if (getComputedStyle(contentSection).position === 'static') {
            contentSection.style.position = 'relative';
        }
        contentSection.appendChild(notificationContainer);
    } else {
        console.warn('Could not find .content-section, falling back to body');
        document.body.appendChild(notificationContainer);
    }

    // Assign the function to the global variable
    showNotification = function (message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = message;

        // Style the notification
        notification.style.cssText = `
            background-color: var(--bs-light);
            border-left: 4px solid #007bff;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            margin-bottom: 10px;
            padding: 15px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease-in-out;
        `;

        // Add different colors based on notification type
        switch (type) {
            case 'success':
                notification.style.borderLeftColor = '#28a745';
                break;
            case 'error':
                notification.style.borderLeftColor = '#dc3545';
                break;
            case 'warning':
                notification.style.borderLeftColor = '#ffc107';
                break;
        }

        notificationContainer.appendChild(notification);

        // Trigger animation
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 10);

        // Auto-remove notification after 5 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    };

    // Define messages for each role
    const messages = {
        ADMIN: [
            { content: 'Hello Admin! Welcome back!', type: 'success', interval: 60000, startTime: '09:00', startImmediately: false }, // Every minute starting at 9 AM
        ],
        PATIENT: [
            { content: 'Breakfast time!', type: 'success', interval: 86400000, startTime: '08:00', startImmediately: false }, // Every 24 hours starting at 8 AM
            { content: 'Time for lunch!', type: 'success', interval: 86400000, startTime: '12:00', startImmediately: false }, // Every 24 hours starting at 12 PM
            { content: 'Snack time!', type: 'success', interval: 86400000, startTime: '16:00', startImmediately: false }, // Every 24 hours starting at 4 PM
            { content: 'Dinner time!', type: 'success', interval: 86400000, startTime: '20:00', startImmediately: false }, // Every 24 hours starting at 8 PM
            { content: 'Reminder: Drink water!', type: 'info', interval: 15 * 60 * 1000, startTime: '09:00', startImmediately: false }, // Every hour starting at 9 AM
        ],
        DOCTOR: [
            { content: 'Hello Doctor! You have new messages!', type: 'success', interval: 10000, startTime: '20:10', startImmediately: true }, // Every 10 seconds starting at 8:10 PM
        ]
    };

    // Get user role and schedule appropriate notifications
    const userRole = document.getElementById('user_role')?.value.toUpperCase() || 'GUEST';
    const roleMessages = messages[userRole] || [];

    // Schedule notifications for the user's role
    roleMessages.forEach(msg => {
        const [startHour, startMinute] = msg.startTime.split(':').map(Number);
        const now = new Date();
        const startTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), startHour, startMinute);

        // If the start time has already passed today, set it for tomorrow
        if (now > startTime) {
            startTime.setDate(startTime.getDate() + 1); // Set for tomorrow
        }

        // Calculate the time until the first display
        const timeUntilFirstDisplay = startTime - now;

        // Schedule the first display
        setTimeout(() => {
            showNotification(msg.content, msg.type); // Show the notification at the scheduled time

            // Set up the interval for repeated notifications
            setInterval(() => {
                showNotification(msg.content, msg.type); // Show the notification at the specified interval
            }, msg.interval);
        }, timeUntilFirstDisplay);

        // If the notification should start immediately, show it right away
        if (msg.startImmediately) {
            showNotification(msg.content, msg.type); // Show the notification immediately
            setInterval(() => {
                showNotification(msg.content, msg.type); // Show the notification at the specified interval
            }, msg.interval);
        }
    });
});
