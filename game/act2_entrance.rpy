label act2_entrance:
    # Import the NPC module
    $ import npc

    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the location with a dissolve transition
    scene bg garden with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = gm_prompt_template.format(
    facts= act2_facts,
    gm_current_situation = "I am currently in front of the Abbey, in the garden. There is nobody expect me in the garden at the moment."
    ,
    gm_knows_ok_to_say = """
    I am in front of the once mighty Neuberg abbey, which seems to be victim of a dark conspiracy of some sort.
    The ambiance is very heavy as all monks are in mourning and in shock."""
    ,
    gm_actions = """
    If I want to visit the corridors of the abbey respond this exact meaning : I can observe several monks wandering the passageways with no apparent purpose, appearing utterly exhausted. When questioned about their activities, they can hardly muster a response, clearly preoccupied by their thoughts.
    If I want to visit the monks cells : I discover that some of the cells are in a state of disarray, appearing as if they have not been cleaned or tidied for weeks. Such conditions are absolutely intolerable within the walls of an abbey.
    If I want to leave the abbey : I can't, I need to investigate here and anyway the bridge is destroyed
    If I want to enter any of those locations the Chapel, the Library, the Kitchen, the Mortuary or the Scriptorium : 'You need to use the map to go to another location'"""
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
                    control_phrase="I requested to leave the Abbey or I am not in the Abbey anymore.",
                    #Which label should be called if this action happens
                    callback= "leaving_abbey",
                    #We only activate this controller if the missing heart is not known yet
                    activated = True
                 ),
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="I requested to enter or I am in the Chapel, the Library, the Kitchen, the Mortuary or the Scriptorium",
                    #Which label should be called if this action happens
                    callback= "leaving_abbey",
                    #We only activate this controller if the missing heart is not known yet
                    activated = True
                 ),
                 npc.Controller(
                     #The condition which this controller is Checking for
                     control_phrase="the NPC or Gamemaster mentioned some monks wandering in the alleys without purpose and seemingly lost in thoughts",
                     #Which label should be called if this action happens
                     callback= "monks_wandering_discovered",
                     #We only activate this controller if the missing herbs are not known yet
                     activated = not monks_wandering_known
                 ),
                 npc.Controller(
                     #The condition which this controller is Checking for
                     control_phrase="the NPC or Gamemaster mentioned that some cells are messy",
                     #Which label should be called if this action happens
                     callback= "messy_rooms_discovered",
                     #We only activate this controller if the missing herbs are not known yet
                     activated = not messy_rooms_known
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
    if not entrance_visited:
        "(In this sequence you are not talking to any Character in particular, you have to describe what you do and the game will react accordingly)"
        "You find yourself at the entrance of the once-peaceful abbey garden, now shrouded in a foreboding atmosphere."
        "The once-vibrant foliage and blooming flowers seem muted, as if they too are grieving the recent tragedies. The usual symphony of birdsong and rustling leaves is eerily absent, replaced by a heavy silence that hangs in the air."
    else:
        "(You are back in front of the Abbey)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("""The garden appears to be abandoned, as the Abbot has left in search of help following the discovery of three grisly murders and the sabotaged bridge. A somber cloud of unease looms over the entire abbey, casting a pall upon its once-hallowed grounds."""
    ,
    #Display this message only the first time
    not entrance_visited
    )

    # Set the location flag to True
    $ entrance_visited = True

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
label leaving_abbey:
    "(To go somewhere you should click on the Map Icon on the top right.)"
    jump act2_entrance


label monks_wandering_discovered:
    "Several monks meander through the corridor, seemingly adrift in contemplation. When engaged, their responses are barely legible."
    "How disconcerting this is!"
    call monks_wandering_mentioned

label messy_rooms_discovered:
    "At the core of monastic existence lies order and discipline."
    "You are shocked to find that some of the cells are in disarray!"
    call messy_rooms_mentioned
