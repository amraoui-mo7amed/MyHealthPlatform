document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('id_thumbnail');
    const preview = document.getElementById('thumbnail_preview');

    fileInput.addEventListener('change', function (event) {
        if (event.target.files && event.target.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block'; // Show the image preview
            };

            reader.readAsDataURL(event.target.files[0]);
        }
    });
});
// Updating the profile
// document.getElementById('user-overview').addEventListener('submit', function (e) {
//     e.preventDefault();

//     const formData = new FormData(this);
//     const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//     fetch('/dashboard/user/edit/', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': csrfToken,
//         },
//         body: formData
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 Swal.fire({
//                     icon: 'success',
//                     title: 'Success',
//                     text: data.message,
//                     timer: 3000,
//                     showConfirmButton: false
//                 }).then(() => {
//                     // Redirect after SweetAlert confirmation
//                     window.location.href = '/dashboard/user/';
//                 });
//             } else {
//                 const errors = data.errors;
//                 let errorMessages = '';
//                 for (const field in errors) {
//                     errorMessages += `${field}: ${errors[field]}<br>`;
//                 }
//                 Swal.fire({
//                     icon: 'error',
//                     title: 'Validation Errors',
//                     html: errorMessages,
//                     timer: 5000,
//                     showConfirmButton: true
//                 });
//             }
//         })
//         .catch(error => {
//             Swal.fire({
//                 icon: 'error',
//                 title: 'Oops...',
//                 text: 'Something went wrong! Please try again.',
//             });
//         });
// });
