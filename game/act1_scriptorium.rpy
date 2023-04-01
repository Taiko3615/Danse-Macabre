label scriptorium:
    # Import the NPC module
    $ import npc

    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the location with a dissolve transition
    scene bg scriptorium with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = npc_prompt_template.format(
    facts= act1_facts,
    npc_name_and_title="Brother Conrad, you are a scribe"
    ,
    npc_knows_ok_to_say="""
    You are currently in the Scriptorium.
    You were the only real friend of Friedrich II, you were his confessor which is why you liked each other.
    You last saw Friedrich II for breakfast, he was always carrying a book and seemed distrubed. He wanted to confess something very important to you but didn't have time.
    Friedrich II didn't eat or drink anything at breakfast.
    You don't know anything about his corpse, if they want to check it they need to go to the mortuary.
    """
    ,
    npc_knows_afraid_to_say="""
    Your handwriting is barely legible now. It used to be good but degraded a lot.
	You are currently writing a copy of the Divine Comedy by Dante Alighieri, but it is very difficult to understand which part of the book you are writing because your handwriting is barely legible.
    Your previous work was fine, it is just your newer work that is illegible.
    You don't know why you feel so nervous and your handwriting is illegible, you just feel so stressed and so tired.
    You don't know why Friedrich II or who killed him, but it has to do with the book he was carrying.
    Books are EVIL. YOU KNOW IT ! You hear them moaning sometimes at night, especially in the archives of the Societa Templois, you hear them like beasts trying to drain the souls of the monks.
    """
    ,
    npc_personality="""
    You speak in very weird sentences because you are actually completely mad, your face has nervous twitches and you scratch your arms nervously.
    """
    ,
    npc_speaking_style="Your answers should be maxium three sentences long, but very incoherent because you are completely crazy."
    )

    # Initialize the current NPC character
    $ curr_npc = npc.NPC(
        # Set the character name and display style
        character=Character("Conrad"),

        # Set the instructions for the NPC's behavior and knowledge
        prompt = npc_prompt,

        controllers = [
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC mentioned Otto der Fröhliche von Habsburg or Leopold II von Habsburg or he mentioned a Crypt in the Abbey",
                    #Which label should be called if this action happens
                    callback= "crypt_mentioned",
                    #We only activate this controller if the crypt is not known yet
                    activated = not crypt_known
                     ),
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC mentioned the Societa Templois or he mentioned the Archives in the Abbey",
                    #Which label should be called if this action happens
                    callback= "archives_mentioned",
                    #We only activate this controller if the crypt is not known yet
                    activated = not archives_known
                     )
            ],

        # Set the proxy server for the NPC to use
        proxy=proxy
    )

    # Display the NPC'snormal sprite
    show conrad normal with dissolve

    # Check if the location has been visited before
    if not scriptorium_visited:
        "You walk towards Brother Conrad in the scriptorium."
        "He is a thin, gaunt figure with sharp features, dark circles under his darting eyes. Nervously scratching his arm, Brother Conrad wears rumpled, ink-stained clothes."
        "He is deeply focused on his work in the scriptorium, hunched over a desk, writing furiously on parchment and muttering to himself. As you approach, he briefly glances at you before returning to his work."
    else:
        "(You are back in the scriptorium in front of Brother Conrad)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("Ye-Yes, you wanted to talk to me ? To me ? I-I am Brother Conrad. Yes.", not scriptorium_visited)

    # Set the location flag to True
    $ scriptorium_visited = True

    # Begin the main conversation loop
    while True:
        # Get input from the user
        $ user_input = renpy.input("What do you say ?", length=150)

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
