function updateCurrentDateTime() {
    let date = $.format.date(Date.now(), "yyyy-MM-dd HH:mm:ss");
    $("span#current-time").text(date);
}

updateCurrentDateTime();
setInterval(updateCurrentDateTime, 1000);
