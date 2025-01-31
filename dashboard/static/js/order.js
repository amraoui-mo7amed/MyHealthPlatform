const statusBtn = document.querySelectorAll('.approveBtn');
const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

statusBtn.forEach(btn => {
    btn.addEventListener('click', () => {
        const endpoint = btn.getAttribute('data-url'); // Fix variable name

        fetch(endpoint, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: data.message,
                        icon: "success",
                        showConfirmButton: false,
                        timer: 3000 // Close the alert after 3 seconds
                    }).then(() => {
                        location.reload(); // Reload the page after the alert closes
                    });
                } else {
                    Swal.fire({
                        title: data.message,
                        icon: "error"
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error); // Handle network errors
                Swal.fire({
                    title: 'An error occurred. Please try again.',
                    icon: "error"
                });
            });
    });
});