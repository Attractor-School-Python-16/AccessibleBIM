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
        buttonLink.classList.add('page-link', 'mx-1', 'my-1', 'button');
        buttonLink.href = "#";  // Установите нужный href
        buttonLink.textContent = index + 1;

        buttonLink.addEventListener('click', (event) => {
            event.preventDefault();
            showQuestions(index);
        });

        button.appendChild(buttonLink);
        paginationContainer.appendChild(button);
    });

    paginationContainer.classList.add('d-flex', 'flex-wrap', 'justify-content-center');
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
