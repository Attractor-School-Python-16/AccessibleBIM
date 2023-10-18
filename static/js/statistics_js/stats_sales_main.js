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

async function getDataByDay(url, days){
    url = url + days;
    return await makeRequest(url, "GET");
}

async function renderChart(name){
    chartUrlsByDays[name].url
    let response = await getDataByDay(chartUrlsByDays[name].url, 7);
    if (!response.error){
        let options = createChartOptions(response.labels, response.values);
        window.charts[name] = new ApexCharts(chartUrlsByDays[name].div, options);
        window.charts[name].render();
    }
    else{
        $(chartUrlsByDays[name].div).text('Error occured while loading data');
    }
}

async function updateChart(name, days){
    let response = await getDataByDay(chartUrlsByDays[name].url, days)
    if (!response.error){
         window.charts[name].updateOptions({
           xaxis: {
              categories: response.labels
           },
           series: [{
              data: response.values
           }],
        });

    }
    else{
        $(chartUrlsByDays[name].div).text('Error occured while loading data')
    }
}

async function changeDaysOnChart(event){
    let btn = event.currentTarget;
    $(btn).siblings().removeClass("active");
    $(btn).addClass( "active" );
    let days = $(btn).data('days')
    await updateChart('newSubscriptionsChart', days)
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
let popularCoursesChartDiv = document.getElementById('popular-courses-chart');

let chartUrlsByDays = {
    'newSubscriptionsChart': {
        url: '/statistics/get-new-subscriptions-qty/?days=',
        div: newSubscriptionsChartDiv,
    },
    'popularCoursesChart': {
        url: '/statistics/get-popular-courses/?days=',
        div: popularCoursesChartDiv,
    }
}


renderChart('newSubscriptionsChart');
let newSubscriptionButtons = $('.new-subscriptions-chart-btn')
newSubscriptionButtons.click(changeDaysOnChart)