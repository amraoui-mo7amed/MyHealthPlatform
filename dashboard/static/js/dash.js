document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL path
    const currentPath = window.location.pathname;

    // Select all nav-items
    const navItems = document.querySelectorAll("#menu .nav-item");

    // Loop through nav-items to find a match
    navItems.forEach(item => {
        const itemUrl = item.getAttribute("data-url");

        if (currentPath.startsWith(itemUrl)) {
            // Add the active class
            item.classList.add("active");
        }
    });
});
// JavaScript to add any interactivity if needed
document.querySelectorAll('.dropdown-menu').forEach(menu => {
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!menu.parentElement.contains(e.target)) {
            menu.style.display = 'none';
        }
    });

    // Open dropdown on button click
    menu.parentElement.addEventListener('click', () => {
        const isVisible = menu.style.display === 'flex';
        menu.style.display = isVisible ? 'none' : 'flex';
    });
});
// Rest Notifications Count
document.addEventListener('DOMContentLoaded', function () {
    const notificationButton = document.querySelector('.mark-as-read');

    if (notificationButton) {
        notificationButton.addEventListener('click', function () {
            // SweetAlert Confirmation
            Swal.fire({
                title: 'Mark all as read?',
                text: "This will mark all your notifications as read.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, reset!',
                cancelButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    // If user confirms, make the POST request
                    fetch("/dashboard/reset-notifications/", {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": "{{ csrf_token }}", // Replace with CSRF token
                            "Content-Type": "application/json"
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire(
                                    'Reset!',
                                    'Done.',
                                    'success'
                                );

                                // Update the notifications count
                                const notificationCount = document.querySelector('.notification-btn .bg-teal.text-white');
                                if (notificationCount) {
                                    notificationCount.textContent = "0";
                                }
                            } else {
                                Swal.fire(
                                    'Error!',
                                    data.message || 'Failed to reset notifications.',
                                    'error'
                                );
                            }
                        })
                        .catch(error => {
                            console.error('Request failed:', error);
                            Swal.fire(
                                'Error!',
                                'An unexpected error occurred.',
                                'error'
                            );
                        });
                }
            });
        });
    }
});

// Controlling the sidebar visibility
let MenuBtn = document.getElementById('menu-btn')
let SideBar = document.getElementById('sidebar')

// Hide sidebar when clicking outside
document.addEventListener('click', (e) => {
    if (!SideBar.contains(e.target) && !MenuBtn.contains(e.target)) {
        SideBar.classList.replace('show-sidebar', 'hide-sidebar')
    }
});

MenuBtn.addEventListener('click', () => {
    if (SideBar.classList.contains('show-sidebar')) {
        SideBar.classList.replace('show-sidebar', 'hide-sidebar')
    }
    else {
        SideBar.classList.replace('hide-sidebar', 'show-sidebar')
    }
})
// Datatables
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.datatable').forEach(table => {
        new DataTable(table, {
            paging: true,
            lengthChange: true,
            searching: true,
            ordering: true,
            info: true,
            autoWidth: false,
            responsive: true,

        });
    });
});

// Nutrition dropdown toggle
// document.getElementById('nt-drodown-toggel').addEventListener('click', function () {
//     const dropdownList = document.getElementById('nt-dropdown-list-items');
//     const chevron = this.querySelector('i');

//     if (dropdownList.style.display === 'none' || !dropdownList.style.display) {
//         dropdownList.style.display = 'block';
//         chevron.classList.remove('fa-chevron-down');
//         chevron.classList.add('fa-chevron-up');
//     } else {
//         dropdownList.style.display = 'none';
//         chevron.classList.remove('fa-chevron-up');
//         chevron.classList.add('fa-chevron-down');
//     }
// });

// Digital Watch
function updateDigitalWatch() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('digitalWatch').textContent = `${hours}:${minutes}:${seconds}`;
    
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('currentDate').textContent = now.toLocaleDateString('en-US', options);
}

// Calendar
let currentDate = new Date();

function renderCalendar() {
    const monthYear = document.getElementById('currentMonthYear');
    const calendarGrid = document.getElementById('calendarGrid');
    
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // Set month and year
    monthYear.textContent = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(currentDate);
    
    // Get first and last day of month
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    // Clear previous calendar
    calendarGrid.innerHTML = '';
    
    // Add empty cells for days before first day
    for (let i = 0; i < firstDay.getDay(); i++) {
        calendarGrid.innerHTML += `<div class="calendar-day"></div>`;
    }
    
    // Add days of the month
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const date = new Date(year, month, day);
        const isToday = date.toDateString() === new Date().toDateString();
        calendarGrid.innerHTML += `
            <div class="calendar-day ${isToday ? 'today' : ''}">
                ${day}
            </div>`;
    }
}

// Event Handling
document.getElementById('prevMonth').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

document.getElementById('nextMonth').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

// Upcoming Events
function updateUpcomingEvents() {
    // Get today's date in YYYY-MM-DD format
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const day = String(today.getDate()).padStart(2, '0');
    const todayFormatted = `${year}-${month}-${day}`;

    const events = [
        { date: todayFormatted, time: '08:00', title: '🍞 Breakfast', status: 'Upcoming' },
        { date: todayFormatted, time: '12:00', title: '🥗 Lunch', status: 'Upcoming' },
        { date: todayFormatted, time: '16:00', title: '🍫 Snacks', status: 'Upcoming' },
        { date: todayFormatted, time: '20:00', title: '🍚 Dinner', status: 'Upcoming' }
    ];

    const tableBody = document.getElementById('upcomingEventsTable');
    tableBody.innerHTML = '';

    const now = new Date();
    const todayDate = new Date(now.getFullYear(), now.getMonth(), now.getDate()); // Set time to midnight

    events.forEach(event => {
        const eventDateTime = new Date(`${event.date}T${event.time}:00`);
        let status = event.status;

        // Check if the event is in the past
        if (eventDateTime < now) {
            status = 'Completed'; // Change status for past events
        }

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${event.date}</td>
            <td>${event.time}</td>
            <td>${event.title}</td>
            <td><span class="badge ${status === 'Upcoming' ? '' : 'active'}">${status}</span></td>
        `;
        tableBody.appendChild(row);
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Digital Watch
    setInterval(updateDigitalWatch, 1000);
    updateDigitalWatch();

    // Calendar
    renderCalendar();

    // Upcoming Events
    updateUpcomingEvents();
});