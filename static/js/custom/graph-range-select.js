// Trends time range select
$(document).ready(function() {
    var selects = document.getElementsByClassName('trends-range');
    // Months as M for Grafana
    var ranges = ["2h", "12h", "24h", "2d", "7d", "30d", "90d", "6M", "1y", "2y", "5y"];

    for( var i = 0; i < selects.length; i++ ) {
        for( var j in ranges ) {
            let range = ranges[j]
            const text = range.replace("h", " hours").replace("y", " year(s)").replace("d", " days").replace("M", " months")
            selects[i].options.add( new Option("Last " + text, range, false, range == "24h") );
        }
    }
})

function GraphTimeRange(name, value) {
    var graph = $("iframe#" + name);
    var url = new URL(graph.attr("src"));
    url.searchParams.set("from", "now-" + value);
    graph.attr("src", url.href);
}

function updateGraphTimeRange(selection) {
    var name = $(selection).data("graph");
    var value = selection.value;
    GraphTimeRange(name, value);
}

function updateGraphTimeRangeMul(selection, numOfGraphs) {
    var name = "";
    for ( var i = 0; i < numOfGraphs; i++){
        name = $(selection).data("graph") + i.toString();
        var value = selection.value;
        GraphTimeRange(name, value);
    }
}