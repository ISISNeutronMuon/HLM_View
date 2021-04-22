// Measurements table Column Display dropdown

// Populate column display dropdown
$(document).ready(function() {
    let columns = [
        ["Object ID", "checked disabled"],
        ["Object Name", "checked"],
        ["Object Type", ""],
        ["Object Class", "checked"],
        ["Object Comment", ""],
        ["Position", "checked"],
        ["Position Information", ""],
        ["Measurement 1", "checked"],
        ["Measurement 2", "checked"],
        ["Measurement 3", "checked"],
        ["Measurement 4", "checked"],
        ["Measurement 5", "checked"],
        ["Last Update", "checked"]
    ]
    $.each(columns, function(i, col) {
        $("#columns-display").append(
            '<li><label>'
            + '<input type="checkbox" class="col-toggle-vis" data-column="' + i + '"' + col[1] + '>' + col[0]
            + '</label></li>'
        )
    })
})

$('#columns-display').on('change', 'input', function (e) {
    e.preventDefault();

    var table = $('#objects-table').DataTable();

    // Get the column API object
    var column = table.column( $(this).attr('data-column') );

    // Toggle the visibility
    column.visible( this.checked );
    $("#objects-table").width("100%");
});
