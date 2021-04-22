var hpsDataURL = JSON.parse(document.getElementById('hps-data-url').textContent);
var objDetailURL = JSON.parse(document.getElementById('obj-detail-url').textContent);

$(document).ready(function() {
    var table = $('#mcps-table').DataTable( {
        pageLength: 10,
        lengthMenu: [10, 15, 20, 25, 50, 100],
        retrieve: true,
        ajax: {
            url: hpsDataURL,
            type: 'GET',
            dataSrc: 'mcps'
        },
        columnDefs: [
            {
                targets: 4,
                render: function(data, type, row, meta) {
                    if (type == 'display') {
                        if (!(data === null)) {
                            data = $.format.date(data, "MMM. d, yyyy, h:mm p");
                        }
                    }
                    return data;
                }
            },
            {
                targets: 3,
                render: function(data, type, row, meta) {
                    if (type == 'display') {
                        if (data !== null) {
                            data = data + '<span class="font-weight-light text-muted float-right mr-2"> mbar </span>'
                        }
                    }
                    return data;
                }
            },
            {
                targets: 1,
                render: function(data, type, row, meta) {
                    if (type == 'display') {
                        data = '<a href="' + objDetailURL + row.ob_id + '">' + data + '</a>'; 
                    }
                    return data;
                }
            }
        ],
        columns: [
            {"data": "ob_id"},
            {"data": "ob_name"},
            {"data": "dg_name"},
            {"data": "mea_values.0"},
            {"data": "mea_date"}
        ],
        initComplete: function() {
            $("#mcps-table").width("100%");
        }
    });

    setInterval( function () {
        table.ajax.reload( null, false );
    }, 300000 );
});