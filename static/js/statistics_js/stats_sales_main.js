let newSubscriptionsChartDiv = document.getElementById('new-subscriptions-chart');
let popularCoursesChartDiv = document.getElementById('popular-courses-chart');

let newSubscriptionButtons = $('.new-subscriptions-chart-btn');
let popularCoursesButtons = $('.popular-courses-chart-btn');

let chartUrlsByDays = {
    'newSubscriptionsChart': {
        url: '/statistics/get-new-subscriptions-qty/?days=',
        div: newSubscriptionsChartDiv,
        btn_cls: 'new-subscriptions-chart-btn'
    },
    'popularCoursesChart': {
        url: '/statistics/get-popular-courses/?days=',
        div: popularCoursesChartDiv,
        btn_cls: 'popular-courses-chart-btn'
    },
};

renderChart('area', 'newSubscriptionsChart', param='7');
newSubscriptionButtons.click(changeDaysOnChart);

renderChart('bar', 'popularCoursesChart', param='7');
popularCoursesButtons.click(changeDaysOnChart);
