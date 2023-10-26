let newUsersChartDiv = document.getElementById('new-users-chart');
let newUsersButtons = $('.new-users-chart-btn');
let chartUrlsByDays = {
    'newUsersChart': {
        url: '/statistics/get-new-users-qty/?days=',
        div: newUsersChartDiv,
        btn_cls: 'new-users-chart-btn'
    }
};

renderChart('area', 'newUsersChart', param='7');
newUsersButtons.click(changeDaysOnChart);