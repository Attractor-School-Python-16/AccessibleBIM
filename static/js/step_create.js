const videoSelect = document.getElementById("id_step-video")
const textSelect = document.getElementById("id_step-text")
const testSelect = document.getElementById("id_step-test")


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
}

function handleSelectChange(select, type) {
    if (type === "text") {
        let inputTitle = document.getElementById("id_text-text_title");
        let descriptionDiv = document.getElementById("div_id_text-text_description");
        let contentDiv = document.getElementById("div_id_text-content");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            inputTitle.value = "";
            descriptionDiv.style.pointerEvents = "none";
            contentDiv.style.pointerEvents = "none";
            clearTextAreas()
        } else {
            inputTitle.removeAttribute("disabled");
            descriptionDiv.style.pointerEvents = "auto";
            contentDiv.style.pointerEvents = "auto";

        }
    } else if (type === "video") {
        let inputTitle = document.getElementById("id_video-video_title");
        let inputDescription = document.getElementById("id_video-video_description");
        let inputVideoFile = document.getElementById("id_video-video_file");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            inputTitle.value = "";
            inputDescription.setAttribute("disabled", "disabled");
            inputDescription.value = "";
            inputVideoFile.setAttribute("disabled", "disabled");
            inputVideoFile.value = ""
        } else {
            inputTitle.removeAttribute("disabled");
            inputDescription.removeAttribute("disabled");
            inputVideoFile.removeAttribute("disabled");
        }


    } else if (type === "test") {

        let inputTitle = document.getElementById("id_quiz-title");
        let inputQty = document.getElementById("id_quiz-questions_qty");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            inputTitle.value = "";
            inputQty.setAttribute("disabled", "disabled");
            inputQty.value = ""
        } else {
            inputTitle.removeAttribute("disabled");
            inputQty.removeAttribute("disabled");
        }
    }
}


if (textSelect) {
    textSelect.addEventListener("change", function () {
        handleSelectChange(textSelect, "text");
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
