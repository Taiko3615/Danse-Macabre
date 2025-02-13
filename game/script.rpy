#The rollback creates some bugs, so I disable it
define config.rollback_enabled = False

define playlist = [ "audio/music/Music 1.mp3", "audio/music/Music 2.mp3", "audio/music/Music 3.mp3", "audio/music/Music 4.mp3", "audio/music/Music 5.mp3", "audio/music/Music 6.mp3", "audio/music/Music 7.mp3", "audio/music/Music 8.mp3"]

init python:
    import npc
    import chatgpt
    import re

##BASIC GAME STRUCTURE##
label start:
    #Change the music
    stop music fadeout 1.0
    $ renpy.random.shuffle(playlist)         # Should shuffle in place
    play music playlist fadeout 1.0 fadein 1.0 # Thi

    #Unfortunately some users horribly abused my API Key, so now you need to provide your own.
    call get_api_key

    #Let's start with the intro
    call intro from _call_intro

    #Now start act 1
    call act1 from _call_act1

    return


label get_api_key:
    define s = Character(None, kind=nvl, what_prefix="Game Author: \"", what_suffix="\"")

    s "Welcome to Danse Macabre RPG, the world's first game entire powered by AI.\nIt's commonplace now, but back then we were the first."
    s "Initially this game would use my own Open AI API key to generate all the dialogues.\nUnfortunately some players abused it in horrible ways, which got me banned from OpenAI."
    s "No surprises there, Welcome to the internet !"
    s "So I have no choice now but to ask you to use your own OpenAI api key.\nGoogle 'how to create an Open AI API key' to learn how to do it, then input you key here :"
    python:
        apikey = renpy.input("What is your OpenAI API key?")
        apikey = apikey.strip()
    s "Thanks ! Without further ado, let's start !"
    return


#During the game, you can lose sanity. It's a permanent effect that adds up
define sanity_loss = 0

label lose_sanity:
    "You are loosing grip with reality."
    $ sanity_loss = sanity_loss + 1
    show screen sanity_icon
    return

screen sanity_icon:
    zorder 10
    imagebutton:
        xcenter 110
        ycenter 110
        idle "icon sanity.png"
        hover "icon sanity hovered.png"
        activate_sound "audio/click.mp3"
        at transform:
            zoom 0.1875
        action Call("open_sanity_icon")

label open_sanity_icon:
    nvl clear
    define j = Character(kind=nvl)
    j "Congratulations! You are Insane{nw}"
    python:
        messages = [
            {"role": "system", "content": "Write me a poetry about life and death in Ogham. The poetry should be at least "+str(sanity_loss)+"00 characters long and using Ogham characters. Don't include a translation."},
        ]
        try:
            # Make a ChatGPT API call to get the response
            response = chatgpt.completion(messages, proxy=proxy, api_key=apikey)[-1]["content"]
        except:
            # Display an error message if the API call fails
            response = """᚛ᚉᚑᚊᚔᚉᚔᚋᚐᚉᚓ᚜ ᚄᚏᚑᚔᚅᚓ᚜
᚛ᚔᚅᚓ᚜ ᚋᚔᚊᚔᚓ᚜ ᚋᚐᚊᚐᚔ᚜
᚛ᚔᚅᚓ᚜ ᚉᚐᚅᚑᚔ᚜ ᚄᚔᚋᚐᚉ᚜
᚛ᚔᚅᚓ᚜ ᚉᚐᚅᚑᚔ᚜ ᚋᚔᚊᚔᚓ᚜
᚛ᚄᚉᚓ᚜ ᚋᚐᚊᚐᚔ᚜ ᚔᚓᚅᚓ᚜ᚔᚅᚔ᚜ᚔᚅᚓ᚜
᚛ᚔᚅᚓ᚜ ᚉᚐᚅᚑᚔ᚜ ᚐᚅᚔᚉᚔ᚜
᚛ᚉᚓᚅᚐ᚜ ᚐᚅᚔᚉᚔ᚜ ᚋᚓᚏᚑᚔ᚜
᚛ᚉᚑᚊᚔᚉᚔᚋᚐᚉᚓ᚜ ᚄᚏᚑᚔᚅᚓ᚜᚜"""

        # Let's remove anything that would be remotely legible.
        response = re.sub("[a-zA-Z(),.?!:;\'\"\[\]]+", "", response)

        # If the response is longer than 150 characters, split it into multiple messages
        if len(response) > 150:
            response_list = [response[i:i+150] for i in range(0, len(response), 150)]
        else:
            response_list = [response]

        # Print each message in the response list
        for r in response_list:
            j("{font=DejaVuSans.ttf}"+r+"{/font}{nw}")

        j("-----")
    return
