label tutorial:

    scene bg neutral

    "Welcome to the Abbey of Neuberg"

    "As your Game Master I'll tell you how to look around."

    "You have a map button on the top right, it shows you the different areas that you can explore."

    "Try clicking on it :"

    screen book:
        imagebutton:
            xpos 190
            ypos 450
            idle "book.png"
            at custom_zoom
            action Jump("livre_recupere")


    transform custom_zoom:
        zoom 0.2

    label livre_recupere:
        "Well done"

    show screen book
