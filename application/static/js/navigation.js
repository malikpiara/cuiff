/* Start of Workspace Dropdown */

// Get the element that opens the workspace dropdown
var workspace_dropdown = document.getElementById('workspace-dropdown')
var workspace_selector = document.getElementById('workspace-selector')

// When the user clicks the element, open the dropdown
workspace_selector.onclick = function() {
  workspace_dropdown.style.display = "block";
}

// Detect all clicks on the document
document.addEventListener("click", function(event) {

  // If user clicks on the element, display workspace dropdown
	if (event.target.closest("#workspace-selector"))
    workspace_dropdown.style.display = "block";
    workspace_dropdown.classList.remove("js-is-hidden");

  if (!event.target.closest("#workspace-selector"))
  workspace_dropdown.classList.add("js-is-hidden");
  return;
});

/* End of Workspace dropdown */