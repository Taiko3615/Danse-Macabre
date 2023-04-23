label act2_mortuary:
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
    facts= act2_facts,
    npc_name_and_title="Brother Galeazzo, you are a doctor"
    ,
    npc_knows_ok_to_say="""
    You are currently in the Mortuary.
    The corpse (or body) of Friedrich II is in front of you covered by a covered by a flag bearing the Habsburg coat of arms.
    The air of the Mortuary is full of incense because you had to leave the body there for 9 days.
    The heart of Friedrich II is missing, which is horrible. It was removed post mortem.
    When you collected the body, the heart was still there, this removal happened post mortem.
    Some rare herbs are missing from your storage, they were there few hours ago ! Those can be used to make poisons !
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
                    control_phrase="the NPC mentioned the missing rare herbs used to make poisons or he mentions they disappeared few hours ago",
                    #Which label should be called if this action happens
                    callback= "missing_poison_ingredients_mentioned_at_mortuary",
                    #We only activate this controller if the missing herbs are not known yet
                    activated = not missing_poison_ingredients_known
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
    show galeazzo normal with dissolve

    "(You are back in the mortuary in front of Brother Galeazzo)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("Greetings, I am Brother Galeazzo, the abbey's doctor. Quomodo te adiuvare possum?", False)

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
label missing_poison_ingredients_mentioned_at_mortuary:
    "Brother Galeazzo informs you that some rare herbs used to make poisons have gone missing from the mortuary."
    "He explains that they were present just a few hours ago before he went for lunch, but they have now disappeared."
    "This is very troubling !"
    call missing_poison_ingredients_mentioned from _call_missing_poison_ingredients_mentioned
