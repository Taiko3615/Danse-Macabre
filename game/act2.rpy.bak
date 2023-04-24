##BASIC GAME STRUCTURE##
label act2:
    hide screen map_icon
    hide screen journal_icon

    play sound "audio/big_tree_fall_in_forest.ogg"

    "(You hear a thunderous crashing noise echoing in the distance)"

    define unknown = Character("?????")
    unknown "THE BRIDGE! THE BRIDGE! HELP!"

    scene bg broken bridge with dissolve

    show abbot normal at left with dissolve

    show galeazzo normal at right with dissolve
    define abbot = Character("Abbot")
    define galeazzo = Character("Galeazzo")
    galeazzo "Reverend Father, what happened?"

    abbot "I heard a great noise and, upon looking, I saw the bridge destroyed!"
    abbot "We find ourselves trapped!"

    galeazzo "Numerous paths lead to the monastery, yet only one requires traversal of a bridge."

    abbot "Indeed, but not during winter. Have you forgotten the avalanche from a mere week ago?"
    abbot "We are now utterly secluded! No way in, no way out !"
    abbot "That is, unless one possesses exceptional climbing skills."

    galeazzo "This situation is indeed most disconcerting."

    abbot "I must summon aid at once!"
    abbot "Brother de Vermont, Brother Basile, accompany me!"
    abbot "A settlement lies nearby; they may offer assistance."
    abbot "The ascent shall take hours, but we shall arrive ere the morrow."

    hide abbot normal at left with dissolve

    galeazzo "Inquisitor, gratias Deo quod ades. Thank God you are here!"
    galeazzo "Graviora manent. I beseech you to assist us!"
    galeazzo "This bridge underwent renovations but a month prior; it seems implausible that its collapse coincided with your arrival by mere chance."
    galeazzo "Nos precamur te, quaesumus, adiuvandi causa investiga. (We beseech you, we ask, to help us investigate the cause.)"

    "(Surely, this is no mere coincidence. There must be an individual striving to obstruct our quest for truth.)"
    "(It has become imperative to examine the entirety of the abbey, as numerous disconcerting occurrences have come to light.)"

    #We reset the journal
    $ journal = [
        "20th of December 1344 Abbey of Neuberg\n(Austrian Alps, Holy Roman Empire)",
        "I have been hired to investigate the death of Friedrich II von Habsburg duke of Austria",
        "He died at the Abbey 9 days ago, he was poisoned",
        "The heart of all three dukes : Friedrich II, Otto der Fröhliche and Leopold II von Habsburg are missing ! This is a proof of not one, but three murders !",
        "Someone sabotaged the bridges, there is no way out of here !",
        "I must examine the entirety of the abbey, as numerous disconcerting occurrences have come to light."
    ]

    show screen journal_icon
    show screen map_icon_act2

    while True :
        jump act2_entrance

##MAP SYSTEM##
#Keep track of which location has been visited already
#So we display a different message the second time you go there
default entrance_visited = False
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
         jump act2_entrance

     "Mortuary with Brother Galeazzo":
         jump act2_mortuary

     "Scriptorium with Brother Conrad":
         jump act2_scriptorium

     "Kitchen with Brother Eudes" if kitchen_known:
         jump act2_kitchen

     "Chapel with Father Ambrose" if chapel_known:
         jump act2_chapel

     "Library" if library_known:
         jump act2_library

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
    call count_clues
    return

label illegible_writing_mentioned:
    if illegible_writing_known:
        return

    $ illegible_writing_known = True
    "(This is an important clue !)"
    $ journal.append("Some scribes' writings is barely legible.")
    call count_clues
    return

label monks_wandering_mentioned:
    if monks_wandering_known:
        return

    $ monks_wandering_known = True
    "(This is an important clue !)"
    $ journal.append("Some monks seem lost in thoughts, and are caught wandering in the corridors aimlessly.")
    call count_clues
    return

label messy_rooms_mentioned:
    if messy_rooms_known:
        return

    $ messy_rooms_known = True
    "(This is an important clue !)"
    $ journal.append("Some monks don't tidy their cells.")
    call count_clues
    return

label messy_library_mentioned:
    if messy_library_known:
        return

    $ messy_library_known = True
    "(This is an important clue !)"
    $ journal.append("Most library books are in the wrong shelves.")
    call count_clues
    return

label missing_poison_ingredients_mentioned:
    if missing_poison_ingredients_known:
        return

    $ missing_poison_ingredients_known = True
    "(This is an important clue !)"
    $ journal.append("Lots of rare herbs that can be used to make poisons have been stolen in the last few hours at the mortuary.")
    call count_clues
    return

label monks_not_eating_mentioned:
    if monks_not_eating_known:
        return

    $ monks_not_eating_known = True
    "(This is an important clue !)"
    $ journal.append("Lots of monks miss meal times or don't eat when they attend.")
    call count_clues
    return

#Count the number of clues found, when we reach a certain level, we win this act
label count_clues:
    define a = 0
    $ if monks_dont_attend_mass_known: a = a+1
    $ if illegible_writing_known: a = a+1
    $ if monks_wandering_known: a = a+1
    $ if messy_rooms_known: a = a+1
    $ if messy_library_known: a = a+1
    $ if missing_poison_ingredients_known: a = a+1
    $ if monks_not_eating_known: a = a+1

    if a >= 5:
        "There is something heretical about this abbey"
        "Monks not attending mass ? Scribes unable to write ?"
        "This can only be the work of the devil"
        "END OF ACT 2"
        "Wait few weeks for ACT 3 :-)"
        "You can keep playing in the meantime, but you have discovered everything that needed to be."

    $ a = 0
