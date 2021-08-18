var meaTypesURL = JSON.parse(document.getElementById('mea-types-url').textContent);
var objectsDataURL = JSON.parse(document.getElementById('objects-data-url').textContent);
var objDetailURL = JSON.parse(document.getElementById('obj-details-url').textContent);

$(document).ready(function() {
    $.ajax({
        url: meaTypesURL,
        dataType: 'json',
        complete: function(data) {
            var mea_types = data.responseJSON;

            let hideEmptyMeasChecked = false;  // for saving state of custom filter
            var table = $('#objects-table').DataTable( {
                pageLength: 25,
                lengthMenu: [10, 25, 50, 100, 150, 200, 250],
                retrieve: true,
                stateSave: true,
                ajax: {
                    url: objectsDataURL,
                    type: 'GET',
                    dataSrc: ''
                },
                columnDefs: [
                    {
                        targets: [7, 8, 9, 10, 11],
                        defaultContent: '',
                        render: function(data, type, row, meta) {
                            
                            if (type == 'display') {
                                if (!(mea_types === undefined) && !(data === null) && !(data === "None")) {
                                    // Update "meta.col - 3" if targets change
                                    const mea_type = mea_types[row.ob_type][meta.col - 7];                                                               
                                    if (typeof(data)==="string"&& data.includes("\t")){
                                        const data_and_change = data.split("\t");
                                        if(data_and_change[1].includes("+0.00%") ||data_and_change[1].includes("N/A")){
                                            var font_color = "blue";
                                            if(data_and_change[2].includes("+0.00")){
                                                var second_font_color = "blue"
                                            }else if (data_and_change[2].includes("+")){
                                                second_font_color = "green"
                                            }else{
                                                second_font_color = "red"
                                            }
                                        }else if (data_and_change[1].includes("+")){
                                             font_color = "green";
                                             second_font_color = font_color
                                        }else{
                                            font_color = "red";
                                            second_font_color = font_color
                                        }
                                        data = '<span>' + (mea_type !== null ? mea_type : 'N/A') + '</span>'  + data_and_change[0] + "<span style='float: right'>" +data_and_change[1].fontcolor(font_color)+"<\span>"+ "<span style='float: right'>" +data_and_change[2].fontcolor(second_font_color)+"<\span>";
                                    } else {
                                        data = '<span>' + (mea_type !== null ? mea_type : 'N/A') + '</span>'  + data;
                                    }
                                }
                            }
                            return data;
                        }

                    },

                    {
                        targets: [2, 4, 6],
                        visible: false
                    }
                ],
                columns: [
                    {"data": "ob_id"},
                    {"data": "ob_name",
                    "render": function(data, type, row, meta) {
                        if (type == 'display') {
                            data = '<a href="' + objDetailURL + row.ob_id + '">' + data + '</a>'; 
                        }
                        return data;
                    }
                    },
                    {"data": "ob_type_name"},
                    {"data": "ob_class_name"},
                    {"data": "ob_comment"},
                    {"data": "dg_name"},
                    {"data": "ob_posinformation"},
                    {"data": "mea_values.0"},
                    {"data": "mea_values.1"},
                    {"data": "mea_values.2"},
                    {"data": "mea_values.3"},
                    {"data": "mea_values.4"},
                    {"data": "mea_date",
                    "render": function(data, type, row, meta) {
                        if (type == 'display') {
                            if (!(data === null)) {
                                data = $.format.date(data, "MMM. d, yyyy, h:mm p");
                            }
                        }
                        return data;
                    }}
                ],
                stateSaveParams: function(settings, data) {
                    data.emptyMeasHidden = $('input#cb-hide-empty-meas').is(':checked');
                    data.positionSelect = $('select#select-position-filter').val();
                    
                    data.objectClassDropdown = {}
                    $('ul#obj-class-display .obj-class-filter').each( function() {
                        const objectClass = $(this).attr('data-val');
                        data.objectClassDropdown[ objectClass ] = $(this).is(':checked');
                    });

                    data.columnDisplayDropdown = {}
                    $('ul#columns-display .col-toggle-vis').each( function() {
                        const column = $(this).attr('data-column');
                        data.columnDisplayDropdown[ column ] = $(this).is(':checked');
                    });

                },
                stateLoadParams: function(settings, data) {
                    if (data.emptyMeasHidden !== undefined) { 
                        $('input#cb-hide-empty-meas').prop('checked', data.emptyMeasHidden) 
                        hideEmptyMeasChecked = data.emptyMeasHidden;  // update custom filter state (used in initComplete)
                    }
                    if (data.positionSelect !== undefined) { 
                        $('select#select-position-filter').val(data.positionSelect) 
                    }
                    if (data.objectClassDropdown !== undefined) {
                        let dict = data.objectClassDropdown
                        for (let objectClass in dict) {
                            let checked = dict[objectClass];
                            $('ul#obj-class-display .obj-class-filter[data-val="' + objectClass + '"]').prop('checked', checked);
                        }
                    }
                    if (data.columnDisplayDropdown !== undefined) {
                        let dict = data.columnDisplayDropdown
                        for (let column in dict) {
                            let checked = dict[column];
                            $('ul#columns-display .col-toggle-vis[data-column="' + column + '"]').prop('checked', checked);
                        }
                    }
                },
                initComplete: function() {
                    $("#objects-table").width("100%");
                    refreshLastUpdatedDate();

                    if (hideEmptyMeasChecked) {
                        hideEmptyMeasurements($('input#cb-hide-empty-meas')[0]);   
                    }
                }
            });

            // update table data every few mins (100000 = 100s)
            setInterval(ajaxReload, 300000 );
        }
    });
} );
