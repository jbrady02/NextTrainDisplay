// Display the current day of the week, date, and time
function displayTime() {
    const now = new Date();
    const dayOfWeek = ["Sun.", "Mon.", "Tue.", "Wed.",
        "Thu.", "Fri.", "Sat."];
    dateAndTime = now.toLocaleString('en-US', {timeZone: 'America/New_York' })
    document.getElementById("time-text").textContent = 
        dayOfWeek[now.getDay()] + " " + dateAndTime;
}

function reload() {
    location.reload();
}

displayTime(); // Display the time as soon as the page loads
setInterval(displayTime, 1000); // Update the time each second
setInterval(reload, 10000); // Refresh the page with new data every 10 seconds