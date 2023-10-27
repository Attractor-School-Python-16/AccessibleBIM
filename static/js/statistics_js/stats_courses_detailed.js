let lessonsTypesInCourseChartDiv = document.getElementById('lesson-types-in-course-chart');
let stepCompletionTimeChartDiv = document.getElementById('step-completion-time-chart');
let testResultsInCourseChartDiv = document.getElementById('test-results-in-course-chart');


let chartUrlsByDays = {
    'lessonsTypesInCourseChart': {
        title: 'Типы уроков',
        url: '/statistics/get-lesson-types-in-course/?course=',
        div: lessonsTypesInCourseChartDiv,
        type: 'pie',
    },
    'stepCompletionTimeChart': {
        title: 'Время на изучение урока',
        url: '/statistics/get-steps-completion-time/?course=',
        div: stepCompletionTimeChartDiv,
        type: 'bar',
        yaxis: 'datetime',
    },
    'testResultsInCourseChart': {
        title: 'Результаты тестов',
        url: '/statistics/get-test-progress-in-course/?course=',
        div: testResultsInCourseChartDiv,
        type: 'bar',
    },
};

let course_id = $(lessonsTypesInCourseChartDiv).data('course');
renderChart('lessonsTypesInCourseChart', param=course_id);
renderChart('stepCompletionTimeChart', param=course_id);
renderChart('testResultsInCourseChart', param=course_id);