document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll('.delete-item');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();  // Prevent the default form submission

            const form = button.closest('form');  // Get the form element associated with the button
            const itemId = button.getAttribute('data-id');
            const deleteUrl = form.getAttribute('action');  // Get the URL for the form submission

            // SweetAlert Confirmation
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Make the AJAX POST request instead of submitting the form directly
                    fetch(deleteUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                        },
                        body: JSON.stringify({ id: itemId })  // Optionally send item ID as JSON
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire({
                                    title: 'Deleted!',
                                    text: data.success,
                                    icon: 'success'
                                }).then(() => {
                                    window.location.reload();  // Reload the page after successful deletion
                                });
                            } else {
                                Swal.fire({
                                    title: 'Error!',
                                    text: 'Something went wrong. Please try again.',
                                    icon: 'error'
                                });
                            }
                        })
                        .catch(error => {
                            Swal.fire({
                                title: 'Error!',
                                text: 'Failed to delete the item. Please try again later.',
                                icon: 'error'
                            });
                        });
                }
            });
        });
    });
});
