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

async function getDataByQueryParam(url, param=''){
    url = url + param;
    return await makeRequest(url, "GET");
}

async function renderChart(name, param){
    let response = await getDataByQueryParam(chartUrlsByDays[name].url, param);
    if (response.error){
        $(chartUrlsByDays[name].div).text('Error occured while loading data');
    }
    else if (response.values.length===0){
        $(chartUrlsByDays[name].div).text('No data to display');
    }
    else{
        let options = createChartOptions(chartUrlsByDays[name].type, response.labels, response.values,
            chartUrlsByDays[name].title);
        options = modifyOptions(options, chartUrlsByDays[name]);
        window.charts[name] = new ApexCharts(chartUrlsByDays[name].div, options);
        window.charts[name].render();
    }
}

async function updateChart(name, days){
    let response = await getDataByQueryParam(chartUrlsByDays[name].url, days);
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
        $(chartUrlsByDays[name].div).text('Error occured while loading data');
    }
}

async function changeDaysOnChart(event){
    let btn = event.currentTarget;
    $(btn).siblings().removeClass("active");
    $(btn).addClass( "active" );
    let days = $(btn).data('days');
    $.each(chartUrlsByDays, function (index){
        if ($(btn).hasClass(this.btn_cls)){
            chart = index;
        }
    })
    await updateChart(chart, days);
}


function createChartOptions(type, labels, values, title){
    if (type === 'area' || type === 'bar'){
        return createStandardChartOptions(labels, values, type, title);
    }
    else if (type === 'pie'){
        return createPieChartOptions(labels, values);
    }
}

function modifyOptions(options, chartSettings){
    if (chartSettings.yaxis==='datetime'){
        options.yaxis = {
            labels: {
                formatter: function (value){
                    let days =  Math.floor(Math.floor(value / 60) / 24);
                    let hours = Math.floor((value - days * 60 * 24)  / 60);
                    let minutes = value % 60;
                    return `${days}d. ${hours}:${minutes}`;
                }
            }
        }
    }
    if (chartSettings.xaxis==='datetime'){
        options.xaxis.type = 'datetime'
        options.xaxis.labels = {
            format: 'dd.MM'
        }
    }
    return options;
}

function createStandardChartOptions(labels, values, type, title){
    let options = {
        series: [{
            name: title,
            data: values
        }],
        chart: {
            fontFamily: 'inherit',
            type: type,
            height: '100%'
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
            height: '100%'
        },
    };
    return options;
}