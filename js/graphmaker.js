google.charts.load('current', {
    'packages': ['corechart']
});

function scraper(file) {
    d3.csv(file).then(makeChart);
}

function makeChart(rawData) {
    var arr = [
        ["University", "Paid fee", "Average scholarship per student", "Percentage of international student"]
    ];

    rawData.forEach(function (el) {
        arr.push([el.uni, parseFloat(el.paidfee), parseFloat(el.relative_scholarship), parseFloat(el.perc_intern)])
    });

    var data = google.visualization.arrayToDataTable(arr);

    var options = {
        title: 'Correlation among fees and scholarships with rate of international students in Italian university',
        hAxis: {
            title: 'University'
        },
        seriesType: 'bars',
        vAxes: {
            0: {
                logScale: false,
                title: 'Spent amount of € per students (fees, scholarships)',
                gridlines: {
                    color: 'transparent'
                }
            },
            1: {
                logScale: false,
                maxValue: 45,
                gridlines: {
                    color: 'transparent'
                },
                title: '% of students'
            }
        },
        series: {
            0: {
                targetAxisIndex: 0
            },
            1: {
                targetAxisIndex: 0
            },
            2: {
                targetAxisIndex: 1,
                type: 'line'
            }
        }
    };

    var chart = new google.visualization.ComboChart(document.getElementById('myChart'));
    chart.draw(data, options);
}