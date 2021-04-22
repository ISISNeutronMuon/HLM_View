// Building main data cards

var generalDataURL = JSON.parse(document.getElementById('general-data-url').textContent);


function updateValues() {
    $.ajax({
        url: generalDataURL,
        dataType: 'json',
        success: function(data) {
            const buildingId = JSON.parse(document.getElementById('building-id').textContent);
            data = data[buildingId]
            $("#he-transport").text(data["he_total"]);
            $("#oxygen-level").text(data["oxygen"]);
            $("#purity-level").text(data["purity"]);
        }
    });
}

updateValues();
setInterval( updateValues, 300000 ); // 5 min
