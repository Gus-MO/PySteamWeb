'''
This module is made to acelerate the processes to get my steam data. v2
On Windows
'''
import urllib.request, json

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
