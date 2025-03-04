function togglePassword(fieldId) {
    const passwordField = document.getElementById(fieldId);
    const icon = document.querySelector(`#${fieldId} + i`);
    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = "password";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}


// Show/hide doctor specific fields based on role selection
document.getElementById('role').addEventListener('change', function () {
    const doctorFields = document.getElementById('doctorFields');
    const requiredFields = ['main_diploma', 'certificate_serial', 'speciality'];

    if (this.value === 'DOCTOR') {
        doctorFields.classList.remove('d-none');
        // Add required attribute to fields when visible
        requiredFields.forEach(field => {
            document.getElementById(field).required = true;
        });
    } else {
        doctorFields.classList.add('d-none');
        // Remove required attribute from fields when hidden
        requiredFields.forEach(field => {
            document.getElementById(field).required = false;
        });
    }
});

// Initialize the form state on page load
document.addEventListener('DOMContentLoaded', function () {
    const roleSelect = document.getElementById('role');
    if (roleSelect.value !== 'DOCTOR') {
        const requiredFields = ['main_diploma', 'certificate_serial', 'speciality'];
        requiredFields.forEach(field => {
            document.getElementById(field).required = false;
        });
    }
});
