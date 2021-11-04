from functions import make_image
from PIL import Image
import time, os

def resize_image():
    img = Image.open('/mnt/c/Users/Adalton/Desktop/Gustavo0/games/Stream/Images/achievments_temp.jpg')
    width, height = img.size
    with open('/mnt/c/Users/Adalton/Desktop/Gustavo0/games/Stream/Images/total.txt', 'r') as total_file1: 
        texto = total_file1.readline()
        texto = texto[:texto.find('/')]
        total = int(texto)
    center = 64*total
    final = center+(1280/2)
    if final <= width:
        left = center-(1280/2)
        right = center+(1280/2)
    else:
        right = width
        left = width - 1280
    new_img = img.crop((left,0,right,height))
    new_img.save('/mnt/c/Users/Adalton/Desktop/Gustavo0/games/Stream/Images/achievments.jpg')

while True:
    os.system('clear')
    print('Making temporary file!')
    make_image('SuperMeatBoy', 40800)
    time.sleep(1)
    print('Resizing the image to the final file!! :D')
    resize_image()
    time.sleep(1)
    print('Finally erasing the temporary file... Now lets wait...')
    os.system('rm /mnt/c/Users/Adalton/Desktop/Gustavo0/games/Stream/Images/achievments_temp.jpg')
    time.sleep(58)
    print('And here we go again ...')
    time.sleep(2)
    break
