"""
Achievements
------------

A way to store a game achievement from the steam web api
"""

from PySteamWeb.apisteam.apicall import ApiCall
import json
from urllib import request

class Achiev:
    """
    Class to store a single achievement
    """
    def __init__(self, name, value, dis_name, hidden, desc, ico, ico_g):
        self.name = name
        self.default_value = value
        self.display_name = dis_name
        self.hidden = hidden
        self.description = desc
        self.icon_url = ico
        self.icon_gray_url = ico_g

class PlayerAchiev:
    """
    Class to store a single achievement
    """
    def __init__(self, name, achieved, unlocktime):
        self.name = name
        self.achieved = achieved
        self.unlocktime = unlocktime

class Achievements:
    """
    This class defines a standard for geting and consulting
        game achievements

    Parameters
    ----------
    app_id : the Steam app id
         (insert here link to consult)

    kargs :  

    Attributes
    ----------
    None

    Methods
    -------
    achievements_link : 

    """
    def __init__(self, app_id, **kargs):
        self.app_id = app_id
        self.game_name = self.get_game_info()[0]            # Index for game_name
        self.game_version = self.get_game_info()[1]         # Index for game_version
        self.game_achievements = self.get_achievements()    # List with game achievements

    #kargs
    pass

    def schema_link(self, **kargs):
        """
        Returns a link for the Game Schema

        Parameters
        ----------
        kargs: 
        """
        #kargs
        pass

        new_call = ApiCall()
        return new_call.generate_link(interface = 'ISteamUserStats', method='GetSchemaForGame', app_id = self.app_id, key = True)
    
    def get_game_info(self):
        """
        Returns all 3 game info on the WebApi schema link

        Parameters
        ----------
        None
        """
        temp_json = request.urlopen( self.schema_link() )            # Resquests the schema link
        temp_json = json.loads( temp_json.read().decode() ).get('game')     # Stores the json from the link on a dict

        game_name = temp_json.get('gameName')
        game_version = temp_json.get('gameVersion')
        game_achievements = temp_json.get('availableGameStats').get('achievements')

        return [game_name, game_version, game_achievements] 
    def get_achievements(self):
        """
        Funtions to get the achievements returning a list with the json search

        Parameters
        ----------
        None
        """
        temp_achiev_list = self.get_game_info()[2]
        new_achiev_list = []

        for achiev in temp_achiev_list:
            new_achiev_list.append( Achiev(
                                        achiev.get('name'),
                                        achiev.get('defaultvalue'),
                                        achiev.get('displayName'),
                                        achiev.get('hidden'),
                                        achiev.get('description'),
                                        achiev.get('icon'),
                                        achiev.get('icongray')
                ))

        return new_achiev_list

    def get_achievements_player (self):
        """
        Funtions to get the achievements returning a list with the json search
        (from player)
        """
        new_call = ApiCall(api_v = '1')
        new_call = new_call.generate_link(interface = 'ISteamUserStats', method='GetPlayerAchievements', app_id = self.app_id, key = True, steam_id = True)

        temp_json = request.urlopen( new_call )                          # Resquests the schema link
        temp_json = json.loads( temp_json.read().decode() ).get('playerstats')  # Stores the json from the link on a dict

        game_achievements = temp_json.get('achievements')

        new_achiev_list = []

        for achiev in game_achievements:
            new_achiev_list.append( PlayerAchiev(
                                        achiev.get('apiname'),
                                        achiev.get('achieved'),
                                        achiev.get('unlocktime'),
                ))

        return new_achiev_list
