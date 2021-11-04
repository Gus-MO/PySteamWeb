'''
This module is made to acelerate the processes to get my steam data. v2
On Windows
'''

import urllib.request, json

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
            api_v : The method version, defauts to 2
            key : Especifies if the creds are necessarie
            game_id : The game id param
            user_id : The use id param
            
        """
        if None != kargs.get('api_v'):
            self.api_v = kargs.get('api_v')
        key = kargs.get('key')
        game_id = kargs.get('game_id')
        app_id = kargs.get('app_id')
        user_id = kargs.get('user_id')

        # Getting the params list
        params = ''
        if key:
            params += 'key=' + self.import_credentials().get('key') + '&'
        if game_id != None:
            params += 'gameid=' + game_id + '&'
        if app_id != None:
            params += 'appid=' + app_id + '&'
        if user_id != None:
            params += 'userid=' + user_id + '&'

        return 'https://api.steampowered.com/' + interface + '/' + method + '/v' + self.api_v + '/?' + params

class Achievements:
    def __init__(self, api_v = '1'):
        self.api_v = api_v   #api version
    
    def import_credentials(self):
        '''
        Imports a credential in a especified folder
        '''
        with open('credentials.txt', 'r') as arquivo:
            return json.load(arquivo)

    def achievements_link(self, game_id, **kargs):
        '''
        Returns a link for the search
        on the v1 Steamworks Web Api
        --------------------------------
        key: api key
        steamId: user steam id
        kargs:  l = language
                of = output format
        '''
        #kargs
        language = kargs.get('l')
        format_out = kargs.get('of')

        #import credentials and defines the link to put on the SteamAPI requirement
        credentials = self.import_credentials()
        link = 'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v000{}/'.format(self.api_v)
    
        #define the values os the language and the format_out
        if language: language = '&l={}'.format(language)
        else: language = ''
        if format_out: format_out = '&format={}'.format(language)
        else: format_out = ''

        #defines the args to put on the SteamAPI requirement
        args = '?appid={0:s}&key={1:s}&steamid={2:s}'.format(str(game_id), credentials.get('key'), credentials.get('steamID'))
        args += language + format_out
    
        return link + args

    def get_achievements (self, game_id):
        '''
        Funtions to get the achievements
        returning a list with the json search
        (from player)
        '''
        link = self.achievements_link(game_id)

        #saves the content on a file

        with urllib.request.urlopen(link) as url:
            return json.loads(url.read().decode()).get('playerstats').get('achievements')

    def get_gameSchema (self, game_id):
        '''
        Funtions to get the game schema
        returning a dict with the json search
        '''
        link = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?appid={}'.format(str(game_id))
        key = self.import_credentials().get('key')

        link += '&key={}'.format(key)

        with urllib.request.urlopen(link) as url:
            return json.loads(url.read().decode()).get('game').get('availableGameStats').get('achievements')
