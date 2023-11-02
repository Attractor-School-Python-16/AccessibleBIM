let newSubscriptionsChartDiv = document.getElementById('new-subscriptions-chart');
let popularCoursesChartDiv = document.getElementById('popular-courses-chart');

let newSubscriptionButtons = $('.new-subscriptions-chart-btn');
let popularCoursesButtons = $('.popular-courses-chart-btn');

let chartUrlsByDays = {
    'newSubscriptionsChart': {
        title: 'Новых подписок',
        url: '/statistics/get-new-subscriptions-qty/?days=',
        div: newSubscriptionsChartDiv,
        type: 'area',
        btn_cls: 'new-subscriptions-chart-btn',
        xaxis: 'datetime',
    },
    'popularCoursesChart': {
        title: 'Курсов куплено',
        url: '/statistics/get-popular-courses/?days=',
        div: popularCoursesChartDiv,
        type: 'bar',
        btn_cls: 'popular-courses-chart-btn'
    },
};

renderChart('newSubscriptionsChart', param='7');
newSubscriptionButtons.click(changeDaysOnChart);

renderChart('popularCoursesChart', param='7');
popularCoursesButtons.click(changeDaysOnChart);
