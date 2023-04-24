label act2_library:
    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the location with a dissolve transition
    scene bg library with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = gm_prompt_template.format(
    facts= act2_facts,
    gm_current_situation = "I am currently in the Library of the abbey. There is nobody expect me in the library at the moment."
    ,
    gm_knows_ok_to_say = """
    I am in the famous Library of the Abbey, three levels of rare books on varying topics. The two first levels are open to everyone and the third need a special permission, but I was allowed to go.
    I am not in the Archives of the Societa Templois"""
    ,
    gm_actions = """
    If I want to read some books : I realise that most books are on the wrong shelves !
    If I want to leave the Library : 'You need to use the map to go to another location'
    If I want to enter any of those locations the Chapel, the Kitchen, the Mortuary or the Scriptorium : 'You need to use the map to go to another location'"""
    ,
    gm_speaking_style = "Your answers will be very descriptive and three sentences long in a very educated writing style."
    )

    # Initialize the current NPC character
    $ curr_npc = npc.NPC(
        # Set the character name and display style
        character=Character(),

        # Set the instructions for the NPC's behavior and knowledge
        prompt = npc_prompt,

        controllers = [
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="I requested to leave the Library or I am not in the Library anymore.",
                    #Which label should be called if this action happens
                    callback= "leaving_library",
                    #We only activate this controller if the missing heart is not known yet
                    activated = True
                 ),
                 npc.Controller(
                     #The condition which this controller is Checking for
                     control_phrase="the NPC or Gamemaster mentioned that the books are on the wrong shelves",
                     #Which label should be called if this action happens
                     callback= "messy_library_discovered",
                     #We only activate this controller if the missing herbs are not known yet
                     activated = not messy_library_known
                 ),
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC or Gamemaster mentioned the Chapel of the abbey or Father Ambrose",
                    #Which label should be called if this action happens
                    callback= "chapel_mentioned",
                    #We only activate this controller if the missing herbs are not known yet
                    activated = not chapel_known
                ),
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC or Gamemaster mentioned the Library of the abbey",
                    #Which label should be called if this action happens
                    callback= "library_mentioned",
                    #We only activate this controller if the missing herbs are not known yet
                    activated = not library_known
                ),
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC or Gamemaster mentioned the Kitchen of the abbey or Brother Eudes",
                    #Which label should be called if this action happens
                    callback= "kitchen_mentioned",
                    #We only activate this controller if the missing herbs are not known yet
                    activated = not kitchen_known
                )

            ],

        # Set the proxy server for the NPC to use
        proxy=proxy
    )

    # Check if the location has been visited before
    if not library_visited:
        "(In this sequence you are not talking to any Character in particular, you have to describe what you do and the game will react accordingly)"
    else:
        "(You are back in the Library)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("""You step into the magnificent Abbey Library, a grand repository of knowledge spanning three levels and housing a wealth of rare books. The first two levels are open to the public, offering an extensive array of texts that draw scholars and seekers of wisdom from near and far. The polished wooden shelves overflow with ancient tomes, illuminated manuscripts, and scrolls that whisper the secrets of the ages. Thanks to a special authorization you've obtained, you also have access to the exclusive third level, a restricted sanctum filled with the most precious and arcane volumes. This hidden treasure trove promises unparalleled insights and mysteries, igniting a sense of excitement within you as you prepare to explore its hidden depths."""
    ,
    #Display this message only the first time
    not library_visited
    )

    # Set the location flag to True
    $ library_visited = True

    # Begin the main conversation loop
    while True:
        # Get input from the user
        $ user_input = renpy.input("What do you do ?", length=150)

        # Process the user input and display the NPC's response
        $ curr_npc.user_says(user_input)

        #After the conversation, the NPC has perhaps some callbacks that needs to be called
        #There's a super super weird bug when we are inside a python "while" loop, the "Call" function doesn't work as intended
        #But as long as we are inside a "Ren'Py" while loop, all is ok.
        #So we have no choice but to do the loop here
        #Yes I agree it's stupid but no choice
        while curr_npc.callbacks:
            $ renpy.call(curr_npc.callbacks.pop(0))

        #Lots of bugs with history, so we clear it each times
        $ _history_list = []

#Call this label when someone mentions it
label leaving_library:
    "(To go somewhere you should click on the Map Icon on the top right.)"
    jump act2_library


label messy_library_discovered:
    "The volumes are misplaced throughout the shelves! Theological works are found intermingled with the fiction section, while alchemical treatises are misplaced among the forbidden texts."
    "Reorganizing this library will be a painstaking task, taking months to complete and rendering it unusable in the interim. Such disarray is utterly inconceivable for a distinguished library like the one at Neuberg Abbey."
    call messy_library_mentioned
