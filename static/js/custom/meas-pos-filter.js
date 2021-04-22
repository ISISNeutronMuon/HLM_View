// Measurements table - filter by position select

var displayGroupsURL = JSON.parse(document.getElementById('display-groups-url').textContent);


// Populate object position (display group) filter select options
$(document).ready(function() {
    $.ajax({
        url: displayGroupsURL,
        dataType: 'json',
        complete: function(data) {
            var displayGroups = data.responseJSON;
            displayGroups.unshift({"dg_name": "All"});
            $.each(displayGroups, function(key, displayGroup) {
                var option = new Option(displayGroup.dg_name, displayGroup.dg_name);
                $("#select-position-filter").append(option);
            });
        }
    });
});

function filterByPosition(selection) {
    var table = $('#objects-table').DataTable();
    // Update if columns change
    table.columns( 5 ).search( selection.value != "All" ? selection.value : '' ).draw();
}
