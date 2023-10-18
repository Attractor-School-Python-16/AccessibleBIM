document.addEventListener("DOMContentLoaded", function() {
    console.log("here")
    let deselectButton = document.createElement("button");
    deselectButton.textContent = "Снять выбор";
    deselectButton.className = "btn btn-primary"
    deselectButton.addEventListener("click", function(event) {
        event.preventDefault()
      let selectElement = document.getElementById('id_step-file');
      for (let i = 0; i < selectElement.options.length; i++) {
        selectElement.options[i].selected = false;
      }
    });
    let fileDiv = document.getElementById('div_id_step-file');
    fileDiv.parentNode.appendChild(deselectButton);
  });
