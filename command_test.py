from init_commands import *

"""
parse("/msg Isaac 'Hey there dumb head hows it going'")

parse("/help")

parse("/connect Andrew 191.002.022.02")

parse("/disconnect")

parse("/Junk")
"""

while(True):
    user_input = input(">")
    parse(None, user_input)