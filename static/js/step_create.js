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
    } else {
        form.style.display = "block";
    }
}


function clearInputsInDiv(div) {
    const inputElements = div.getElementsByTagName('input');
    const selectElements = div.getElementsByTagName('select');

    for (let i = 0; i < inputElements.length; i++) {
        inputElements[i].value = '';
    }
    for (let i = 0; i < selectElements.length; i++) {
        selectElements[i].value = '';
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
        clearInputsInDiv(videoContent, testContent);
    } else if (lessonType.value === "video") {
        textContent.style.display = "none";
        videoContent.style.display = "block";
        testContent.style.display = "none";
        clearInputsInDiv(textContent, testContent);
    } else if (lessonType.value === "test") {
        textContent.style.display = "none";
        videoContent.style.display = "none";
        testContent.style.display = "block";
        clearInputsInDiv(videoContent, textContent);
    }
});

document.getElementById("confirmQuestions").addEventListener("click", function () {
    const questionsQty = parseInt(document.getElementById("test_questions_qty").value, 10);
    if (!isNaN(questionsQty)) {
        createQuestionInputs(questionsQty);
    }
});

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

        const addAnswerButton = document.createElement("button");
        addAnswerButton.setAttribute("type", "button");
        addAnswerButton.setAttribute("class", "btn btn-primary my-3");
        addAnswerButton.textContent = "Добавить ответ";

        addAnswerButton.addEventListener("click", function () {
            createAnswerInputs(answersContainer);
        });

        questionBlock.appendChild(questionLabel);
        questionBlock.appendChild(questionInput);
        questionBlock.appendChild(answersContainer);
        questionBlock.appendChild(addAnswerButton);
        questionForm.appendChild(questionBlock);
        createAnswerInputs(answersContainer);
    }
}

function createAnswerInputs(answersContainer) {
    const answerBlock = document.createElement("div");
    answerBlock.setAttribute("class", "content-test");

    const answerLabel = document.createElement("label");
    answerLabel.setAttribute("for", "answer");
    answerLabel.textContent = "Введите ответ";

    const answerInput = document.createElement("input");
    answerInput.setAttribute("type", "text");
    answerInput.setAttribute("name", "answer");
    answerInput.setAttribute("class", "form-control");

    const isCorrectLabel = document.createElement("label");
    isCorrectLabel.textContent = "Выберите правильность ответа";

    const isCorrectSelect = document.createElement("select");
    isCorrectSelect.setAttribute("name", "is_correct");
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

}