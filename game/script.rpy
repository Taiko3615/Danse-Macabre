#The rollback creates some bugs, so I disable it
define config.rollback_enabled = False

##BASIC GAME STRUCTURE##
label start:

    #Let's start with the intro
    call intro from _call_intro

    #Now the tutorial
    #call tutorial

    #Now start act 1
    call act1 from _call_act1

    return
