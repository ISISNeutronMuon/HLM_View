const buildingId = JSON.parse(document.getElementById('building-id').textContent);
var buildingDataURL = JSON.parse(document.getElementById('general-data-url').textContent);
var objDetailsURL = JSON.parse(document.getElementById('obj-details-url').textContent);


/* Formatting function for row details (nested table) */
function format ( rowData ) {
    // `rowData` is the original data object for the row
    return  '<table id="' + rowData.id + '" class="table table-bordered table-hover table-sm mx-auto" style="width: 90%;">'+
            '</table>';   
}

$(document).ready(function() {
    var table = $('#coordinators-table').DataTable( {
        retrieve: true,
        searching: false,
        paging: false,
        info: false,
        order: [[1, "asc"]],
        language: {
            emptyTable: "No coordinators found for " + buildingId
        },
        ajax: {
            url: buildingDataURL,
            type: 'GET',
            dataSrc: 'coordinators'
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "he_total"},
            {"data": "devices.length" }
        ],
        columnDefs: [
            {
                targets: 1,
                className: "coord-name",
                render: function(data, type, row, meta) {
                    if (type == 'display') {
                        data = '<a href="' + objDetailsURL + row.id + '">' + data + '</a>'; 
                    }
                    return data;
                }

            },
            {
                targets: 3,
                render: function(data, type, row, meta) {
                    if (type == 'display') {
                        if (data !== null) {
                            const stale_warning = function() {
                                if (row.warnings.stale_devices.length > 0) {
                                    return '<span class="text-warning mx-2">' + 
                                                row.warnings.stale_devices.length + ' stale' +
                                            '</span>'
                                }
                                return ''
                            }

                            const no_value_warning = function() {
                                if (row.warnings.no_value_devices.length > 0) {
                                    return  '<span class="text-danger mx-2">' + 
                                                row.warnings.no_value_devices.length + ' He L N/A' +
                                            '</span>'
                                }
                                return ''
                            }

                            // If coordinator has devices connected to it, enable nested table display of connected devices
                            // and check for warnings
                            if (row.devices.length > 0) {
                                data = 
                                '<div class="show-devices cursor-pointer d-flex">' + 
                                    '<span class="float-left">' + 
                                        row.devices.length + 
                                    '</span>' +
                                    '<div class="ml-auto">' +
                                        '<div class="mr-4 d-inline">' +
                                            stale_warning() +
                                            no_value_warning() + 
                                        '</div>' +
                                        '<span class="mr-3">' + 
                                            '<i class="bi bi-zoom-in"></i>' +
                                        '</span>' +
                                    '</div>' +
                                '</div>';
                            } else {
                                data = row.devices.length
                            }

                        }
                    }
                    return data;
                }
            }
        ],
        initComplete: function() {
            $("#objects-table").width("100%");
        }
    });

    // Add event listener for opening and closing coordinator devices
    $('#coordinators-table tbody').on('click', '.show-devices', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var rowData = row.data();
        var coordinatorName = $(tr).find("td.coord-name")

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            $("i", this).toggleClass("bi bi-zoom-in bi-zoom-out");

            coordinatorName.removeClass("font-weight-bold");

            // Destroy the nested datatable
            $('#' + rowData.id).DataTable().destroy();
        }
        else {
            // Open this row
            row.child( format(rowData) ).show();

            coordinatorName.addClass("font-weight-bold");

            // Create the nested datatable for devices
            $( '#' + rowData.id ).DataTable( {
                data: rowData.devices,
                dataSrc: '',
                retrieve: true,
                searching: false,
                paging: false,
                info: false,
                order: [[1, "asc"]],
                language: {
                    emptyTable: "No devices found for this coordinator."
                },
                columns: [
                    { data: "id", title: "Device ID" },
                    { data: "name", title: "Device Name" },
                    { data: "he_value", title: "Helium (L)" },
                    { data: "fill_percentage", title: "Fill (%)" },
                    { data: "last_update", title: "Last Update" }
                ],
                columnDefs: [
                    {
                        targets: 1,
                        render: function(data, type, row, meta) {
                            if (type == 'display') {
                                data = '<a href="' + objDetailsURL + row.id + '">' + data + '</a>'; 
                            }
                            return data;
                        }
                    },
                    {
                        targets: 2,
                        render: function(data, type, row, meta) {
                            if (type == 'display') {
                                if (data === "N/A") {
                                    data = '<span class="text-danger">' + data + '</span>';
                                }
                            }
                            return data;
                        }
                    },
                    {
                        targets: 4,
                        render: function(data, type, row, meta) {
                            if (type == 'display') {
                                if (!(data === null)) {
                                    let relative_time = moment($.format.date(data, "yyyy-MM-dd HH:mm:ss"), "YYYY-MM-DD HH:mm:ss").fromNow()

                                    if (row.warnings.is_stale == true) {
                                        relative_time = relative_time + '<span class="text-warning"> stale</span>';
                                    }
                                    
                                    data = 
                                    "<div>" +
                                        relative_time +
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
            });
            
            $("i", this).toggleClass("bi bi-zoom-in bi-zoom-out");
        }
    } );

    setInterval( function () {
        table.ajax.reload( null, false );
    }, 300000 );
});
