const options_btn = document.querySelectorAll('.entry-options-container');

const dropdown_content = document.querySelectorAll('.dropdown-content');

console.log(options_btn)

options_btn.forEach(el => el.addEventListener('click', event => {
  console.log(event);
  console.log("Oh no");
  const childElement = el.querySelectorAll(".dropdown-content");
  childElement[0].style.visibility = "visible";
}));

/* 
var options_content = document.getElementsByClassName("options-content");


var dropbtn = document.getElementByClassName("dropbtn");

dropbtn.onclick = function() {
    document.getElementById("myDropdown").classList.toggle("show");
  } */

  window.addEventListener('click', event => {
    dropdowns = document.querySelectorAll(".dropdown-content");
    console.log(event.target)
    dropdowns.forEach(element => {
        console.log(event.target.className)
        if (event.target.className != "entry-options-container") {
            
            if (element.style.visibility = "visible") {
                element.style.visibility = "hidden"
            }
        }
    });
});