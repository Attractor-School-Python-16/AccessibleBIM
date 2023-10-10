window.charts = {}

async function makeRequest(url, method){
    let response = await fetch(url, {
        "method": method,
        mode: 'same-origin',
    });
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.statusText);
        error.response = response
        console.log(error)
        throw error;
    }
}

async function getNewUsersQty(days){
    let url = '/statistics/get-new-users-qty/?days=' + days;
    let response = await makeRequest(url, "GET");
    console.log('response is ready')
    console.log(response);
    return response;
}

async function renderChart(){
    let response = await getNewUsersQty(30);
    if (!response.error){
        console.log('make options')
        let options = createChartOptions(response.labels, response.values);
        window.charts.newUsersChart = new ApexCharts(newUsersChartDiv, options);
        window.charts.newUsersChart.render();
    }
    else{
        $(newUsersChartDiv).text('Error occured while loading data');
    }
}

async function updateNewUsersChart(days){
    let response = await getNewUsersQty(days)
    if (!response.error){
        // chart.updateSeries();
         window.charts.newUsersChart.updateOptions({
           xaxis: {
              categories: response.labels
           },
           series: [{
              data: response.values
           }],
        });

    }
    else{
        $(newUsersChartDiv).text('Error occured while loading data')
    }
}

async function newUsersWeekOnClick(){
    await updateNewUsersChart(7)
}

async function newUsersMonthOnClick(){
    await updateNewUsersChart(30)
}

function createChartOptions(labels, values){
    let options = {
        series: [{
            name: 'Новых пользователей',
            data: values
        }],
        chart: {
            fontFamily: 'inherit',
            type: 'area',
            // height: 300px,
            toolbar: {
                show: false
            }
        },
        plotOptions: {

        },
        legend: {
            show: false
        },
        dataLabels: {
            enabled: false
        },
        fill: {
            type: 'solid',
            opacity: 1
        },
        stroke: {
            curve: 'smooth',
            show: true,
            width: 3,
            // colors: [baseColor]
        },
        xaxis: {
            type: 'datetime',
            categories: labels,
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false
            },
            labels: {
                format: 'dd.MM',
                style: {
                    // colors: labelColor,
                    fontSize: '12px'
                }
            },
            crosshairs: {
                position: 'front',
                stroke: {
                    // color: baseColor,
                    width: 1,
                    dashArray: 3
                }
            },
            tooltip: {
                enabled: true,
                formatter: undefined,
                offsetY: 0,
                style: {
                    fontSize: '12px'
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    // colors: labelColor,
                    fontSize: '12px'
                }
            }
        },
        states: {
            normal: {
                filter: {
                    type: 'none',
                    value: 0
                }
            },
            hover: {
                filter: {
                    type: 'none',
                    value: 0
                }
            },
            active: {
                allowMultipleDataPointsSelection: false,
                filter: {
                    type: 'none',
                    value: 0
                }
            }
        },
        // tooltip: {
        //     style: {
        //         fontSize: '12px'
        //     },
        //     y: {
        //         formatter: function (val) {
        //             return '$' + val + ' thousands'
        //         }
        //     }
        // },
        // colors: [lightColor],
        grid: {
            // borderColor: borderColor,
            strokeDashArray: 4,
            yaxis: {
                lines: {
                    show: true
                }
            }
        },
        markers: {
            // strokeColor: baseColor,
            strokeWidth: 3
        }
    };
    return options;
}

let newUsersChartDiv = document.getElementById('new-users-chart');
renderChart()
$('#new-users-chart-week').on('click', newUsersWeekOnClick);
$('#new-users-chart-month').on('click', newUsersMonthOnClick);