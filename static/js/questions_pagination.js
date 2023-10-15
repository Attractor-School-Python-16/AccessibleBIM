let questionBlocks = document.querySelectorAll('.question-block');
let paginationContainer = document.getElementById('pagination-block');

let currentPage = 0;

function showQuestions(pageNumber) {
    questionBlocks.forEach((block, index) => {
        if (index === pageNumber) {
            block.style.display = 'block';
        } else {
            block.style.display = 'none';
        }
    });
}

function createPaginationButtons() {
    paginationContainer.innerHTML = '';

    questionBlocks = document.querySelectorAll('.question-block');

    questionBlocks.forEach((_, index) => {
        let button = document.createElement('li');
        button.classList.add('page-item');
        let buttonLink = document.createElement('a');
        buttonLink.classList.add('page-link');
        buttonLink.classList.add('mx-1');
        buttonLink.type = "button";
        buttonLink.textContent = index + 1;

        buttonLink.addEventListener('click', () => {
            showQuestions(index);
        });

        button.appendChild(buttonLink);
        paginationContainer.appendChild(button);
    });
}

function updatePageAfterNewQuestionCreated() {
    let questionForms = document.getElementById('questionforms');
    let questionDetailBlock = questionForms.querySelector('#question_detail');

    if (questionDetailBlock) {
        let newQuestionBlock = document.createElement('div');
        newQuestionBlock.classList.add('question-block');
        newQuestionBlock.appendChild(questionDetailBlock.cloneNode(true));
        let questionsContainer = document.querySelector('.questions-container');
        questionsContainer.appendChild(newQuestionBlock);

        questionDetailBlock.remove();

        createPaginationButtons();
        showQuestions(currentPage);
    }
}

document.body.addEventListener('htmx:afterOnLoad', function (event) {
    let questionCreated = document.getElementById("questionforms")
    let questionToProcess = questionCreated.querySelector("#question_detail")
    if (questionToProcess) {
        updatePageAfterNewQuestionCreated()
    }
});

let deleteButtons = document.querySelectorAll('[id="delete-question"]')

deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
        window.location.reload();
    });
});

createPaginationButtons();
showQuestions(currentPage);
