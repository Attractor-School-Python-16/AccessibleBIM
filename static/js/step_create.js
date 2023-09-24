const textContent = document.getElementById("text_content");
const videoContent = document.getElementById("video_content");
const testContent = document.getElementById("test_content");
const lessonType = document.getElementById("id_lesson_type");
const textSelect = document.getElementById("id_text");
const videoSelect = document.getElementById("id_video");
const testSelect = document.getElementById("id_test");
const textForm = document.getElementById("text-form");
const videoForm = document.getElementById("video-form");
const testForm = document.getElementById("test-form");

function handleSelectChange(select, form) {
    if (select.value) {
        form.style.display = "none";
        clearInputsInDiv(form);
    } else {
        form.style.display = "block";
    }
}


function clearInputsInDiv(div) {
    const inputElements = div.getElementsByTagName('input');
    const textareaElements = div.querySelectorAll('textarea');



    for (let i = 0; i < inputElements.length; i++) {
        inputElements[i].value = '';
    }


    for (let i = 0; i < textareaElements.length; i++) {
        textareaElements[i].value = '';
    }
}



textSelect.addEventListener("change", function () {
    handleSelectChange(textSelect, textForm);
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
    const questionsQtyInput = document.getElementsByName("test_questions_qty")[0];
    const questionsQty = parseInt(questionsQtyInput.value);
    if (!isNaN(questionsQty)) {
        createQuestionInputs(questionsQty);
    }
});

let questionCounter = 1;

function createQuestionInputs(questionsQty) {
    const questionForm = document.getElementById("question-form");
    questionForm.innerHTML = "";

    for (let i = 1; i <= questionsQty; i++) {
        const questionBlock = document.createElement("div");
        questionBlock.setAttribute("class", "question-block");

        const questionLabel = document.createElement("label");
        questionLabel.setAttribute("for", `question_title_${i}`);
        questionLabel.textContent = `Введите вопрос ${i}`;

        const questionInput = document.createElement("input");
        questionInput.setAttribute("type", "text");
        questionInput.setAttribute("name", `question_title_${i}`);
        questionInput.setAttribute("class", "form-control");

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