##BASIC GAME STRUCTURE##
label act1:
    show screen map_icon

    show screen journal_icon

    while True :
        jump garden

##MAP SYSTEM##
#Keep track of which location has been visited already
#So we display a different message the second time you go there
default garden_visited = False
default mortuary_visited = False
default scriptorium_visited = False
default archives_visited = False
default crypt_visited = False

#Map Icon functionality
screen map_icon:
    zorder 10
    imagebutton:
        xcenter 1810
        ycenter 110
        idle "icon map.png"
        hover "icon map hovered.png"
        at custom_zoom
        action Jump("open_map")

transform custom_zoom:
    zoom 0.1875

label open_map:
    scene bg map
    nvl clear
    menu:
     "Where should I go ?"

     "Garden with the Abbot":
         jump garden

     "Mortuary with Brother Galeazzo":
         jump mortuary

     "Scriptorium with Brother Conrad":
         jump scriptorium

     "Archives of the Societa Templois" if archives_known:
         jump archives

     "Crypt" if crypt_known:
         jump garden

###MAP-HIDDEN LOCATIONS SYSTEM###
#Not all locations are known initially

#Archives are hidden by default
default archives_known = False

#Call this label when someone mentions them
label archives_mentioned:
    #Normally should onlny be called once, but to be sure
    if archives_known:
        return

    $ archives_known = True
    "(New location unlocked : Archives of the Societa Templois)"
    $ journal.append("The archives of a former knight order called the 'Societa Templois' are stored in the abbey's basement.")
    return

#Crypt is hidden by default
default crypt_known = False

#Call this label when someone mentions it
label crypt_mentioned:
    #Normally should onlny be called once, but to be sure
    if crypt_known:
        return

    $ crypt_known = True
    "(New location unlocked : Crypt)"
    $ journal.append("Otto der Fröhliche von Habsburg and Leopold II von Habsburg both died at the abbey recently. They are burried in the Abbey's Crypt.")
    return

##JOURNAL SYSTEM##
#Initial Entries of the Journal
define journal = [
    "20th of December 1344 Abbey of Neuberg\n(Austrian Alps, Holy Roman Empire)",
    "I have been hired to investigate the death of Friedrich II von Habsburg duke of Austria",
    "He died at the Abbey 9 days ago"
]

#Journal Icon functionality
screen journal_icon:
    zorder 10
    imagebutton:
        xcenter 1810
        ycenter 280
        idle "icon journal.png"
        hover  "icon journal hovered.png"
        at custom_zoom
        action Call("open_journal")

#When you open the journal we display the few journal entries
label open_journal:
    nvl clear
    define j = Character(kind=nvl)
    python :
        for entry in journal:
            j("[entry]{nw}")
        j(" ")

    return

##JOURNAL SYSTEM-CLUES##
define missing_heart_known = False

#Call this label when someone mentions it
label missing_heart_mentioned:
    #Normally should onlny be called if not known yet, but in case of
    if missing_heart_known:
        return

    $ missing_heart_known = True

    "(This is an important clue !)"
    $ journal.append("Friedrich II's heart has been removed post mortem ! This is a proof that someone wanted him dead.")
    call missing_heart_mentioned
