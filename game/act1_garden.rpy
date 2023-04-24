label garden:
    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the garden with a dissolve transition
    scene bg garden with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = npc_prompt_template.format(
    facts= act1_facts,
    npc_name_and_title="Reverend Father Albrecht, you are the Abbot of this abbey"
    ,
    npc_knows_ok_to_say="""
    You are currently in the Garden.
    You do not know if the body has any traces because it was sent to the Mortuary as soon as you found it.
    You then immediately sent a request to the pope for help to investigate this case which is why the player is here.
    You don't know anything about the corpse, if they want to check it they need to go to the mortuary.
    """
    ,
    npc_knows_afraid_to_say="""
    Things became very messy recently, the scribes are doing a worse and worse job, sometimes making obvious mistakes or being very negligent in their work.
    Some monks are missing Mass, which is a grave offence.
    And some monks are seen wandering in the alleys after curfew.
    You do not know why those things happen, everyone seems burnout all the time.
    You are ashamed of yourself and blame yourself for all the woes that happened in the abbey, you doubt if it is a punishment from god.
    """
    ,
    npc_personality="""
    You love gardening, it is his favourite activity.
    You are quite old and he seems lost in thoughts.
    You always carry a rosary and pray even when talking to the player.
    You pray a lot because you are very very worried about what will happen to the abbey now that their most important donors are dead. Almost of the funding of the abbey came from the generous patronage of Otto Leopold and Friedrich.
    """
    ,
    npc_speaking_style="Your answers should be maxium two sentences long in a very educated tone."
    )

    # Initialize the current NPC character
    $ curr_npc = npc.NPC(
        # Set the character name and display style
        character=Character("Abbot"),

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

    # Display the Abbot character's normal sprite
    show abbot normal with dissolve

    # Check if the garden has been visited before
    if not garden_visited:
        "(In this Game, the NPCs are powered by artificial intelligence, they understand what you tell them and will respond accordingly)"
        "(You are currently in the Garden. Click on the top right Map icon to explore other locations and Journal icon to consul your notes)"
        "You approach Reverend Father Albrecht."
        "The Abbot stands tall, his kind face and deep-set eyes suggesting wisdom. His measured steps and long white beard convey authority, and his gnarled hands reveal a life of work. Often found in his beloved garden, he tends to plants and flowers."
        "Speaking to the players, he holds a rosary, beads clicking softly as he prays. His devotion to the abbey and its inhabitants is evident."
    else:
        "(You are back in the garden in front of the Abbot Reverend Father Albrecht)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("Ah, you've arrived. I'm Abbot Reverend Father Albrecht. I'm grateful His Holiness has sent help upon my request.", not garden_visited)

    # Set the garden_visited flag to True
    $ garden_visited = True

    # Begin the main conversation loop
    while True:
        # Get input from the user
        $ user_input = renpy.input("What do you say ?", length=150)

        $ if user_input == "LOZDGV" : renpy.jump("act2")

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
