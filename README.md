# split_upload_doc

## Inspiration of the project:

The inspiration of this program comes from the shear frustration that I faced while uploading my assignments on crowdmark. I usually have a cumulative pdf which contains my entire assignment and then I had to drag through Crowdmark to drop the other questions' solutions. I did try to separately save my assignment into each question pdf and then uploading them, but its time consuming too. So, why not build a program that does it for me.

## Questions the program asks a user:

It asks you a bunch of questions based on your assignment; location of assignment, the link where the assignment is to be uploaded etc. The way they work is:

**1) Select the assignment file in the window that shows up**

**2) Enter start value of questions eg. 13 9 1. It requires user to select the pages on which each question lies. So in the example above; my question 1 starts on 13th page of the cumulative assignment, question 2 starts on the 9th page and question 3 starts on the 1st page. I know its a weird way to do assignments but I figuered, people might do it like that.**

**3) Enter end value of questions eg. 14 12 8. It requires user to select the pages on which each question ends. So in the example above; my question 1 ends on 14th page of the cumulative assignment, question 2 ends on the 12th page and question 3 ends on the 8st page.**

**4) Copy and paste the link of the website in crowdmark where the assignment has to be uploaded**

**5) Enter y/Y if you want the program to even press the submit button for you**

**6) Enter y/Y if you eventually want to delete the individual question pdfs**



##### Note: (2-6) can all be done in 3 different ways. 1st: the user can use `inputs.json` file in `resources` folder; 2nd: the user can use a GUI app built in the program; 3rd: the user can input values through terminal window. To change the different modes of input, the user can go in the main.py and change `input_method` to 1, 2 or 3 depending on the input method type they want.

There are 4 steps currently to how this program runs:

## Step 1: 

The program separates the cumulative assignment into individual question pdfs. The input for this case goes as follows:

<img width="217" alt="image" src="https://user-images.githubusercontent.com/59942900/225540056-279d30ef-750d-49ff-8432-6fcc48fa59a1.png">

The inputs are provided above only, to create a seemless experience. In both inputs, each question value is separates by a space. So the first input looks like: `13 9 1` and the second input looks like `14 12 8`. The program automatically converts these strings to array of numbers.

## Step 2:

The program then opens up a new Chrome browser window and logs into your crowdmark account (currently selected for university of waterloo students).

## Step 3: 

The program submits the individual question pdfs to the input fields on the crowdmark page. It presses the submit button if the user selected y/Y.

## Step 4:

The program deletes the individual question pdfs if the user doesn't want them, thus if the user selected y/Y.
