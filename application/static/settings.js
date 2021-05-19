document.getElementById("edit-name-button").addEventListener("click", ()=> activateEditState("name"));
document.getElementById("cancel-name-button").addEventListener("click", ()=> disableEditState("name"));

document.getElementById("edit-email-button").addEventListener("click", ()=> activateEditState("email"));
document.getElementById("cancel-email-button").addEventListener("click", ()=> disableEditState("email"));

function enableField(id) {
  var field = document.getElementById(id)
  field.disabled = false;
}

function disableField(id) {
  var field = document.getElementById(id)
  field.disabled = true;
}

function showButton(id) {
  document.getElementById(id).style.visibility = "visible";
}

function hideButton(id) {
  document.getElementById(id).style.visibility = "hidden";
}

function activateEditState(fieldName) {
  enableField(fieldName + "-field")
  showButton("save-"+fieldName+"-button")
  showButton("cancel-"+fieldName+"-button")
}

function disableEditState(fieldName) {
  disableField(fieldName + "-field")
  hideButton("save-" + fieldName + "-button")
  hideButton("cancel-" + fieldName + "-button")
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