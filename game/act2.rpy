##BASIC GAME STRUCTURE##
label act2:
    hide screen map_icon

    "ACT2 INTRO"

    show screen map_icon_act2

    #We reset the journal
    $ journal = [
        "20th of December 1344 Abbey of Neuberg\n(Austrian Alps, Holy Roman Empire)",
        "I have been hired to investigate the death of Friedrich II von Habsburg duke of Austria",
        "He died at the Abbey 9 days ago, he was poisoned"
        "The heart of all three dukes : Friedrich II, Otto der Fröhliche and Leopold II von Habsburg are missing ! This is a proof of not one, but three murders !"
        "Someone sabotaged the bridges, there is no way out of here !"
    ]

    while True :
        jump act2_mortuary#act2_entrance

##MAP SYSTEM##
#Keep track of which location has been visited already
#So we display a different message the second time you go there
default kitchen_visited = False
default chapel_visited = False
default library_visited = False

#Map Icon functionality
screen map_icon_act2:
    zorder 10
    imagebutton:
        xcenter 1810
        ycenter 110
        idle "icon map.png"
        hover "icon map hovered.png"
        activate_sound "audio/click.mp3"
        at transform:
            zoom 0.1875
        action Jump("open_map_act2")

label open_map_act2:
    scene bg map
    nvl clear
    menu:
     "Where should I go ?"

     "Entrance of the Abbey":
         jump act2_mortuary#act2_entrance

     "Mortuary with Brother Galeazzo":
         jump act2_mortuary

     "Scriptorium with Brother Conrad":
         jump act2_mortuary#act2_scriptorium

     "Kitchen with Brother Eudes" if kitchen_known:
         jump act2_mortuary#act2_kitchen

     "Chapel with Brother Ambrose" if chapel_known:
         jump act2_mortuary#act2_chapel

     "Library" if library_known:
         jump act2_mortuary#act2_library

     "Archives of the Societa Templois":
         jump archives

###MAP-HIDDEN LOCATIONS SYSTEM###
#Not all locations are known initially

#Call this label when someone mentions them
default chapel_known = False

label chapel_mentioned:
    if chapel_known:
        return

    $ chapel_known = True
    "(New location unlocked: Chapel)"
    return

default library_known = False

label library_mentioned:
    if library_known:
        return

    $ library_known = True
    "(New location unlocked: Library)"
    return


default kitchen_known = False

label kitchen_mentioned:
    if kitchen_known:
        return

    $ kitchen_known = True
    "(New location unlocked: Kitchen)"
    return

##JOURNAL SYSTEM-CLUES##
define monks_dont_attend_mass_known = False
define illegible_writing_known = False
define monks_wandering_known = False
define messy_rooms_known = False
define messy_library_known = False
define missing_poison_ingredients_known = False
define monks_not_eating_known = False

# Call this label when someone mentions it
label monks_dont_attend_mass_mentioned:
    if monks_dont_attend_mass_known:
        return

    $ monks_dont_attend_mass_known = True
    "(This is an important clue !)"
    $ journal.append("Some monks don't attend mass, this is unacceptable!")
    return

label illegible_writing_mentioned:
    if illegible_writing_known:
        return

    $ illegible_writing_known = True
    "(This is an important clue !)"
    $ journal.append("Some scribes' writings is barely legible.")
    return

label monks_wandering_mentioned:
    if monks_wandering_known:
        return

    $ monks_wandering_known = True
    "(This is an important clue !)"
    $ journal.append("Some monks seem lost in thoughts, and are caught wandering in the corridors aimlessly.")
    return

label messy_rooms_mentioned:
    if messy_rooms_known:
        return

    $ messy_rooms_known = True
    "(This is an important clue !)"
    $ journal.append("Some monks don't tidy their cells.")
    return

label messy_library_mentioned:
    if messy_library_known:
        return

    $ messy_library_known = True
    "(This is an important clue !)"
    $ journal.append("Most library books are in the wrong shelves.")
    return

label missing_poison_ingredients_mentioned:
    if missing_poison_ingredients_known:
        return

    $ missing_poison_ingredients_known = True
    "(This is an important clue !)"
    $ journal.append("Lots of rare herbs that can be used to make poisons have been stolen in the last few hours at the mortuary.")
    return

label monks_not_eating_mentioned:
    if monks_not_eating_known:
        return

    $ monks_not_eating_known = True
    "(This is an important clue !)"
    $ journal.append("Lots of monks miss meal times or don't eat when they attend.")
    return
