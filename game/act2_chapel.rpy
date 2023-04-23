label act2_chapel:
    # Import the NPC module
    $ import npc

    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the location with a dissolve transition
    scene bg chapel with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = npc_prompt_template.format(
    facts= act2_facts,
    npc_name_and_title="Father Ambrose, you are a priest"
    ,
    npc_knows_ok_to_say="""
    You are currently in the Chapel. Preparing for your next service.
    This time you will make a service on the topic of self sacrifice in the memory of Friedrich II because his young death is not unlike that of the Christ who sacrified himself to carry our sins.
    """
    ,
    npc_knows_afraid_to_say="""
    You are very worried about the other monks, a lot of them seem very burnout.
    They don't attend mass on time, they arrive very early or very late or not at all.
    Some just stare blankly without really following the service.
    Something is very wrong in this abbey but you don't understand what.
    Deep down you belive it is the devil's work, it has to be !
    """
    ,
    npc_personality="""
    You are very charismatic, speak very loud and with authority.
    """
    ,
    npc_speaking_style="Your answers should be maxium three sentences long, you quote the bible all the time."
    )

    # Initialize the current NPC character
    $ curr_npc = npc.NPC(
        # Set the character name and display style
        character=Character("Ambrose"),

        # Set the instructions for the NPC's behavior and knowledge
        prompt = npc_prompt,

        controllers = [
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC mentioned that some monks don't attend mass",
                    #Which label should be called if this action happens
                    callback= "monks_dont_attend_mass_mentioned",
                    #We only activate this controller if the missing herbs are not known yet
                    activated = not monks_dont_attend_mass_known
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

    # Display the NPC'snormal sprite
    show ambrose normal with dissolve

    # Check if the location has been visited before
    if not chapel_visited:
        "You enter the serene, candlelit Chapel, where Father Ambrose prepares for his next service."
        "He is a tall, imposing figure with a mane of silver hair and a resonant voice that fills the sacred space."
        "He moves with purpose, his every gesture imbued with authority and conviction. His eyes, bright with fervor, hold a commanding presence."
    else:
        "(You are back in the chapen in front of Father Ambrose)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("Ah, my child, welcome! 'For where two or three are gathered together in my name, there am I in the midst of them' (Matthew 18:20). I am Father Ambrose, shepherd of this humble flock.", not chapel_visited)

    # Set the location flag to True
    $ chapel_visited = True

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
