document.addEventListener('DOMContentLoaded', function () {
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiInput = document.getElementById('bmi');
    if (bmiInput.value) {
        updateBMIProgress(bmiInput.value)
    }

    function calculateBMI() {
        const height = parseFloat(heightInput.value) / 100; // Convert cm to m
        const weight = parseFloat(weightInput.value);

        if (height > 0 && weight > 0) {
            const bmi = (weight / (height * height)).toFixed(2);
            bmiInput.value = bmi;
            console.log(bmi);

            updateBMIProgress(parseFloat(bmi));
        } else {
            bmiInput.value = '';
        }
    }

    heightInput.addEventListener('input', calculateBMI);
    weightInput.addEventListener('input', calculateBMI);
});

// Initialize fields on page load
document.addEventListener('DOMContentLoaded', function () {
    // Hide all fields by default
    document.getElementById('diabetesFields').style.display = 'none';
    document.getElementById('obesityFields').style.display = 'none';
    document.getElementById('diabetesandobesityFields').style.display = 'none';

    // Then check if any should be shown
    toggleDiabetesFields();
    toggleObesityFields();
    toggleDiabetesAndObesityFields();
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

// Show/hide diabetes and obesity fields when checkbox is clicked or on page load
function toggleDiabetesAndObesityFields() {
    const diabetesAndObesityFields = document.getElementById('diabetesandobesityFields');
    const diabetesAndObesityCheckbox = document.getElementById('diabetesandobesity');
    diabetesAndObesityFields.style.display = diabetesAndObesityCheckbox.checked ? 'block' : 'none';
}

document.getElementById('diabetesandobesity').addEventListener('change', toggleDiabetesAndObesityFields);
toggleDiabetesAndObesityFields(); // This checks the state on page load

// Handle allergy details visibility
function toggleAllergyDetails() {
    const allergyDetails = document.getElementById('allergyDetails');
    const allergyYes = document.getElementById('food_allergy_yes');
    allergyDetails.style.display = allergyYes.checked ? 'block' : 'none';
}

document.getElementById('food_allergy_yes').addEventListener('change', toggleAllergyDetails);
document.getElementById('food_allergy_no').addEventListener('change', toggleAllergyDetails);
toggleAllergyDetails();

// Handle medication details visibility
function toggleMedicationDetails() {
    const medicationDetails = document.getElementById('medicationDetails');
    const medicationYes = document.getElementById('medication_yes');
    medicationDetails.style.display = medicationYes.checked ? 'block' : 'none';
}

document.getElementById('medication_yes').addEventListener('change', toggleMedicationDetails);
document.getElementById('medication_no').addEventListener('change', toggleMedicationDetails);
toggleMedicationDetails();


function showSection(sectionNumber) {
    // Hide all sections
    const sections = document.querySelectorAll('[id^="section"]');
    const submitDiv = document.getElementById('submitDiv')
    sections.forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected section
    const formTitle = document.getElementsByClassName('form_title')[0]
    let title = ''
    if (sectionNumber === 1) {
        title = 'Body Mass Indicator'
    }
    else if (sectionNumber === 2) {
        title = 'Health Conditions'
    }
    else if (sectionNumber === 3) {
        title = 'Lifestyle'
        submitDiv.classList.remove('d-none')
        submitDiv.classList.add('d-block')
    }
    formTitle.innerText = title
    const currentSection = document.getElementById(`section${sectionNumber}`);
    if (currentSection) {
        currentSection.style.display = 'block';
    }
}

function updateBMIProgress(bmiValue) {
    const progressBar = document.getElementById('bmiProgressBar');
    const bmiStatus = document.getElementById('bmiStatus');
    let status = '';
    let color = '#76e5b1';
    
    bmiValue = parseFloat(bmiValue);
    const circumference = 565.48; // 2 * π * r (where r = 90)
    const progress = (bmiValue / 40) * circumference; // Assuming 40 as max BMI
    
    if (bmiValue < 18.5) {
        status = 'Underweight';
        color = '#17a2b8'; // Blue
    } else if (bmiValue >= 18.5 && bmiValue <= 24.9) {
        status = 'Normal';
        color = '#28a745'; // Green
    } else if (bmiValue >= 25 && bmiValue <= 29.9) {
        status = 'Overweight';
        color = '#ffc107'; // Yellow
    } else {
        status = 'Obese';
        color = '#dc3545'; // Red
    }
    
    // Update progress bar
    progressBar.style.stroke = color;
    progressBar.style.strokeDashoffset = circumference - progress;
    
    // Update status text
    bmiStatus.textContent = bmiValue.toFixed(1) + ' : ' + status;
    bmiStatus.style.fill = color;
}

