label archives:
    #Prevents a bug where it reloads this scene and the user never said anything
    $ user_input = ""

    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # This should now play the full randomized playlist and then repeat from the begining.

    # Set the background scene to the location with a dissolve transition
    scene bg archives with dissolve

    # Let's create the Prompt of the NPC in this scene
    $ npc_prompt = gm_prompt_template.format(
    facts= act1_facts,
    gm_current_situation = "I am currently exploring the basement of the abbey of Neuberg, in the basement there's the archives of the Societa Templois, a knight order founded by Otto der Fröhliche and who fought against pagans in the far East."
    ,
    gm_knows_ok_to_say = """
    The Societa Templois doesn’t exist anymore, it disappeared shortly after the death of Otto.
    The archives are full of very weird books chained to the shelves as if they were beast ready to jump at them.
    Some of the books are really too thick some are really too thin or of weird proportions.
    Some have a perfectly black cover and some seems to be bound with human skin.
    There's a cage in the middle with a massive book with teeth. There are also armors, crests and weapons of the defeated pagans. They are of very weird and disturbing shapes.
    They are alone in the archives, there's nobody to talk to here."""
    ,
    gm_actions = """
    If I want to read a book, respond this exact meaning : I start reading and the more I read the more I want to read and I start reading like madman. The book is twisted, dark and illogical. Then describe that I becomes mad.
    If I want to open the massive cage or read the book with teeth or read the big book, respond this exact meaning : I can't because the cage is locked and nothing they do will unlock it and the book is inside it."""
    ,
    gm_speaking_style = "Your answers will be very descriptive and three sentences long in a very educated writing style. There is nothing magical in room or anywhere else, these books just seem horrible, but they aren't any magic."
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
                    control_phrase="I requested to leave the archives or I am not in the archives anymore.",
                    #Which label should be called if this action happens
                    callback= "leaving_archives",
                    #We only activate this controller if the missing heart is not known yet
                    activated = True
                     ),
                 npc.Controller(
                     #The condition which this controller is Checking for
                     control_phrase="I read the content of a book.",
                     #Which label should be called if this action happens
                     callback= "reads_a_book",
                     #We only activate this controller if the missing heart is not known yet
                     activated = True,
                     #This controller should stay active
                     permanent = True
                      )
            ],

        # Set the proxy server for the NPC to use
        proxy=proxy
    )

    # Check if the location has been visited before
    if not archives_visited:
        "(In this sequence you are not talking to any Character in particular, you have to describe what you do and the game will react accordingly)"
    else:
        "(You are back in the archives)"

    #Say the initial message if it's the first time we are here, but still record it in the conversation if it isn't.
    $ curr_npc.npc_says("""As you reach the bottom of the stairs, you find yourself standing before the entrance to the Societa Templois archives. Pushing open the creaking door, you're met with a dimly lit room filled with an intriguing collection of bizarre objects and countless books.
The shelves are lined with tomes of varying sizes and shapes, their odd configurations capturing your attention. Most of these books are chained securely to their resting places, as if they were wild beasts poised to leap at you.
Dominating the center of the room is a massive book with teeth, encased within an imposing cage. The atmosphere within the archive exudes an air of mystery and caution, inviting you to explore further while maintaining a respectful distance from its peculiar inhabitants."""
    ,
    #Display this message only the first time
    not archives_visited
    )

    # Set the location flag to True
    $ archives_visited = True

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
label leaving_archives:
    "(To leave the archives you should click on the Map Icon on the top right.)"
    jump archives

#Every time the user tries to read a book, something happens to him, different each time
define reading_attempts = 0

label reads_a_book:

    if reading_attempts == 0:
        # Display the NPC's normal sprite
        show torch monk normal at left with dissolve
        $ curr_npc.npc_says("And suddently a concerned monk enters the room, pulling you away from the book, and breaking the trance that held you captive.")
        $ curr_npc.npc_says("The Monk says : You've been reading here for hours, is everything ok ?")
        $ curr_npc.npc_says("You answer politely and he leaves the room.")
        "(Reading those books are clearly harmful)"
        hide torch monk normal with dissolve

    elif reading_attempts == 1:
        "You are unsure what time it is."
        "(You feel that you are not safe here and should leave at once.)"

    elif reading_attempts == 2:
        "You have the unnerving feeling that someone is watching you and coming closer."
        "(All your senses are screaming : Leave ! Now !)"

    else :
        call lose_sanity from _call_lose_sanity

    $ reading_attempts = reading_attempts + 1
    return
