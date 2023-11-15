const videoSelect = document.getElementById("id_step-video")
const textSelect = document.getElementById("id_step-text")
const testSelect = document.getElementById("id_step-test")
const videoSelectDiv = document.getElementById("video")
const textSelectDiv = document.getElementById("text")
const form = document.getElementById("main-form")


document.addEventListener("DOMContentLoaded", function () {
    if (videoSelectDiv) {
        let videoTitle = document.getElementById("video_title")
        form.insertBefore(videoSelectDiv, videoTitle)
    }
    if (textSelectDiv) {
        let textTitle = document.getElementById("text_title")
        form.insertBefore(textSelectDiv, textTitle)
    }
    if (videoSelect || textSelect) {
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
    }
    if (textSelect) {
        handleSelectChange(textSelect, "text");
    }
    ;
    if (videoSelect) {
        handleSelectChange(videoSelect, "video");
    }
    ;
    if (testSelect) {
        handleSelectChange(testSelect, "test");
    }
});


function clearTextAreas() {
    const descFrame = document.getElementById("id_text-text_description_iframe");
    const contentFrame = document.getElementById("id_text-content_iframe");
    const descDocument = descFrame.contentDocument || descFrame.contentWindow.document;
    const contentDocument = contentFrame.contentDocument || contentFrame.contentWindow.document;
    const elementsInDescDocument = descDocument.querySelectorAll(".note-editable.card-block");
    const elementsInContentDocument = contentDocument.querySelectorAll(".note-editable.card-block");
    elementsInDescDocument.forEach(function (element) {
        element.innerHTML = "";
    });
    elementsInContentDocument.forEach(function (element) {
        element.innerHTML = "";
    });
    const form = document.getElementById("main-form");
    for (const element of form.elements) {
        if (!element.name || element.disabled || element.type === "submit" || element.type === "button") {
            continue;
        }
        if (element.name === "text-text_description" || element.name === "text-content") {
            element.value = "";
        }
    }
}

function handleSelectChange(select, type) {
    if (type === "text") {
        let inputTitle = document.getElementById("id_text-text_title");
        let descriptionDiv = document.getElementById("div_id_text-text_description");
        let contentDiv = document.getElementById("div_id_text-content");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            inputTitle.value = "";
            inputTitle.required = false
            descriptionDiv.style.pointerEvents = "none";
            contentDiv.style.pointerEvents = "none";
            clearTextAreas()
        } else {
            inputTitle.removeAttribute("disabled");
            inputTitle.required = true
            descriptionDiv.style.pointerEvents = "auto";
            contentDiv.style.pointerEvents = "auto";

        }
    } else if (type === "video") {
        let inputTitle = document.getElementById("id_video-video_title");
        let inputDescription = document.getElementById("id_video-video_description");
        let inputVideoFile = document.getElementById("id_video-video_file");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            inputTitle.required = false
            inputTitle.value = "";
            inputDescription.setAttribute("disabled", "disabled");
            inputDescription.required = false
            inputDescription.value = "";
            inputVideoFile.setAttribute("disabled", "disabled");
            inputVideoFile.required = false
            inputVideoFile.value = ""
        } else {
            inputTitle.removeAttribute("disabled");
            inputTitle.required = true
            inputDescription.removeAttribute("disabled");
            inputDescription.required = true
            inputVideoFile.removeAttribute("disabled");
            inputVideoFile.required = true
        }

    } else if (type === "test") {

        let inputTitle = document.getElementById("id_quiz-title");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            inputTitle.required = false
            inputTitle.value = "";
        } else {
            inputTitle.removeAttribute("disabled");
            inputTitle.required = true
        }
    }
}


if (textSelect) {
    textSelect.addEventListener("change", function () {
        handleSelectChange(textSelect, "text");
    });

    let submitButton = document.getElementById("submit_button");
    submitButton.addEventListener("click", function (event) {
        const descFrame = document.getElementById("id_text-text_description_iframe");
        const contentFrame = document.getElementById("id_text-content_iframe");
        const descDocument = descFrame.contentDocument || descFrame.contentWindow.document;
        const contentDocument = contentFrame.contentDocument || contentFrame.contentWindow.document;
        const elementsInDescDocument = descDocument.querySelectorAll(".note-editable.card-block");
        const elementsInContentDocument = contentDocument.querySelectorAll(".note-editable.card-block");

        const regex = /^(<p>|<br>|<\/p>|&nbsp;)+$/;

        elementsInDescDocument.forEach(function (element) {
            if (regex.test(element.innerHTML)) {
                event.preventDefault();
                alert("Заполните описание лекции");
            }
        });

        elementsInContentDocument.forEach(function (element) {
            if (regex.test(element.innerHTML)) {
                event.preventDefault();
                alert("Заполните содержание лекции");
            }
        });
    });
}


if (videoSelect) {
    videoSelect.addEventListener("change", function () {
        handleSelectChange(videoSelect, "video");
    });
}

if (testSelect) {
    testSelect.addEventListener("change", function () {
        handleSelectChange(testSelect, "test");
    });
}

