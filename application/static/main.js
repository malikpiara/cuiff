/* Start of Workspace Dropdown */

// Get the element that opens the workspace dropdown
var workspace_dropdown = document.getElementById('workspace-dropdown')
var workspace_selector = document.getElementById('workspace-selector')

// When the user clicks the element, open the dropdown
workspace_selector.onclick = function() {
  workspace_dropdown.style.display = "block";
}

/* End of Workspace dropdown */

// Get the modal
var modal = document.getElementById("new-board-modal");
var new_space_modal = document.getElementById("new-space-modal");

// Get the button that opens the modal
var btn = document.getElementById("board-add");
var new_space_btn = document.getElementById("space-add");

// Get the <span> element that closes the modal
var new_board_span = document.getElementsByClassName("close")[0];
var new_space_span = document.getElementsByClassName("close")[1];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

new_space_btn.onclick = function() {
  new_space_modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
new_board_span.onclick = function() {
  modal.style.display = "none";
}

new_space_span.onclick = function() {
  new_space_modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
  if (event.target == new_space_modal) {
    new_space_modal.style.display = "none";
  }
}

// Navigation Dropdown
var nav_dropdown = document.getElementsByClassName("nav-dropdown")[0];

var box = document.querySelector(".nav-dropdown");

// Detect all clicks on the document
document.addEventListener("click", function(event) {
	// If user clicks on the button, display dropdown
	if (event.target.closest("#create-btn"))
    nav_dropdown.style.display = "block";
    box.classList.remove("js-is-hidden");

  if (!event.target.closest("#create-btn"))
    box.classList.add("js-is-hidden");

  // If user clicks on the element, display workspace dropdown
	if (event.target.closest("#workspace-selector"))
    workspace_dropdown.style.display = "block";
    workspace_dropdown.classList.remove("js-is-hidden");

  if (!event.target.closest("#workspace-selector"))
  workspace_dropdown.classList.add("js-is-hidden");
  return;
});