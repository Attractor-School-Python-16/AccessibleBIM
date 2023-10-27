const tasksListElement = document.querySelector(`.list-group`);
const taskElements = tasksListElement.querySelectorAll(`.list-group-item`);

for (const task of taskElements) {
    task.draggable = true;
}
tasksListElement.addEventListener(`dragstart`, (evt) => {
    evt.target.classList.add(`selected`);
})

tasksListElement.addEventListener(`dragend`, (evt) => {
    evt.target.classList.remove(`selected`);
});
tasksListElement.addEventListener(`dragover`, (evt) => {
    evt.preventDefault();

    const activeElement = tasksListElement.querySelector(`.selected`);
    const currentElement = evt.target;
    const isMoveable = activeElement !== currentElement &&
        currentElement.classList.contains(`list-group-item`);

    if (!isMoveable) {
        return;
    }
    const nextElement = getNextElement(evt.clientY, currentElement);
    if (
        nextElement &&
        activeElement === nextElement.previousElementSibling ||
        activeElement === nextElement
    ) {
        return;
    }

    tasksListElement.insertBefore(activeElement, nextElement);
    updateHiddenInputsAndNewNumbers();
});
const getNextElement = (cursorPosition, currentElement) => {
    const currentElementCoord = currentElement.getBoundingClientRect();
    const currentElementCenter = currentElementCoord.y + currentElementCoord.height / 2;
    const nextElement = (cursorPosition < currentElementCenter) ?
        currentElement :
        currentElement.nextElementSibling;

    return nextElement;
};

function updateHiddenInputsAndNewNumbers() {
    const listItems = tasksListElement.querySelectorAll('.list-group-item');
    listItems.forEach((item, index) => {
        const previousInputs = Array.from(item.getElementsByClassName("number-value"));
        if (previousInputs.length > 0) {
            previousInputs.forEach((input) => {
                input.remove();
            });
        }
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = item.id;
        input.value = index + 1;
        input.className = "number-value"
        item.appendChild(input);

        const newNumberText = item.querySelector('#new-number');
        newNumberText.textContent = `Новый номер: ${index + 1}`;
    });
}