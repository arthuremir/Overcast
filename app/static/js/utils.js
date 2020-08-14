function validateForm() {
    input_field = document.getElementsByClassName("location_input")[0];
    if (input_field.value === "") {
        input_field.setAttribute("placeholder", "Input is empty...");
        return false;
    }
    return true;
}

