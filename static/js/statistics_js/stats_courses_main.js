let lessonTypesChartDiv = document.getElementById('lesson-types-chart');
let stepsCompletedChartDiv = document.getElementById('steps-completed-chart');

let stepsCompletedButtons = $('.steps-completed-chart-btn');

let chartUrlsByDays = {
    'lessonTypesChart': {
        title: 'Типы уроков',
        url: '/statistics/get-lesson-types/',
        div: lessonTypesChartDiv,
        type: 'pie',
    },
    'stepsCompletedChart': {
        title: 'Уроков изучено',
        url: '/statistics/get-steps-completed-qty/?days=',
        div: stepsCompletedChartDiv,
        type: 'area',
        btn_cls: 'steps-completed-chart-btn',
        xaxis: 'datetime',
    },
};

renderChart('lessonTypesChart');
renderChart('stepsCompletedChart', param='7');
stepsCompletedButtons.click(changeDaysOnChart);
