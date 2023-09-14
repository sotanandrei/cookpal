//add  value to list item and have it display

function addToList() {
  //get value from input
  var value = document.getElementById("inputText").value;

  //alert that the text box is empty
  if (value === "") {
    alert("To add an item, type its name into the box");
  } else {
    //create a list item element
    var li = document.createElement("li");
    var textNode = document.createTextNode(value);

    //append value to list item
    li.appendChild(textNode);
    document.getElementById("list").appendChild(li);
    li.className = "item";

    //add an X to each list item
    var close = document.createElement("i");
    li.appendChild(close);
    close.className = "close bi bi-x";

    //add a check to each list item
    var check = document.createElement("i");
    li.appendChild(check);
    check.className = "check bi bi-check";
  }
}

//have X or check remove list item on click
document.addEventListener("click", function (event) {
  if (event.target.className == "close bi bi-x") {
    event.target.parentElement.style.display = "none";
  } else if (event.target.className == "check bi bi-check") {
    event.target.parentElement.style.display = "none";
    var value = event.target.parentElement.textContent;

    //create a list item element
    var li = document.createElement("li");
    var textNode = document.createTextNode(value);

    //append value to list item
    li.appendChild(textNode);
    document.getElementById("cart-list").appendChild(li);
    li.className = "item";
  }
});
