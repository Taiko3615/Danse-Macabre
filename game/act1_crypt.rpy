label crypt:
    # Import the NPC module
    $ import npc

    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    # Set the background scene to the location with a dissolve transition
    scene bg crypt with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = gm_prompt_template.format(
    facts= act1_facts,
    gm_current_situation = "I am currently exploring the crypt of the abbey of Neuberg where Both Otto der Fröhliche and Leopold II von Habsburg are burried."
    ,
    gm_knows_ok_to_say = """
    It is a very solemn crypt with a massive statue of Otto der Fröhliche in armor, and it’s written below : Otto slaying the heretics. Lots of candles and gifts in front of him. One Monk is crying, this family was the abbey’s only protectors, what will happen now ?"""
    ,
    gm_actions = """
    If I want to exhume or inspect the body of Otto der Fröhliche or Leopold II respond this exact meaning : It would be highly improper and the monks will never allow it.
"""
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
                    control_phrase="I requested to leave the Crypt or I am not in the Crypt anymore.",
                    #Which label should be called if this action happens
                    callback= "leaving_crypt",
                    #We only activate this controller if the missing heart is not known yet
                    activated = True
                     )
            ],

        # Set the proxy server for the NPC to use
        proxy=proxy
    )

    # Check if the location has been visited before
    if not crypt_visited:
        "(In this sequence you are not talking to any Character in particular, you have to describe what you do and the game will react accordingly)"
    else:
        "(You are back in the crypt)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("""As you enter the solemn crypt of the Neuberg Abbey, a feeling of reverence descends upon you.
At the center of the room stands a massive statue of Otto der Fröhliche in full armor, towering over the visitors.
Below the statue, it is written "Otto slaying the heretics", a reminder of the late ruler's role in the holy military order.
You notice that there are numerous candles and gifts placed in front of the statue, a sign of the reverence and devotion that the people of the abbey had for their protectors.
As you look around, you see a monk crying in the corner, clearly distressed by the loss of this branch of the Habsburg family."""
    ,
    #Display this message only the first time
    not crypt_visited
    )

    # Set the location flag to True
    $ crypt_visited = True

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
label leaving_crypt:
    "(To leave the crypt you should click on the Map Icon on the top right.)"
    jump crypt
