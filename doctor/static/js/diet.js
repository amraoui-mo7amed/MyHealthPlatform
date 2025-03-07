document.getElementById('updateDietBtn').addEventListener('click', function () {
    const dietDetails = document.getElementById('dietDetails');
    const updateForm = document.getElementById('updateForm');

    if (dietDetails.style.display === 'none') {
        dietDetails.style.display = 'block';
        updateForm.style.display = 'none';
    } else {
        dietDetails.style.display = 'none';
        updateForm.style.display = 'block';
    }
});