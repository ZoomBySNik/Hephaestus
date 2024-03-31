const checkboxesDivs = document.querySelectorAll('.checkbox-div');
let global_mas_checkboxes = {};

checkboxesDivs.forEach(function (checkboxesDiv) {
    let checked_checkboxes = [];
    let not_checked_checkboxes = [];
    let checkboxes = checkboxesDiv.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            var checkboxId = this.id;
            var wrapperId = checkboxesDiv.id;

            if (this.checked) {
                moveCheckbox(checkboxId, global_mas_checkboxes[wrapperId].NotCheckedCheckboxes, global_mas_checkboxes[wrapperId].CheckedCheckboxes);
            } else {
                moveCheckbox(checkboxId, global_mas_checkboxes[wrapperId].CheckedCheckboxes, global_mas_checkboxes[wrapperId].NotCheckedCheckboxes);
            }

            updateCheckboxes(global_mas_checkboxes[wrapperId].CheckedCheckboxes, global_mas_checkboxes[wrapperId].NotCheckedCheckboxes, checkboxesDiv);
        });

        var label = checkbox.parentElement.outerText;
        var checkboxObj = {checkbox: checkbox, label: label, requiredParent: checkbox.parentNode.parentNode};

        if (checkbox.checked) {
            checked_checkboxes.push(checkboxObj);
        } else {
            not_checked_checkboxes.push(checkboxObj);
        }
    });

    global_mas_checkboxes[checkboxesDiv.id] = {CheckedCheckboxes: checked_checkboxes, NotCheckedCheckboxes: not_checked_checkboxes};
    updateCheckboxes(checked_checkboxes, not_checked_checkboxes, checkboxesDiv);
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
