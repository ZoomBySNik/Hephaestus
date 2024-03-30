var checkboxes = document.querySelectorAll('input[type="checkbox"]');
let checked_checkboxes = [];
let not_checked_checkboxes = [];
const checkboxesDiv = document.querySelector('.checkbox-div');
checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
        var checkboxId = this.id;
        var requiredParent = this.parentNode.parentNode;
        if (this.checked) {
            console.log(this);
            moveCheckbox(checkboxId, not_checked_checkboxes, checked_checkboxes);
        } else {
            console.log(this);
            moveCheckbox(checkboxId, checked_checkboxes, not_checked_checkboxes);
        }
        updateCheckboxes(checked_checkboxes, not_checked_checkboxes, checkboxesDiv);
    });
});

function moveCheckbox(checkboxId, fromArray, toArray) {
    var index = fromArray.findIndex(function (checkbox) {
        return checkbox.checkbox.id === checkboxId;
    });

    if (index !== -1) {
        var removedCheckbox = fromArray.splice(index, 1)[0];
        toArray.push(removedCheckbox);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    let checkboxes = document.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(function (checkbox) {
        if (checkbox.closest('.switch__input')) {
            return; // Пропускаем кнопку смены темы
        }
        var label = checkbox.parentElement.outerText;
        var checkboxObj = {checkbox: checkbox, label: label, requiredParent: checkbox.parentNode.parentNode};
        if (checkbox.checked) {
            checked_checkboxes.push(checkboxObj)
        } else {
            not_checked_checkboxes.push(checkboxObj)
        }

    });
    updateCheckboxes(checked_checkboxes, not_checked_checkboxes, checkboxesDiv);
});

function updateCheckboxes(checked_checkboxes, not_checked_checkboxes, checkboxesDiv) {
    checked_checkboxes.forEach(function (checkbox) {
        checkbox.requiredParent.classList.add('selected');
    });
    not_checked_checkboxes.forEach(function (checkbox) {
        checkbox.requiredParent.classList.remove('selected');
    });
    checked_checkboxes.sort((a, b) => a.label.localeCompare(b.label));
    not_checked_checkboxes.sort((a, b) => a.label.localeCompare(b.label));
    if (checkboxesDiv) {
        while (checkboxesDiv.firstChild) {
            checkboxesDiv.removeChild(checkboxesDiv.firstChild);
        }

        // Отрисовка отсортированных списков заново
        checked_checkboxes.forEach(function (checkbox) {
            checkboxesDiv.appendChild(checkbox.requiredParent);
        });
        not_checked_checkboxes.forEach(function (checkbox) {
            checkboxesDiv.appendChild(checkbox.requiredParent);
        });
    }
}