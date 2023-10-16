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

async function getStepsCompletedQty(days){
    let url = '/statistics/get-steps-completed-qty/?days=' + days;
    let response = await makeRequest(url, "GET");
    return response;
}

async function getLessonTypesStats(){
    let url = '/statistics/get-lesson-types/';
    let response = await makeRequest(url, "GET");
    return response;
}

async function renderChart(){
    let response = await getStepsCompletedQty(7);
    if (!response.error){
        let options = createChartOptions(response.labels, response.values);
        window.charts.stepsCompletedChart = new ApexCharts(stepsCompletedChartDiv, options);
        window.charts.stepsCompletedChart.render();
    }
    else{
        $(stepsCompletedChartDiv).text('Error occured while loading data');
    }
}

async function renderPieChart(){
    let response = await getLessonTypesStats();
    if (!response.error){
        let options = createPieChartOptions(response.labels, response.values);
        window.charts.lessonTypesChart = new ApexCharts(lessonTypesChartDiv, options);
        window.charts.lessonTypesChart.render();
    }
    else{
        $(lessonTypesChartDiv).text('Error occured while loading data');
    }
}

async function updateStepsCompletedChart(days){
    let response = await getStepsCompletedQty(days)
    if (!response.error){
         window.charts.stepsCompletedChart.updateOptions({
           xaxis: {
              categories: response.labels
           },
           series: [{
              data: response.values
           }],
        });

    }
    else{
        $(stepsCompletedChartDiv).text('Error occured while loading data')
    }
}

async function stepsCompletedWeekOnClick(event){
    let btn = event.currentTarget;
    $(btn).addClass( "active" );
    $('#steps-completed-chart-month').removeClass("active");
    $('#steps-completed-chart-half-year').removeClass("active");
    await updateStepsCompletedChart(7)
}

async function stepsCompletedMonthOnClick(event){
    let btn = event.currentTarget;
    $(btn).addClass( "active" );
    $('#steps-completed-chart-week').removeClass("active");
    $('#steps-completed-chart-half-year').removeClass("active");
    await updateStepsCompletedChart(30)
}

async function stepsCompletedHalfYearOnClick(event){
    let btn = event.currentTarget;
    $(btn).addClass( "active" );
    $('#steps-completed-chart-week').removeClass("active");
    $('#steps-completed-chart-month').removeClass("active");
    await updateStepsCompletedChart(180)
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

function createPieChartOptions(labels, values){
    let options = {
        series: values,
        labels: labels,
        chart: {
            fontFamily: 'inherit',
            type: 'donut',
        },
    };
    return options;
}

let stepsCompletedChartDiv = document.getElementById('steps-completed-chart');
let lessonTypesChartDiv = document.getElementById('lesson-types-chart');
renderChart()
renderPieChart()
$('#steps-completed-chart-week').on('click', stepsCompletedWeekOnClick);
$('#steps-completed-chart-month').on('click', stepsCompletedMonthOnClick);
$('#steps-completed-chart-half-year').on('click', stepsCompletedHalfYearOnClick);