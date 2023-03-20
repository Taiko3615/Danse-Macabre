
#The game is in NVL mode, meaning the text fills the screen
define narrator = nvl_narrator

include "intro.rpy"
include "tutorial.rpy"
include "garden.rpy"

#Not all locations are known initially
default archives_known = False
default crypt_known = False

#Keep track of which location has been visited already
default garden_visited = False
default mortuary_visited = False
default scriptorium_visited = False
default archives_visited = False
default crypt_visited = False

label start:

    #Let's start with the intro
    #call intro

    #Now the tutorial
    #call tutorial

    show screen map

    while True :
        jump garden

    return

#Map Icon an functionality
screen map:
    zorder 10
    imagebutton:
        xpos 1800
        ypos 10
        idle "map.png"
        at custom_zoom
        action Jump("chose_location")

transform custom_zoom:
    zoom 0.2

label chose_location:
    scene bg map
    nvl clear
    menu:
     "Where should I go ?"

     "Garden with the Abbot":
         jump garden

     "Mortuary with Brother Galeazzo":
         jump garden

     "Scriptorium with Brother Conrad":
         jump garden

     "Archives of the Societa Templois" if archives_known:
         jump garden

     "Crypt" if crypt_known:
         jump garden
