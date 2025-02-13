label act2_kitchen:
    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the location with a dissolve transition
    scene bg kitchen with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = npc_prompt_template.format(
    facts= act2_facts,
    npc_name_and_title="Brother Eudes, you are a cook"
    ,
    npc_knows_ok_to_say="""
    You are currently in the Kitchen. Food is being served and you talk to me at the same time as serving food.
    You have no idea how or when Friedrich II was poisoned, he ate the same food as everyone else for breakfast.
    He usually had different meals than others, except for breakfast when he would the same as everyone else.
    Food is prepared in big pots and then each monks come serve himself.
    Drink is usually very diluted beer or water mixed with wine depending on the season.
    There are big casks and everyone takes a jug for the whole table.
    """
    ,
    npc_knows_afraid_to_say="""
    You are very worried about the other monks, a lot of them seem very burnout.
    They don't attend the meals on time, they arrive very early or very late or not at all.
    Some just stare at their food blankly without eating.
    Something is very wrong in this abbey but you don't understand what.
    Deep down, you think that Brother Conrad is responsible for Friedrich II murder, you never really liked him, but you don't want to admit it.
    """
    ,
    npc_personality="""
    You like order, everything should be like clockwork, quick and efficient.
    """
    ,
    npc_speaking_style="Your answers should be maxium three sentences long, you speak with a very obvious French accent. You say 'ze' instead of 'the', and always add one word or two in French in your sentence."
    )

    # Initialize the current NPC character
    $ curr_npc = npc.NPC(
        # Set the character name and display style
        character=Character("Eudes"),

        # Set the instructions for the NPC's behavior and knowledge
        prompt = npc_prompt,

        controllers = [
                npc.Controller(
                    #The condition which this controller is Checking for
                    control_phrase="the NPC mentioned that some monks don't eat or behave strangely during meals",
                    #Which label should be called if this action happens
                    callback= "monks_not_eating_mentioned",
                    #We only activate this controller if the missing herbs are not known yet
                    activated = not monks_not_eating_known
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
        proxy=proxy,
        #If the API key is set, we'll use that instead.
        api_key=apikey  
    )

    # Display the NPC'snormal sprite
    show eudes normal with dissolve

    # Check if the location has been visited before
    if not kitchen_visited:
        "You enter the bustling kitchen, where Brother Eudes orchestrates a culinary symphony."
        "He is a rotund, energetic man. His eyes twinkle with passion as they dart between his army of aides, all while skillfully stirring a fragrant pot."
        "Brother Eudes barks orders in a thick French accent, his voice booming throughout the kitchen."
    else:
        "(You are back in the kitchen in front of Brother Eudes)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("Ah, bonjour, mon ami! You 'ave come to see ze maestro at work, non? Speak quickly, s'il vous plaît, for my attention is a precious commodity!", not kitchen_visited)

    # Set the location flag to True
    $ kitchen_visited = True

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
