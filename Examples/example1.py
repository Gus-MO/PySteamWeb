"""
On this example we get the game achievements and the achievements
on this game of a player.

After that we're gonna print out the value on the format:
    (player_achievements) / (game_achievements)

Notice that we have the user credentials(api key and steam_id)
on a local file called 'credentials.json' so the script can be
on a directory with the format:

    Base_directory
    |__example1.py
    |__credentials.json
"""

import PySteamWeb

def achiev_printer(game_id):
    # Here we call a instance of Achievements
    my_call = PySteamWeb.achievs.Achievements(game_id)
    
    # This is the counter for the player achievements
    counter = 0
    for achievement in my_call.get_achievements_player():
        counter += achievement.achieved
    
    # Now is just printing the result
    print( counter, '/', len(my_call.get_achievements()))

# Uncomment the line below for calling the function directly
#achiev_printer('1145360')

"""
We can make the example more pratical especifing a __name__
condition, and taking a param from the Comand Line for the
game_id(Hades on this example) using 'sys' module:

    $ python3 example1.py 1145360
"""

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        achiev_printer(sys.argv[1])
    else:
        raise ValueError('Input Required')
