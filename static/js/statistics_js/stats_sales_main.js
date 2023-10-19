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

async function renderChart(type, name){
    chartUrlsByDays[name].url
    let response = await getDataByDay(chartUrlsByDays[name].url, 7);
    if (!response.error){
        let options = createChartOptions(type, response.labels, response.values);
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


function createChartOptions(type, labels, values){
    if (type === 'area'){
        return createAreaChartOptions(labels, values)
    }
    else if (type === 'bar'){
        return createBarChartOptions(labels, values)
    }
}

function createAreaChartOptions(labels, values){
    let options = {
        series: [{
            name: 'Новых пользователей',
            data: values
        }],
        chart: {
            fontFamily: 'inherit',
            type: 'area',
        },
        xaxis: {
            type: 'datetime',
            categories: labels,
            labels: {
                format: 'dd.MM',
            },
        },
    };
    return options;
}

function createBarChartOptions(labels, values){
    let options = {
        series: [{
            data: values
        }],
        chart: {
            fontFamily: 'inherit',
            type: 'bar',
        },
        xaxis: {
            categories: labels
        },
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


renderChart('area', 'newSubscriptionsChart');
let newSubscriptionButtons = $('.new-subscriptions-chart-btn')
newSubscriptionButtons.click(changeDaysOnChart)

renderChart('bar', 'popularCoursesChart');
let popularCoursesButtons = $('.popular-courses-chart-btn')
popularCoursesButtons.click(changeDaysOnChart)