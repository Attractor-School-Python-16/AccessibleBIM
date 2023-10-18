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

async function getNewSubscriptionsQty(days){
    console.log('getNewSubscriptionsQty start')
    let url = '/statistics/get-new-subscriptions-qty/?days=' + days;
    let response = await makeRequest(url, "GET");
    console.log('getNewSubscriptionsQty response', response)
    return response;
}

async function renderChart(){
    console.log('renderChart start')
    let response = await getNewSubscriptionsQty(7);
    console.log('renderChart response', response)
    if (!response.error){
        let options = createChartOptions(response.labels, response.values);
        window.charts.newSubscriptionsChart = new ApexCharts(newSubscriptionsChartDiv, options);
        window.charts.newSubscriptionsChart.render();
    }
    else{
        $(stepsCompletedChartDiv).text('Error occured while loading data');
    }
}

async function updateNewSubscriptionsChart(days){
    let response = await getNewSubscriptionsQty(days)
    if (!response.error){
         window.charts.newSubscriptionsChart.updateOptions({
           xaxis: {
              categories: response.labels
           },
           series: [{
              data: response.values
           }],
        });

    }
    else{
        $(newSubscriptionsChartDiv).text('Error occured while loading data')
    }
}

async function newSubscriptionsWeekOnClick(event){
    let btn = event.currentTarget;
    $(btn).addClass( "active" );
    $('#new-subscriptions-chart-month').removeClass("active");
    $('#new-subscriptions-chart-half-year').removeClass("active");
    await updateNewSubscriptionsChart(7)
}

async function newSubscriptionsMonthOnClick(event){
    let btn = event.currentTarget;
    $(btn).addClass( "active" );
    $('#new-subscriptions-chart-week').removeClass("active");
    $('#new-subscriptions-chart-half-year').removeClass("active");
    await updateNewSubscriptionsChart(30)
}

async function newSubscriptionsHalfYearOnClick(event){
    let btn = event.currentTarget;
    $(btn).addClass( "active" );
    $('#new-subscriptions-chart-week').removeClass("active");
    $('#new-subscriptions-chart-month').removeClass("active");
    await updateNewSubscriptionsChart(180)
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

let newSubscriptionsChartDiv = document.getElementById('new-subscriptions-chart');
renderChart()
$('#new-subscriptions-chart-week').on('click', newSubscriptionsWeekOnClick);
$('#new-subscriptions-chart-month').on('click', newSubscriptionsMonthOnClick);
$('#new-subscriptions-chart-half-year').on('click', newSubscriptionsHalfYearOnClick);