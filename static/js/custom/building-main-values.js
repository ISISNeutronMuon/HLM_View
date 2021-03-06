// Building main data cards

var buildingDataURL = JSON.parse(document.getElementById('general-data-url').textContent);

$(document).ready(function() {
    function updateValues() {
        $.ajax({
            url: buildingDataURL,
            dataType: 'json',
            success: function(data) {
                $("#he-transport").text(data["he_total"]);
                $("#oxygen-level").text(data["oxygen"]);
                $("#purity-level").text(data["purity"]);
            }
        });
    }

    updateValues();
    setInterval( updateValues, 300000 ); // 5 min
})