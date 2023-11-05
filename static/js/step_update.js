const videoSelectDiv = document.getElementById("video")
const textSelectDiv = document.getElementById("text")
const form = document.getElementById("main-form")

document.addEventListener("DOMContentLoaded", function () {
    if (videoSelectDiv) {
        let submitButton = document.getElementById("submit_button")
        form.insertBefore(videoSelectDiv, submitButton)
    }
    if (textSelectDiv) {
        let submitButton = document.getElementById("submit_button")
        form.insertBefore(textSelectDiv, submitButton)
    }
    let deselectButton = document.createElement("button");
    deselectButton.textContent = "Снять выбор";
    deselectButton.className = "btn btn-primary"
    deselectButton.addEventListener("click", function (event) {
        event.preventDefault()
        let selectElement = document.getElementById('id_step-file');
        for (let i = 0; i < selectElement.options.length; i++) {
            selectElement.options[i].selected = false;
        }
    });
    let fileDiv = document.getElementById('div_id_step-file');
    fileDiv.parentNode.appendChild(deselectButton);
});

let lessonType;
let contentUpdateLink;
let selectElement;
let baseUrl = window.location.protocol + '//' + window.location.host;

document.addEventListener("DOMContentLoaded", function () {
    const elementsWithLessonTypes = Array.from(document.querySelectorAll('[id*="text"], [id*="video"], [id*="test"]'));
    if (elementsWithLessonTypes.length > 0) {
        lessonType = extractLessonTypeFromId(elementsWithLessonTypes[0].id);
        selectElement = document.getElementById(`id_step-${lessonType}`);
        const stepDiv = document.getElementById(`div_id_step-${lessonType}`);
        if (stepDiv) {
            contentUpdateLink = document.createElement("a");
            contentUpdateLink.textContent = "Редактировать связанный контент";
            contentUpdateLink.className = "content-update-link my-2";
            contentUpdateLink.href = getUpdateUrl(lessonType, baseUrl, selectElement.value);
            stepDiv.appendChild(contentUpdateLink);
        }
    }

    function handleSelectChange() {
        contentUpdateLink.href = getUpdateUrl(lessonType, baseUrl, selectElement.value);
    }

    selectElement.addEventListener("change", handleSelectChange);
});

function extractLessonTypeFromId(elementId) {
    if (elementId.includes("text")) {
        return "text";
    } else if (elementId.includes("video")) {
        return "video";
    } else if (elementId.includes("test")) {
        return "test";
    }
    return "unknown";
}

function getUpdateUrl(lessonType, baseUrl, selectValue) {
    if (lessonType === "text") {
        return selectValue ? `${baseUrl}/moderator/text/${selectValue}/update/` : "";
    } else if (lessonType === "video") {
        return selectValue ? `${baseUrl}/moderator/video/${selectValue}/update/` : "";
    } else if (lessonType === "test") {
        return selectValue ? `${baseUrl}/moderator/quiz_bim/test/${selectValue}` : "";
    } else {
        return "";
    }
}


