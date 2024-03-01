/* Home */
// Funcție pentru a actualiza days_diff și a o salva în localStorage
function updateDaysDiff(days) {
    // Obține valoarea curentă a lui currentDaysDiff din query string-ul URL-ului
    var urlParams = new URLSearchParams(window.location.search);
    var currentDaysDiff = parseInt(urlParams.get('days_diff')) || 0;

    // Verifică dacă butonul "Current Day" a fost apăsat și setează days_diff la 0 în acest caz
    if (days === 0) {
        currentDaysDiff = 0;
    } else {
        // Actualizează valoarea lui currentDaysDiff cu days
        currentDaysDiff += days;
    }

    // Salvează noua valoare a lui currentDaysDiff în query string-ul URL-ului și redirecționează utilizatorul
    urlParams.set('days_diff', currentDaysDiff);
    var newUrl = `${window.location.pathname}?${urlParams.toString()}`;
    window.location.href = newUrl;
}

// Adaugă evenimentele pentru fiecare buton pentru a apela funcția updateDaysDiff și a actualiza valoarea lui currentDaysDiff în query string-ul URL-ului
document.getElementById('oneDayBackBtn').addEventListener('click', function() {
    updateDaysDiff(-1);
});

document.getElementById('currentDayBtn').addEventListener('click', function() {
    updateDaysDiff(0);
});

document.getElementById('oneDayLaterBtn').addEventListener('click', function() {
    updateDaysDiff(1);
});