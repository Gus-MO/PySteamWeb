'''
This module is made to acelerate the processes to get my steam data.
'''
import urllib.request, json, os
from PIL import Image

def import_credentials ():
    '''
    Imports a credential in a especified folder,
    '''
    with open('credentials.txt', 'r') as arquivo:
        return json.load(arquivo)

#later try implement a generic funtion to call any API interface function

def achievements_link (game_id,**kargs):
    '''
    Returns a link for the serch
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
    credentials = import_credentials()
    link = 'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/'
    
    #define the values os the language and the format_out
    if language: language = '&l={}'.format(language)
    else: language = ''
    if format_out: format_out = '&format={}'.format(language)
    else: format_out = ''

    #defines the args to put on the SteamAPI requirement
    args = '?appid={0:s}&key={1:s}&steamid={2:s}'.format(str(game_id), credentials.get('key'), credentials.get('steamID'))
    args += language + format_out
    
    return link + args

def get_achievements (game_id):
    '''
    Funtions to get the achievements
    returning a list with the json search
    (from player)
    '''
    link = achievements_link(game_id)

    #saves the content on a file
    #os.system('curl -X GET "{0}" > achievements.json'.format(link))

    with urllib.request.urlopen(link) as url:
        return json.loads(url.read().decode()).get('playerstats').get('achievements')
    
def get_gameSchema (game_id):
    '''
    Funtions to get the game schema
    returning a dict with the json search
    '''
    link = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?appid={}'.format(str(game_id))
    key = import_credentials().get('key')

    link += '&key={}'.format(key)

    #saves the content on a file
    #os.system('curl -X GET "{0}" > achievements1.json'.format(link))

    with urllib.request.urlopen(link) as url:
        return json.loads(url.read().decode()).get('game').get('availableGameStats').get('achievements')

    

def make_image(game_name,game_id):
    '''
    Creates a file with the achievements image
    '''

    images = []
    iter = 0
    for x in images_chooser(game_name,game_id):
        x = Image.open(x[1])
        images.append(x)
        #iter+=1
        #if iter > 20: break

    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('/mnt/c/Users/Adalton/Desktop/Gustavo0/games/Stream/Images/achievments_temp.jpg')

#def get_images(game_id):
#   for i in get_gameSchema(40800):
#   ...:     os.system('curl -X GET {1} > ./Images/Teste/Complete/{0}.jpg'.format(i.get('name'),i.get('icon')))
#
#   for i in get_gameSchema(40800):
#   ...:     os.system('curl -X GET {1} > ./Images/Teste/Missing/{0}.jpg'.format(i.get('name'),i.get('icongray')))

def images_chooser (game_name, game_id):
    my_achieves = get_achievements(game_id)
    all_achieves = get_gameSchema(game_id)
    complete_image = './Images/{}/Complete/'.format(game_name)
    missing_image = './Images/{}/Missing/'.format(game_name)

    images_complet = []
    images_missing = []
    total_achieved = 0
    total_missing = 0
    for i in my_achieves:
        achiev = Achievement(i)
        if achiev.status() == 1:
            images_complet.append((achiev.name(), '{0}{1}.jpg'.format(complete_image, achiev.name())))
            total_achieved +=1
        elif achiev.status() == 0:
            images_missing.append((achiev.name(), '{0}{1}.jpg'.format(missing_image, achiev.name())))
            total_missing +=1
    images = images_complet + images_missing
    with open('/mnt/c/Users/Adalton/Desktop/Gustavo0/games/Stream/Images/total.txt', 'w') as total_file: total_file.write('{0}/{1}'.format(str(total_achieved),total_achieved+total_missing))
    return images


class Achievement:
    def __init__(self, achievement_dict):
        self.achievement_dict = achievement_dict

    def name(self):
        return self.achievement_dict.get('apiname')
    
    def status(self):
        return self.achievement_dict.get('achieved')