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
    if (!response.error){
        let options = createChartOptions(type, response.labels, response.values);
        window.charts[name] = new ApexCharts(chartUrlsByDays[name].div, options);
        window.charts[name].render();
    }
    else{
        $(chartUrlsByDays[name].div).text('Error occured while loading data');
    }
}

// async function updateChart(name, param){
//     let response = await getDataByQueryParam(chartUrlsByDays[name].url, param);
//     if (!response.error){
//          window.charts[name].updateOptions({
//            xaxis: {
//               categories: response.labels
//            },
//            series: [{
//               data: response.values
//            }],
//         });
//
//     }
//     else{
//         $(chartUrlsByDays[name].div).text('Error occured while loading data');
//     }
// }

// async function changeDaysOnChart(event){
//     let btn = event.currentTarget;
//     $(btn).siblings().removeClass("active");
//     $(btn).addClass( "active" );
//     let days = $(btn).data('days');
//     $.each(chartUrlsByDays, function (index){
//         if ($(btn).hasClass(this.btn_cls)){
//             chart = index;
//         }
//     })
//     await updateChart(chart, days);
// }


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

let chartUrlsByDays = {
    'lessonsTypesInCourseChart': {
        url: '/statistics/get-lesson-types-in-course/?course=',
        div: lessonsTypesInCourseChartDiv,
    },
};

let course_id = $(lessonsTypesInCourseChartDiv).data('course');
renderChart('pie', 'lessonsTypesInCourseChart', param=course_id);