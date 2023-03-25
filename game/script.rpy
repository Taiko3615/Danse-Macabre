#The rollback creates some bugs, so I disable it
define config.rollback_enabled = False

##BASIC GAME STRUCTURE##
label start:

    #Let's start with the intro
    call intro

    #Now the tutorial
    #call tutorial

    #Now start act 1
    call act1

    return
