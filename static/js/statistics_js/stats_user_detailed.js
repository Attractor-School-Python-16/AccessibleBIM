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

async function getTestProgress(user_pk, course_pk){
    let url = `/statistics/get-test-progress/?user=${user_pk}&course=${course_pk}`;
    let response = await makeRequest(url, "GET");
    return response;
}

function createBarChartOptions(labels, values){
    let options = {
        series: [{
            name: 'Результат теста',
            data: values
        }],
        chart: {
            fontFamily: 'inherit',
            type: 'bar',
        },
        plotOptions: {
            bar: {
                horizontal: true,
                barHeight: '10%'
            }
        },
        xaxis: {
            categories: labels
        },
        yaxis: {
            min: 0,
            max: 100,
          }
    };
    return options;
}

async function renderTestCharts() {
    $(barCharts).each(async function () {
        let elementId = '#' + this.id;
        let element = $(elementId)[0];
        let user_pk = $(element).data("user");
        let course_pk = $(element).data("course");
        let response = await getTestProgress(user_pk, course_pk);
        if (response.values.length===0) {
            $(element).text('No data to display');
        } else if (!response.error) {
            let options = createBarChartOptions(response.labels, response.values);
            let chart = new ApexCharts(element, options);
            chart.render();
        }else {
            $(element).text('Error occured while loading data');
        }
    });
}

let barCharts = $('.test-progress-chart');
renderTestCharts();
