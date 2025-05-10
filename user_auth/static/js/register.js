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



// Init the Provinces

document.addEventListener('DOMContentLoaded', function () {
    const selectHeader = document.querySelector('.custom-select .select-header');
    const selectOptions = document.getElementById('wilaya-options');
    const hiddenSelect = document.getElementById('wilaya');

    // Algerian provinces data
    const provinces = [
        { value: "01", name: "Adrar" },
        { value: "02", name: "Chlef" },
        { value: "03", name: "Laghouat" },
        { value: "04", name: "Oum El Bouaghi" },
        { value: "05", name: "Batna" },
        { value: "06", name: "Béjaïa" },
        { value: "07", name: "Biskra" },
        { value: "08", name: "Béchar" },
        { value: "09", name: "Blida" },
        { value: "10", name: "Bouira" },
        { value: "11", name: "Tamanrasset" },
        { value: "12", name: "Tébessa" },
        { value: "13", name: "Tlemcen" },
        { value: "14", name: "Tiaret" },
        { value: "15", name: "Tizi Ouzou" },
        { value: "16", name: "Algiers" },
        { value: "17", name: "Djelfa" },
        { value: "18", name: "Jijel" },
        { value: "19", name: "Sétif" },
        { value: "20", name: "Saïda" },
        { value: "21", name: "Skikda" },
        { value: "22", name: "Sidi Bel Abbès" },
        { value: "23", name: "Annaba" },
        { value: "24", name: "Guelma" },
        { value: "25", name: "Constantine" },
        { value: "26", name: "Médéa" },
        { value: "27", name: "Mostaganem" },
        { value: "28", name: "MSila" },
        { value: "29", name: "Mascara" },
        { value: "30", name: "Ouargla" },
        { value: "31", name: "Oran" },
        { value: "32", name: "El Bayadh" },
        { value: "33", name: "Illizi" },
        { value: "34", name: "Bordj Bou Arréridj" },
        { value: "35", name: "Boumerdès" },
        { value: "36", name: "El Tarf" },
        { value: "37", name: "Tindouf" },
        { value: "38", name: "Tissemsilt" },
        { value: "39", name: "El Oued" },
        { value: "40", name: "Khenchela" },
        { value: "41", name: "Souk Ahras" },
        { value: "42", name: "Tipaza" },
        { value: "43", name: "Mila" },
        { value: "44", name: "Aïn Defla" },
        { value: "45", name: "Naâma" },
        { value: "46", name: "Aïn Témouchent" },
        { value: "47", name: "Ghardaïa" },
        { value: "48", name: "Relizane" },
        { value: "49", name: "Timimoun" },
        { value: "50", name: "Bordj Badji Mokhtar" },
        { value: "51", name: "Ouled Djellal" },
        { value: "52", name: "Béni Abbès" },
        { value: "53", name: "In Salah" },
        { value: "54", name: "In Guezzam" },
        { value: "55", name: "Touggourt" },
        { value: "56", name: "Djanet" },
        { value: "57", name: "El MGhair" },
        { value: "58", name: "El Menia" }
    ];

    // Create options
    provinces.forEach(province => {
        // For visible dropdown
        const option = document.createElement('div');
        option.className = 'select-option';
        option.textContent = province.name;
        option.dataset.value = province.value;

        option.addEventListener('click', function () {
            selectHeader.textContent = this.textContent;
            document.querySelectorAll('.select-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            this.classList.add('selected');
            selectOptions.style.display = 'none';

            // Update hidden select
            hiddenSelect.innerHTML = '';
            const hiddenOption = document.createElement('option');
            hiddenOption.value = province.value;
            hiddenOption.textContent = province.name;
            hiddenOption.selected = true;
            hiddenSelect.appendChild(hiddenOption);
        });

        selectOptions.appendChild(option);

        // For hidden select (initial options)
        if (hiddenSelect.querySelector(`option[value="${province.value}"]`) === null) {
            const hiddenOption = document.createElement('option');
            hiddenOption.value = province.value;
            hiddenOption.textContent = province.name;
            hiddenSelect.appendChild(hiddenOption);
        }
    });

    // Toggle dropdown visibility
    selectHeader.addEventListener('click', function (e) {
        e.stopPropagation();
        selectOptions.style.display = selectOptions.style.display === 'block' ? 'none' : 'block';
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function () {
        selectOptions.style.display = 'none';
    });
});
