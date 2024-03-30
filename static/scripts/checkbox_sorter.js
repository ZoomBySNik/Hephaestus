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