let lessonTypesChartDiv = document.getElementById('lesson-types-chart');
let stepsCompletedChartDiv = document.getElementById('steps-completed-chart');

let stepsCompletedButtons = $('.steps-completed-chart-btn');

let chartUrlsByDays = {
    'lessonTypesChart': {
        url: '/statistics/get-lesson-types/',
        div: lessonTypesChartDiv,
    },
    'stepsCompletedChart': {
        url: '/statistics/get-steps-completed-qty/?days=',
        div: stepsCompletedChartDiv,
        btn_cls: 'steps-completed-chart-btn'
    },
};

renderChart('pie', 'lessonTypesChart');
renderChart('area', 'stepsCompletedChart', param='7');
stepsCompletedButtons.click(changeDaysOnChart);
