

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

// Show/hide diabetes fields when checkbox is clicked
document.getElementById('diabetes').addEventListener('change', function () {
    const diabetesFields = document.getElementById('diabetesFields');
    diabetesFields.style.display = this.checked ? 'block' : 'none';
});


// Show/hide obesity fields when checkbox is clicked
document.getElementById('obesity').addEventListener('change', function () {
    const obesityFields = document.getElementById('obesityFields');
    obesityFields.style.display = this.checked ? 'block' : 'none';
});
