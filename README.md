# CookPal

#### Video Demo: <https://youtu.be/6F84dSxOzzY>

#### Description:

CookPal is a simple flask web application that allows users to create their own account and share their recipes and cooking tips & tricks for the other users of the website to see.
Recipes & Menus section includes all of the shared recipes that users have shared on this website. The way I implemented this was by querying the 'recipes' table from my database for all the recipes and then, using jinja, list all of the recipes found.
Share your recipe section is where the magic happens as it's the section where users can actually share their recipe. I have implemented this with the help of the HTML forms and inputs and the functionality that Flask provides. The form takes 4 different inputs, for Title, Ingredients, Recipe and Image and if one of the inputs is empty the function in app.py returns an apology (the one found in the finance web app).
The more interesting part is the one regarding the uploading of images. I have solved this problem by saving the image files using Flask in the static folder at 'uploads'. Then, I have saved the filename as TEXT in the database, at the 'image' columns. In the end, in order to show the actual image, I have written HTML code like this src="/static/uploads/{{recipe['image']}}".
For the Cooking Tips & Tricks section and the Share your Tip section everything is very similar to the sections described above so I will not go through these again.
Create your Grocery List is just a simpe javascript script that uses a function AddToList() that it is called every time the add button is pressed. It takes the value from the input box, and appends this value to a list item in the unorderd list.
I have also added two different icons, one (the x icon) for removing an item from the list and one (the check icon) that removes an item from the list and appends the value from that list to another list, the one below the In Cart header.
The account section shows the user his shared recipes/cookings tips and tricks which is provided by querying the database for all recipes and tips WHERE user_id is the id of current user logged in.
The log in, register and log out functions are the ones from the finance web app.
In terms of design, I have written a single css file (found in /static/css) for every html page that can be found in templates folder. I have also tried to make the website fully responsive so that it looks good on all devices, this I have accomplished by using media queries.
