function scraper(file) {
    d3.csv(file).then(makeChart);

    // Plot the data with Chart.js
    function makeChart(data) {
        var yearLabels = data.map(function (d) {
            return d.uni;
        });
        var countData = data.map(function (d) {
            return d.paidfee;
        });

        var chart = new Chart("myChart", {
            type: "bar",
            data: {
                labels: yearLabels,
                datasets: [{
                    label: "Paid fees",
                    data: countData,
                    backgroundColor: 'rgb(255, 99, 132)',
                }]
            }
        });
    }
}