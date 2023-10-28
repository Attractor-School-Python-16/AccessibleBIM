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
        error.response = response;
        console.log(error);
        throw error;
    }
}

async function getDataByQueryParam(url, param){
    url = url + param;
    return await makeRequest(url, "GET");
}

async function renderChart(type, name, param=7){
    let response = await getDataByQueryParam(chartUrlsByDays[name].url, param);
    if (response.error){
        $(chartUrlsByDays[name].div).text('Error occured while loading data');
    }
    else if (response.values.length===0){
        $(chartUrlsByDays[name].div).text('No data to display');
    }
    else{
        let options = createChartOptions(type, response.labels, response.values);
        window.charts[name] = new ApexCharts(chartUrlsByDays[name].div, options);
        window.charts[name].render();
    }
}

function createChartOptions(type, labels, values){
    if (type === 'area'){
        return createAreaChartOptions(labels, values);
    }
    else if (type === 'bar'){
        return createBarChartOptions(labels, values);
    }
    else if (type === 'pie'){
        return createPieChartOptions(labels, values);
    }
    else if (type === 'column'){
        return createColumnChartOptions(labels, values);
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
            categories: labels,
        },
        yaxis: {
            labels: {
                formatter: function (value){
                    let days =  Math.floor(Math.floor(value / 60) / 24);
                    let hours = Math.floor((value - days * 60 * 24)  / 60);
                    let minutes = value % 60;
                    return `${days}d. ${hours}:${minutes}`
                }
            }
        },
    };
    return options;
}

function createColumnChartOptions(labels, values){
    let options = {
        series: [{
            data: values
        }],
        chart: {
            fontFamily: 'inherit',
            type: 'bar',
        },
        xaxis: {
            categories: labels,
        },
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

let lessonsTypesInCourseChartDiv = document.getElementById('lesson-types-in-course-chart');
let stepCompletionTimeChartDiv = document.getElementById('step-completion-time-chart');
let testResultsInCourseChartDiv = document.getElementById('test-results-in-course-chart');


let chartUrlsByDays = {
    'lessonsTypesInCourseChart': {
        url: '/statistics/get-lesson-types-in-course/?course=',
        div: lessonsTypesInCourseChartDiv,
    },
    'stepCompletionTimeChart': {
        url: '/statistics/get-steps-completion-time/?course=',
        div: stepCompletionTimeChartDiv,
    },
    'testResultsInCourseChart': {
        url: '/statistics/get-test-progress-in-course/?course=',
        div: testResultsInCourseChartDiv,
    },
};

let course_id = $(lessonsTypesInCourseChartDiv).data('course');
renderChart('pie', 'lessonsTypesInCourseChart', param=course_id);
renderChart('bar', 'stepCompletionTimeChart', param=course_id);
renderChart('column', 'testResultsInCourseChart', param=course_id);