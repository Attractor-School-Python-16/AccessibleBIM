const fileSelect = document.getElementById("id_step-file");
const videoSelect = document.getElementById("id_step-video")
const textSelect = document.getElementById("id_step-text")
const testSelect = document.getElementById("id_step-test")




function handleSelectChange(select, type) {
    if (type === "text") {
        let inputTitle = document.getElementById("id_text-text_title");
        let descriptionDiv = document.getElementById("div_id_text-text_description");
        let contentDiv = document.getElementById("div_id_text-content");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            descriptionDiv.style.pointerEvents = "none"
            contentDiv.style.pointerEvents = "none"
        } else {
            inputTitle.removeAttribute("disabled");
            descriptionDiv.style.pointerEvents = "auto"
            contentDiv.style.pointerEvents = "auto"

        }
    }
}



textSelect.addEventListener("change", function () {
    handleSelectChange(textSelect, "text");
});

videoSelect.addEventListener("change", function () {
    handleSelectChange(videoSelect, videoForm);
});

testSelect.addEventListener("change", function () {
    handleSelectChange(testSelect, testForm);
});

lessonType.addEventListener("change", function () {
    if (lessonType.value === "text") {
        textContent.style.display = "block";
        videoContent.style.display = "none";
        testContent.style.display = "none";
        clearInputsInDiv(videoForm);
        clearInputsInDiv(testForm);
    } else if (lessonType.value === "video") {
        textContent.style.display = "none";
        videoContent.style.display = "block";
        testContent.style.display = "none";
        clearInputsInDiv(textForm);
        clearInputsInDiv(testForm);
    } else if (lessonType.value === "test") {
        textContent.style.display = "none";
        videoContent.style.display = "none";
        testContent.style.display = "block";
        clearInputsInDiv(textForm);
        clearInputsInDiv(videoForm);
    }
});

document.getElementById("confirmQuestions").addEventListener("click", function () {
    const questionsQtyInput = document.getElementById("questions_qty_to_create")
    const questionsQty = parseInt(questionsQtyInput.value);
    if (!isNaN(questionsQty)) {
        createQuestionInputs(questionsQty);
    }
});

let questionCounter = 1;

function createQuestionInputs(questionsQty) {
    const questionForm = document.getElementById("question-form");
    const questionBlocksCountInput = document.getElementById("questionBlocksCount");
    questionForm.innerHTML = "";

    for (let i = 1; i <= questionsQty; i++) {
        const questionBlock = document.createElement("div");
        questionBlock.setAttribute("class", "question-block");
        questionBlock.setAttribute("display", "none");

        const questionLabel = document.createElement("label");
        questionLabel.setAttribute("for", `question_title_${i}`);
        questionLabel.textContent = `Введите вопрос ${i}`;

        const questionInput = document.createElement("input");
        questionInput.setAttribute("type", "text");
        questionInput.setAttribute("name", `question_title_${i}`);
        questionInput.setAttribute("class", "form-control");
        questionInput.setAttribute("required", "required");

        const answersContainer = document.createElement("div");
        answersContainer.setAttribute("class", "content-test");

        const answersQtyInput = document.createElement("input");
        answersQtyInput.setAttribute("type", "hidden");
        answersQtyInput.setAttribute("name", `answers_qty_${i}`);
        answersQtyInput.value = 0;

        const addAnswerButton = document.createElement("button");
        addAnswerButton.setAttribute("type", "button");
        addAnswerButton.setAttribute("class", "btn btn-primary my-3");
        addAnswerButton.textContent = "Добавить ответ";
        addAnswerButton.setAttribute("data-question-number", i);

        addAnswerButton.addEventListener("click", function () {
            const questionNumber = this.getAttribute("data-question-number");
            createAnswerInputs(answersContainer, questionNumber);
        });

        questionBlock.appendChild(questionLabel);
        questionBlock.appendChild(questionInput);
        questionBlock.appendChild(answersContainer);
        questionBlock.appendChild(answersQtyInput);
        questionBlock.appendChild(addAnswerButton);

        questionForm.appendChild(questionBlock);

        questionCounter++;
        questionBlocksCountInput.value = parseInt(questionBlocksCountInput.value) + 1;
    }
}

function createAnswerInputs(answersContainer, questionNumber) {
    const answerBlock = document.createElement("div");
    answerBlock.setAttribute("class", "content-test");

    const questionIndex = questionNumber;
    const answersQtyInput = answersContainer.parentElement.querySelector(`input[name="answers_qty_${questionIndex}"]`);
    const currentAnswersQty = parseInt(answersQtyInput.value, 10);

    const answerLabel = document.createElement("label");
    answerLabel.setAttribute("for", `answer_${questionNumber}_${currentAnswersQty + 1}`);
    answerLabel.textContent = `Введите ответ ${currentAnswersQty + 1} для вопроса ${questionNumber}`;

    const answerInput = document.createElement("input");
    answerInput.setAttribute("type", "text");
    answerInput.setAttribute("name", `answer_${questionNumber}_${currentAnswersQty + 1}`);
    answerInput.setAttribute("class", "form-control");
    // answerInput.setAttribute("required", "required");

    const isCorrectLabel = document.createElement("label");
    isCorrectLabel.textContent = "Выберите правильность ответа";

    const isCorrectSelect = document.createElement("select");
    isCorrectSelect.setAttribute("name", `is_correct_${questionNumber}_${currentAnswersQty + 1}`);
    isCorrectSelect.setAttribute("class", "form-control");
    isCorrectSelect.innerHTML = `
            <option value="False" selected>Неверный ответ</option>
            <option value="True">Верный ответ</option>
        `;

    answerBlock.appendChild(answerLabel);
    answerBlock.appendChild(answerInput);
    answerBlock.appendChild(isCorrectLabel);
    answerBlock.appendChild(isCorrectSelect);

    answersContainer.appendChild(answerBlock);

    answersQtyInput.value = currentAnswersQty + 1;
}

const questionsQtyInput = document.getElementById("questions_qty_to_create");
const confirmQuestionsButton = document.getElementById("confirmQuestions");
const paginationBlock = document.getElementById("pagination-block");

confirmQuestionsButton.addEventListener("click", function () {
    const questionsQty = parseInt(questionsQtyInput.value);

    generatePagination(questionsQty);

    showQuestionBlock(1);
});


function generatePagination(numPages) {
    paginationBlock.innerHTML = "";

    for (let i = 1; i <= numPages; i++) {
        const pageItem = document.createElement("li");
        pageItem.classList.add("page-item");

        const pageLink = document.createElement("a");
        pageLink.classList.add("page-link");
        pageLink.classList.add("btn");
        pageLink.textContent = i;

        pageItem.appendChild(pageLink);
        paginationBlock.appendChild(pageItem);


        pageLink.addEventListener("click", function () {
            showQuestionBlock(i);
        });
    }
}

function showQuestionBlock(pageNumber) {
    const questionBlocks = document.querySelectorAll(".question-block");
    currentPage = pageNumber;

    questionBlocks.forEach((block, index) => {
        if (index === pageNumber - 1) {
            block.style.display = "block";
        } else {
            block.style.display = "none";
        }
    });
}

const questionBlocksCount = document.getElementById("questions_qty_to_create");
const questionsQty = document.getElementById("questions_qty_test");
const sendButton = document.getElementById("submit_button");

function handleInputChange() {
    if (parseInt(questionBlocksCount.value) < parseInt(questionsQty.value)) {
        alert('Количество создаваемых вопросов не может быть меньше количества вопросов в тесте');
        sendButton.disabled = true;
    } else {
        sendButton.disabled = false;
    }
}

questionBlocksCount.addEventListener('change', handleInputChange);
questionsQty.addEventListener('change', handleInputChange);
