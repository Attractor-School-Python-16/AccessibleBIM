let lessonsTypesInCourseChartDiv = document.getElementById('lesson-types-in-course-chart');
let stepCompletionTimeChartDiv = document.getElementById('step-completion-time-chart');
let testResultsInCourseChartDiv = document.getElementById('test-results-in-course-chart');


let chartUrlsByDays = {
    'lessonsTypesInCourseChart': {
        url: '/statistics/get-lesson-types-in-course/?course=',
        div: lessonsTypesInCourseChartDiv,
    },
    'stepCompletionTimeChart': {
        url: '/statistics/get-steps-completion-time/?course=',
        div: stepCompletionTimeChartDiv,
    },
    'testResultsInCourseChart': {
        url: '/statistics/get-test-progress-in-course/?course=',
        div: testResultsInCourseChartDiv,
    },
};

let course_id = $(lessonsTypesInCourseChartDiv).data('course');
renderChart('pie', 'lessonsTypesInCourseChart', param=course_id);
renderChart('bar', 'stepCompletionTimeChart', param=course_id);
renderChart('column', 'testResultsInCourseChart', param=course_id);