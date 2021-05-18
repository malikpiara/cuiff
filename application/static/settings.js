document.getElementById("edit-name-button").addEventListener("click", changeName);
document.getElementById("cancel-name-button").addEventListener("click", changeNameSave);

document.getElementById("edit-email-button").addEventListener("click", changeEmail);
document.getElementById("cancel-email-button").addEventListener("click", changeEmailSave);

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

// Get the modal
var modal = document.getElementById("password-modal");

// Get the button that opens the modal
var btn = document.getElementById("edit-password-button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}