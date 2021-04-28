// Warnings to display on the building main data cards 

var buildingDataURL = JSON.parse(document.getElementById('general-data-url').textContent);

function setWarnings() {
    $.ajax({
        url: buildingDataURL,
        dataType: 'json',
        success: function(data) {
            // Stale devices
            if (data.warnings.stale_devices.length > 0) {
                // Display the stale devices warning icon
                $('#stale-devices-wrapper').toggleClass('d-none', false);

                const device_count = data.warnings.stale_devices.reduce((count, current) => count + current.length, 0);

                // Append message with number of stale devices
                $('#stale-devices-dd-menu').append(
                    '<li>' +
                    device_count +
                    ' device(s) have stale values' +
                    '</li>' +
                    '<hr class="my-2">'
                )

                
                // Append list of stale devices
                data.warnings.stale_devices.forEach(coord_devices => {
                    coord_devices.forEach(device => {
                        $('#stale-devices-dd-menu').append(
                            '<li class="font-weight-light">' +
                            device +
                            '</li>'
                        )
                    })
                })
            } else {
                $('#stale-devices-wrapper').toggleClass('d-none', true);
            }

            // Devices with no Helium Litres value
            if (data.warnings.no_value_devices.length > 0) {
                // Display the warning icon
                $('#no-value-devices-wrapper').toggleClass('d-none', false);

                const device_count = data.warnings.no_value_devices.reduce((count, current) => count + current.length, 0);

                // Append message with number of devices
                $('#no-value-devices-dd-menu').append(
                    '<li>' +
                    device_count +
                    ' device(s) have no He L value' +
                    '</li>' +
                    '<hr class="my-2">'
                )

                
                // Append list of device names
                data.warnings.no_value_devices.forEach(coord_devices => {
                    coord_devices.forEach(device => {
                        $('#no-value-devices-dd-menu').append(
                            '<li class="font-weight-light">' +
                            device +
                            '</li>'
                        )
                    })
                })
            } else {
                $('#no-value-devices-wrapper').toggleClass('d-none', true);
            }

        }
    });
}

$(document).ready(function() {
    setWarnings();
    setInterval( setWarnings, 300000 );
});
