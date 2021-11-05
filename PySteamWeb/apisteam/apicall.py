"""
ApiCall
-------

A way to get and store your calls to the Steam Web API.
This is the base module for the rest. It provides a
generic way for calling Methods.
"""

import json

class ApiCall:
    """
    This Class defines a interface for calling Steam API https
    
    The default format for a SteamWebApi Call is:

        https://api.steampowered.com/<interface>/<method>/v<version>/

    As especified on the Documentation:

        https://partner.steamgames.com/doc/webapi_overview

    Parameters
    ----------
    api_v : string
        The steam WebApi version for the calls
    creds : string
        Your api credentials path, defauts to './credentials.json'

    Attributes
    ----------
    None

    Methods
    -------
    import_credentials : Imports a credential in a especified folder

    generate_link : Returns a string with the api call link

    Example
    -------

    """

    def __init__(self, api_v = '2', creds = './credentials.json'):    # some functions are only avaliable on v1
        self.api_v = api_v
        self.creds = creds

    def import_credentials(self):
        """ Imports a credential in a especified folder """
        with open(self.creds, 'r') as arquivo:
            return json.load(arquivo)

    def generate_link(self, interface = '', method = '', **kargs):
        """
        Returns a string with the api call link
        
        Parameters
        ----------
        interface : The API interface as especified on the documentation
            https://partner.steamgames.com/doc/webapi_overview

        method : The API method as especified on the documentation
            https://partner.steamgames.com/doc/webapi_overview

        **kargs
        ---------
            api_v : The method version, defaults to 2
            key : Especifies if the key on credentials file is necessarie
            steam_id : Especifies if the steam_id on credentials file is necessarie
            game_id : The game id param
            user_id : The use id param
            
        """
        if None != kargs.get('api_v'):
            self.api_v = kargs.get('api_v')
        else: self.api_v = '2'
        key = kargs.get('key')
        steam_id = kargs.get('steam_id')
        game_id = kargs.get('game_id')
        app_id = kargs.get('app_id')
        user_id = kargs.get('user_id')

        # Getting the params list
        params = ''
        if key:         # The key is store on a file, so we only especify if we need it
            params += 'key=' + self.import_credentials().get('key') + '&'
        if steam_id:    # The steam_id is store on a file, so we only especify if we need it
            params += 'steamid=' + self.import_credentials().get('steamID') + '&'
        if game_id != None:
            params += 'gameid=' + game_id + '&'
        if app_id != None:
            params += 'appid=' + app_id + '&'
        if user_id != None:
            params += 'userid=' + user_id + '&'

        return 'https://api.steampowered.com/' + interface + '/' + method + '/v' + self.api_v + '/?' + params
