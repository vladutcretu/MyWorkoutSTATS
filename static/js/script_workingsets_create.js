// The showForm() function is used to display the form corresponding to the selected exercise type
function showForm(formType) {
    // Get references to the weights and resistance form elements
    var weightForm = document.getElementById('weightForm');
    var enduranceForm = document.getElementById('enduranceForm');
    // Get references to the weight, reps, distance, and time inputs
    var weightInput = document.getElementById('weight');
    var repetitionsInput = document.getElementById('repetitions');
    var distanceInput = document.getElementById('distance');
    var timeInput = document.getElementById('time');
    
    // Check the form type and display the appropriate form accordingly
    if (formType === 'weight') {
        weightForm.style.display = 'block';
        enduranceForm.style.display = 'none';
        // Reset the distance and time values for the resistance form when endurance type is selected
        distanceInput.value = '';
        timeInput.value = '';
    } else if (formType === 'endurance') {
        weightForm.style.display = 'none';
        enduranceForm.style.display = 'block';
        // Reset the weight and rep values for the weights form when weight type is selected
        weightInput.value = '';
        repetitionsInput.value = '';
    }
}

// The prepareForm() function is used to prepare the form for data submission
function prepareForm() {
    // Get references to the weight, reps, distance, and time inputs
    var weightInput = document.getElementById('weight');
    var repetitionsInput = document.getElementById('repetitions');
    var distanceInput = document.getElementById('distance');
    var timeInput = document.getElementById('time');

    // Ensures that the values entered in each field are valid: if a field is empty, keep the empty value
    if (weightInput.value === '') {
        weightInput.value = '';
    }

    if (repetitionsInput.value === '') {
        repetitionsInput.value = '';
    }

    if (distanceInput.value === '') {
        distanceInput.value = '';
    }

    if (timeInput.value === '') {
        timeInput.value = '';
    }

    // Send form
    document.querySelector('form').submit();
}

// The window.onload function is used to ensure the initial display of the weights form when the page loads
window.onload = function() {
    document.getElementById('weightForm').style.display = 'block';
};

