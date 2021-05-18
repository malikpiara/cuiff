document.getElementById("edit-name-button").addEventListener("click", changeName);
document.getElementById("cancel-name-button").addEventListener("click", changeNameSave);

document.getElementById("edit-email-button").addEventListener("click", changeEmail);
document.getElementById("cancel-email-button").addEventListener("click", changeEmailSave);

document.getElementById("edit-password-button").addEventListener("click", changePassword);

function changeName() {
    var bt = document.getElementById("name-field");
    if (bt.disabled = true) {
        bt.disabled = false;
    }
    document.getElementById("save-name-button").style.visibility = "visible";
    document.getElementById("cancel-name-button").style.visibility = "visible";
}

function changeNameSave() {
    var bt = document.getElementById("name-field");
    bt.disabled = true
    document.getElementById("save-name-button").style.visibility = "hidden";
    document.getElementById("cancel-name-button").style.visibility = "hidden";
}

function changeEmail() {
    var bt = document.getElementById("email-field");
    if (bt.disabled = true) {
        bt.disabled = false;
    }
    document.getElementById("save-email-button").style.visibility = "visible";
    document.getElementById("cancel-email-button").style.visibility = "visible";
}

function changeEmailSave() {
    var bt = document.getElementById("email-field");
    bt.disabled = true
    document.getElementById("save-email-button").style.visibility = "hidden";
    document.getElementById("cancel-email-button").style.visibility = "hidden";
}

function changePassword() {
    var bt = document.getElementById("password-field");
    if (bt.disabled = true) {
        bt.disabled = false;
        bt.placeholder = "";
    }
}