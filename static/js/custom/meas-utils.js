//  Utilities for the Measurements DataTable

// Dropdown menus
$(".checkbox-menu").on("change", "input[type='checkbox']", function() {
    $(this).closest("li").toggleClass("active", this.checked);
});

// to prevent function repeatedly being called on button spam
let locked = false;
function unlock () {
    locked = false;
    if ($("button#reload-data-btn").is(":disabled")) {
        $("button#reload-data-btn").prop("disabled", false);
    }
}

function reloadDataButtonClick() {
    if (!locked) {
        locked = true;
        $("button#reload-data-btn").prop("disabled", true);
        setTimeout(unlock, 5000);
        ajaxReload();
    }
}

function ajaxReload () {
    let table = $('#objects-table').DataTable();
        table.ajax.reload(function() {
            refreshLastUpdatedDate();
        }, false );
}

function refreshLastUpdatedDate() {
    let date = $.format.date(Date.now(), "yyyy-MM-dd HH:mm:ss");
    $("span#last-updated").text(date);
}

function resetTableButtonClick() {
    let table = $('#objects-table').DataTable();
    table.state.clear();
    location.reload();
}
