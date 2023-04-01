label mortuary:
    # Import the NPC module
    $ import npc

    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the location with a dissolve transition
    scene bg mortuary with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = npc_prompt_template.format(
    facts= act1_facts,
    npc_name_and_title="Brother Galeazzo, you are a doctor"
    ,
    npc_knows_ok_to_say="""
    You are currently in the Mortuary.
    The corpse (or body) of Friedrich II is in front of you covered by a covered by a flag bearing the Habsburg coat of arms.
    The air of the Mortuary is full of incense because you had to leave the body there for 9 days.
    The first time (only the first time) I ask you about the cause of death or I ask to inspect the body you will respond this exact sentence : "Let's see. Red eyes and swollen tongue. Cause of death is clearly poison,potentially self-inflicted. Yet we mustn't jump to conclusions. This... This is horrifying. There's a scar on his chest, and his heart is missing! What in the world happened here?. It was removed recently because I don't remember seeing this scar when I first collected the body. Homo homini lupus est."
    When you collected the body, the heart was still there, this scar happened post mortem.
    """
    ,
    npc_knows_afraid_to_say="""
    You analysed the poison used, it is The Composition of Death, red copper, nitric acid, verdigris, arsenic, oak bark, rose water and black soot. A poison very complex and expensive to produce.
    You personally don't know how to produce the Composition of Death and you don't have the ingredients.
    You don't know if anyone has this knowledge in the Abbey or where to find those ingredients.
    You have black spots on your face because you caugth a strange disease few years ago.
    """
    ,
    npc_personality="""
    You are very educated and want people to know it. So you always quote Latin as much as you can.
    """
    ,
    npc_speaking_style="""Your answers should be maxium three sentences long, in a very educated tone, always end your responses with a quote in Latin."""
    )

    # Initialize the current NPC character
    $ curr_npc = npc.NPC(
        # Set the character name and display style
        character=Character("Galeazzo"),

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
                     ),
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC mentioned the scar on the chest of the body or he mentioned that his heart is missing or he mentions that he is starting a more thorough investigation or removing the shroud",
                    #Which label should be called if this action happens
                    callback= "missing_heart_at_mortuary",
                    #We only activate this controller if the missing heart is not known yet
                    activated = not missing_heart_known
                     )
            ],

        # Set the proxy server for the NPC to use
        proxy=proxy
    )

    # Display the NPC'snormal sprite
    show galeazzo normal with dissolve

    # Check if the location has been visited before
    if not mortuary_visited:
        "Upon entering the mortuary, you notice the air is filled with incense and lit by flickering candles, casting shadows on cold stone walls."

        "Friedrich II von Habsburg's shrouded body lies in the center, covered by a flag bearing the Habsburg coat of arms. The solemn atmosphere is palpable as Brother Galeazzo prepares the body for burial."

        "You approach the table to inspect the body, feeling solemnity and respect for the young man who met an untimely end."
    else:
        "(You are back in the mortuary in front of Brother Galeazzo)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("Greetings, I am Brother Galeazzo, the abbey's doctor. Quomodo te adiuvare possum?", not mortuary_visited)

    # Set the location flag to True
    $ mortuary_visited = True

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

#Call this label when someone mentions it
label missing_heart_at_mortuary:
    "You open the shroud covering the body and you are horrified to discover a massive scar on his chest !"
    "His heart has been removed !"
    "The doctor says that this scar wasn't present when he first collected the body, it was removed post mortem."
    call missing_heart_mentioned from _call_missing_heart_mentioned
