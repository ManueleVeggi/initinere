google.charts.load('current', {
    'packages': ['corechart']
});

function getdata() {
    var file = document.getElementById("ayear").elements["ayear"].value;
    d3.csv(file).then(makeChart1);
}

function makeChart1(rawData) {
    var xaxis = document.getElementById("xAxis").elements["x"].value;
    var yaxis = document.getElementById("yAxis").elements["y"].value;

    if (xaxis == yaxis) {
        alert("Same value in x and y axis: please choose a more informative visualization!")
    }

    function assignLabel(value){
        var label;
        if (value == "paidfee") {
            label = "Paid fee";
        } else if (value == "relative_scholarship") {
            label = "Average scholarship per student";
        } else if (value == "perc_intern") {
            label = "% of international students"
        }
        return label
    }

    var labelx = assignLabel(xaxis);
    var labely = assignLabel(yaxis);

    var arr = [[labelx, labely, {role: 'tooltip'}]];

    rawData.forEach(function (el) {
        arr.push([parseFloat(el[xaxis]), parseFloat(el[yaxis]), el.uni])
    });

    var data = google.visualization.arrayToDataTable(arr);

    var options = {
        hAxis: {title: labelx},
        vAxis: {title: labely},
        legend: 'none'
      };

      var chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));

      chart.draw(data, options);
    }