// Function to update days_diff and save it to localStorage
function updateDaysDiff(days) {
    // Get the current value of 'currentDaysDiff' from the URL query string
    var urlParams = new URLSearchParams(window.location.search);
    var currentDaysDiff = parseInt(urlParams.get('days_diff')) || 0;

    // Check if the "Current Day" button has been pressed and set 'days_diff' to 0 in that case
    if (days === 0) {
        currentDaysDiff = 0;
    } else {
        // Update value of 'currentDaysDiff' with 'days' value
        currentDaysDiff += days;
    }

    // Save the new value of 'currentDaysDiff' in the URL query string and redirect the user
    urlParams.set('days_diff', currentDaysDiff);
    var newUrl = `${window.location.pathname}?${urlParams.toString()}`;
    window.location.href = newUrl;
}

// Add events for each button to call the 'updateDaysDiff' function and update the value of 'currentDaysDiff' in the URL query string
document.getElementById('oneDayBackBtn').addEventListener('click', function() {
    updateDaysDiff(-1);
});

document.getElementById('currentDayBtn').addEventListener('click', function() {
    updateDaysDiff(0);
});

document.getElementById('oneDayLaterBtn').addEventListener('click', function() {
    updateDaysDiff(1);
});