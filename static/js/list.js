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
    var close = document.createElement("button");
    var closeNode = document.createTextNode("close");
    close.appendChild(closeNode);
    li.appendChild(close);
    close.className = "close material-symbols-outlined";
  }
}

//have X remove list item on click
document.addEventListener("click", function (event) {
  if (event.target.className == "close material-symbols-outlined")
    event.target.parentElement.style.display = "none";
});

//when an li is clicked toggle class which either adds or removes linethrough
document.addEventListener("click", function (event) {
  if (event.target.tagName == "LI") event.target.classList.toggle("check");
});
