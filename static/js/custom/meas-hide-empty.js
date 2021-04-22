// Checkbox "Hide empty measurements"

function hideEmptyMeasurements(cb) {
    var table = $('#objects-table').DataTable();
    if(cb.checked){
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                const isNull = (value) => value === null;
                const rowData = table.row(dataIndex).data();
                return !rowData.mea_values.every(isNull);
            });
    } else {
        $.fn.dataTable.ext.search.pop();
    }
    table.draw();
}
