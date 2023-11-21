let newUsersChartDiv = document.getElementById('new-users-chart');
let newUsersButtons = $('.new-users-chart-btn');
let chartUrlsByDays = {
    'newUsersChart': {
        title: 'Новых пользователей',
        url: '/statistics/get-new-users-qty/?days=',
        div: newUsersChartDiv,
        type: 'area',
        btn_cls: 'new-users-chart-btn',
        xaxis: 'datetime',
    }
};

renderChart('newUsersChart', param='7');
newUsersButtons.click(changeDaysOnChart);