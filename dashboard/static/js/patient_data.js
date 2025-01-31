document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('patientForm');
    const messagesContainer = document.getElementById('formMessages');
    const phoneInput = document.querySelector('[name="phone_number"]');

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Clear previous messages and errors
            messagesContainer.innerHTML = '';
            clearFormErrors();

            const formData = new FormData(form);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showSuccessMessage(data.message);
                    } else {
                        displayFormErrors(data.errors);
                    }
                })
                .catch(error => {
                    showErrorMessage('An error occurred. Please try again.');
                });
        });
    }

    // Add phone number validation
    if (phoneInput) {
        phoneInput.addEventListener('input', function () {
            const phoneValue = this.value.replace(/\D/g, ''); // Remove non-digits
            this.value = phoneValue.slice(0, 10); // Limit to 10 digits
        });

        phoneInput.addEventListener('blur', function () {
            if (this.value.length !== 10) {
                this.classList.add('is-invalid');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback d-block';
                errorDiv.textContent = 'Phone number must be exactly 10 digits.';
                this.parentNode.insertBefore(errorDiv, this.nextSibling);
            }
        });
    }

    function clearFormErrors() {
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
        document.querySelectorAll('.invalid-feedback').forEach(el => {
            el.remove();
        });
    }

    function displayFormErrors(errors) {
        for (const [field, messages] of Object.entries(errors)) {
            const input = document.querySelector(`[name="${field}"]`);
            if (input) {
                input.classList.add('is-invalid');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'invalid-feedback d-block';
                errorDiv.innerHTML = messages.join('<br>');
                input.parentNode.insertBefore(errorDiv, input.nextSibling);
            }
        }
    }

    function showSuccessMessage(message) {
        messagesContainer.innerHTML = `
            <div class="alert alert-success">${message}</div>
        `;
    }

    function showErrorMessage(message) {
        messagesContainer.innerHTML = `
            <div class="alert alert-danger">${message}</div>
        `;
    }
}); 