google.charts.load('current', {
    'packages': ['line']
});

function linedata(file) {
    d3.csv(file).then(drawChart);
}

function drawChart(rawData) {
    var givenForm = document.getElementById("timelinechart")
    var chosenUni = givenForm.value;
    var labelUni = givenForm.options[givenForm.selectedIndex].text;
    
    var arr = [
        [
            "Academic year",
            "Scholarship",
            "Fee",
            "International students"
        ]
    ]

    rawData.forEach(function (el) {
        if (el.uni == chosenUni) {
            arr.push([
                "2016", 
                parseFloat(el.scholarship16), 
                parseFloat(el.paidfees16),
                parseFloat(el.intstuds16)
            ]);   
            arr.push([
                "2017", 
                parseFloat(el.scholarship17), 
                parseFloat(el.paidfees17),
                parseFloat(el.intstuds17)
            ]);
            arr.push([
                "2018", 
                parseFloat(el.scholarship18), 
                parseFloat(el.paidfees18),
                parseFloat(el.intstuds18)
            ]);     
            arr.push([
                "2019", 
                parseFloat(el.scholarship19), 
                parseFloat(el.paidfees19),
                parseFloat(el.intstuds19)
            ]);     
        }
    });

    var data = google.visualization.arrayToDataTable(arr);

    var options = {
/*        chart: {
            title: 'Average Temperatures and Daylight in Iceland Throughout the Year',
            subtitle: 'Selected university: ' + labelUni
        },
*/
        title: 'Average Temperatures and Daylight in Iceland Throughout the Year',
        subtitle: 'Selected university: ' + labelUni,
        width: 900,
        height: 500,
        series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 0},
            2: {targetAxisIndex: 1}
        },
        vAxes: {
            // Adds titles to each axis.
            0: {
                title: 'Average expenditure (fee/scholarship)',
                gridlines: {
                    color: 'transparent'
                }
            },
            1: {
                title: '% of international students',
                gridlines: {
                    color: 'transparent'
                }
            }
        },
    };

    var chart = new google.visualization.LineChart(document.getElementById('linechart_material'));

    chart.draw(data, google.charts.Line.convertOptions(options));
}