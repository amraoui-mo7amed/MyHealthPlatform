document.addEventListener('DOMContentLoaded', function () {
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiInput = document.getElementById('bmi');

    function calculateBMI() {
        const height = parseFloat(heightInput.value) / 100; // Convert cm to m
        const weight = parseFloat(weightInput.value);

        if (height > 0 && weight > 0) {
            const bmi = (weight / (height * height)).toFixed(2);
            bmiInput.value = bmi;
        } else {
            bmiInput.value = '';
        }
    }

    heightInput.addEventListener('input', calculateBMI);
    weightInput.addEventListener('input', calculateBMI);
});

// Initialize fields on page load
document.addEventListener('DOMContentLoaded', function() {
    // Hide all fields by default
    document.getElementById('diabetesFields').style.display = 'none';
    document.getElementById('obesityFields').style.display = 'none';
    
    // Then check if any should be shown
    toggleDiabetesFields();
    toggleObesityFields();
});

// Show/hide diabetes fields when checkbox is clicked or on page load
function toggleDiabetesFields() {
    const diabetesFields = document.getElementById('diabetesFields');
    const diabetesCheckbox = document.getElementById('diabetes');
    diabetesFields.style.display = diabetesCheckbox.checked ? 'block' : 'none';
}

document.getElementById('diabetes').addEventListener('change', toggleDiabetesFields);
toggleDiabetesFields(); // This checks the state on page load

// Show/hide obesity fields when checkbox is clicked or on page load
function toggleObesityFields() {
    const obesityFields = document.getElementById('obesityFields');
    const obesityCheckbox = document.getElementById('obesity');
    obesityFields.style.display = obesityCheckbox.checked ? 'block' : 'none';
}

document.getElementById('obesity').addEventListener('change', toggleObesityFields);
toggleObesityFields(); // This checks the state on page load
