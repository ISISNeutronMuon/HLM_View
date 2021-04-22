// Object Details - Devices table

var devicesData = JSON.parse(document.getElementById('devices-data').textContent);
var objDetailsURL = JSON.parse(document.getElementById('obj-details-url').textContent);

                  
$(document).ready(function() {
    var devices_table = $('#devices-table').DataTable( {
        data: devicesData,
        dataSrc: '',
        pageLength: 10,
        retrieve: true,
        order: [[1, "asc"]],
        language: {
            emptyTable: "No devices found for this coordinator."
        },
        columns: [
            { data: "id"},
            { data: "name",
            render: function(data, type, row, meta) {
                    if (type == 'display') {
                        data = '<a href="' + objDetailsURL + row.id + '">' + data + '</a>'; 
                    }
                    return data;
                }
            },
            { data: "he_value"},
            { data: "fill_percentage"},
            { data: "last_update",
            render: function(data, type, row, meta) {
                    if (type == 'display') {
                        if (!(data === null)) {
                            data = 
                            "<div>" +
                                moment($.format.date(data, "yyyy-MM-dd HH:mm:ss"), "YYYY-MM-DD HH:mm:ss").fromNow() + 
                                "<span class=\"float-right font-weight-light\">" +
                                    $.format.date(data, "MMM. d, yyyy, h:mm p");
                                "</span>" +
                            "</div>"
                        }
                    }
                    return data;
                }
            }
        ]
    })
});
