document.addEventListener('DOMContentLoaded', () => {

    const editButton = document.querySelectorAll('.show-edit-btn')
    console.log('bs', editButton)
    editButton.forEach(button => {
        button.addEventListener('click', () => {
            toggleCheckboxes()
            button.style.filter = button.style.filter === 'invert(100%)' || button.style.filter == '' ? 'invert(60%)' : 'invert(100%)';
        });
    });

    function toggleCheckboxes() {
        const checkboxes = document.querySelectorAll('.checkbox');
        const editButton = document.querySelectorAll('.edit-button');
        checkboxes.forEach(checkbox => {
            checkbox.style.display = checkbox.style.display === 'none' || checkbox.style.display == ''  ? 'inline-block' : 'none';
        });
        editButton.forEach(checkbox => {
            checkbox.style.display = checkbox.style.display === 'none' || checkbox.style.display == ''  ? 'inline-block' : 'none';
        });
    }

});