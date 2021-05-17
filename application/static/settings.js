document.getElementById("edit-name-button").addEventListener("click", changeName);
document.getElementById("edit-email-button").addEventListener("click", changeEmail);
document.getElementById("edit-password-button").addEventListener("click", changePassword);

function changeName() {
    var bt = document.getElementById("name-field");
    if (bt.disabled = true) {
        bt.disabled = false;
    }
}

function changeEmail() {
    var bt = document.getElementById("email-field");
    if (bt.disabled = true) {
        bt.disabled = false;
    }
}

function changePassword() {
    var bt = document.getElementById("password-field");
    if (bt.disabled = true) {
        bt.disabled = false;
        bt.placeholder = "";
    }
}