const buildingId = JSON.parse(document.getElementById('building-id').textContent);
var generalDataURL = JSON.parse(document.getElementById('general-data-url').textContent);
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
            url: generalDataURL,
            type: 'GET',
            dataSrc: buildingId + '.coordinators'
        },
        columns: [
            {"data": "id"},
            {"data": "name",
            "render": function(data, type, row, meta) {
                if (type == 'display') {
                    data = '<a href="' + objDetailsURL + row.id + '">' + data + '</a>'; 
                }
                return data;
            }
            },
            {"data": "he_total"},
            {"data": "devices.length"}
        ],
        columnDefs: [
            {
                targets: 1,
                className: "coord-name",

            },
            {
                targets: 3,
                render: function(data, type, row, meta) {
                    if (type == 'display') {
                        if (data !== null && row.devices.length > 0) {
                            data = 
                                '<div class="show-devices cursor-pointer">' + 
                                    data + 
                                    '<span class="float-right px-3">' + 
                                        '<i class="bi bi-zoom-in"></i>' +
                                    '</span>' +
                                '</div>';
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
                    { data: "id", title: "Device ID"},
                    { data: "name", title: "Device Name",
                    render: function(data, type, row, meta) {
                            if (type == 'display') {
                                data = '<a href="' + objDetailsURL + row.id + '">' + data + '</a>'; 
                            }
                            return data;
                        }
                    },
                    { data: "he_value", title: "Helium L"},
                    { data: "fill_percentage", title: "Fill %"},
                    { data: "last_update", title: "Last Update",
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
            });
            
            $("i", this).toggleClass("bi bi-zoom-in bi-zoom-out");
        }
    } );

    setInterval( function () {
        table.ajax.reload( null, false );
    }, 300000 );
});
