document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('id_thumbnail');
    const preview = document.getElementById('thumbnail_preview');
    const uploadIcon = document.querySelector('#thumbnail_container .upload-icon');

    fileInput.addEventListener('change', function (event) {
        if (event.target.files && event.target.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block'; // Show the image preview
                uploadIcon.style.display = 'none'; // Hide the upload icon
            };

            reader.readAsDataURL(event.target.files[0]);
        }
    });
});