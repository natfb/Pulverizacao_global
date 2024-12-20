document.addEventListener('DOMContentLoaded', function() {

    $(document).ready(function() {
        var cpf = document.querySelector("#cpf");
        
        Inputmask({"mask": "(99) [9]9999-9999"}).mask("#phone_number");
        $(cpf).inputmask({mask: '999.999.999-99', greedy: false}) // nao funciona com o script abaixo
    });

    const form = document.getElementById('myform');
    const checkbox = document.querySelector("[name='active']");
    const hiddenInput = document.getElementById('is_active_hidden');
    const pkInput = document.querySelector("[name='pk']");
    // When the form is submitted, update the hidden input based on checkbox state
    form.addEventListener('submit', function(event) {
        if (checkbox.checked) {
            hiddenInput.value = 'true';  // Set hidden input to 'true' if checked
        } else {
            hiddenInput.value = 'false'; // Set hidden input to 'false' if unchecked
        }
    });
});