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


let deleteButtons = document.querySelectorAll('[id="delete-question"]')

deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
        setTimeout(() => {
            window.location.reload();
        }, 200);
    });
});


createPaginationButtons();
showQuestions(currentPage);
