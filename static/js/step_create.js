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
    } else if (type === "video") {
        let inputTitle = document.getElementById("id_video-video_title");
        let inputDescription = document.getElementById("id_video-video_description");
        let inputVideoFile = document.getElementById("id_video-video_file");
        if (select.value) {
            inputTitle.setAttribute("disabled", "disabled");
            inputDescription.setAttribute("disabled", "disabled");
            inputVideoFile.setAttribute("disabled", "disabled");
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
            inputQty.setAttribute("disabled", "disabled");
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


    // function generatePagination(numPages) {
    //     paginationBlock.innerHTML = "";
    //
    //     for (let i = 1; i <= numPages; i++) {
    //         const pageItem = document.createElement("li");
    //         pageItem.classList.add("page-item");
    //
    //         const pageLink = document.createElement("a");
    //         pageLink.classList.add("page-link");
    //         pageLink.classList.add("btn");
    //         pageLink.textContent = i;
    //
    //         pageItem.appendChild(pageLink);
    //         paginationBlock.appendChild(pageItem);
    //
    //
    //         pageLink.addEventListener("click", function () {
    //             showQuestionBlock(i);
    //         });
    //     }
    // }
