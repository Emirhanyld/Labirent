import pygame

# SFX file path
asset_sfx_jump_path = "sfx/jump.wav"
asset_sfx_footstep_path = "sfx/footstep.wav"

# SFX
sfx_jump = None
sfx_footstep = None

# SFX Channel
channel_jump = None
channel_footstep = None

def init():
    global sfx_jump
    global sfx_footstep
    global channel_jump
    global channel_footstep

    sfx_footstep = pygame.mixer.Sound(asset_sfx_footstep_path) 
    sfx_jump = pygame.mixer.Sound(asset_sfx_jump_path)

    channel_jump = pygame.mixer.Channel(0)
    channel_footstep = pygame.mixer.Channel(1)

def play_jump_sfx():
    global sfx_jump
    global channel_jump
    
    channel_jump.play(sfx_jump)

def play_footstep_sfx():
    global sfx_footstep
    global channel_footstep

    if not channel_footstep.get_busy():
        channel_footstep.play(sfx_footstep)

def stop_footstep_sfx():
    global sfx_footstep
    global channel_footstep

    if channel_footstep.get_busy():
        channel_footstep.stop()