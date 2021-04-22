// Measurements table - Object Class filter dropdown

var classListURL = JSON.parse(document.getElementById('obj-class-list-url').textContent);


$(document).ready(function() {
    $.ajax({
        url: classListURL,
        dataType: 'json',
        complete: function(data) {
            const objectClasses = data.responseJSON;
            $.each(objectClasses, function(i, obj_class) {
                $("#obj-class-display").append(
                    '<li><label>'
                    + '<input type="checkbox" class="obj-class-filter" data-val="' + obj_class.oc_name + '" checked>' + obj_class.oc_name
                    + '</label></li>'
                )
            })
        }
    });
});

function applyClassFilter() {
    var table = $('#objects-table').DataTable();

    var checkedClasses = [];
    $('#obj-class-display .obj-class-filter').each(function() {
        if ( $(this).is(':checked') ) {
            checkedClasses.push( $(this).attr('data-val') );
        }
    })

    // If none are checked, show nothing, instead of "no search"
    // Update if columns change
    if ( checkedClasses.length == 0) {
        table.column( 3 ).search( false ).draw();
    } else {
        table.column( 3 ).search( checkedClasses.join('|'), true, false, true ).draw();
    }
}

$('#obj-class-display').on('change', 'input', function (e) {
    e.preventDefault();
    applyClassFilter();
});

function objClassSelectAll(select) {
    $("#obj-class-display .obj-class-filter").each(function() {
        $(this).prop("checked", select);
    });
    applyClassFilter();
}
