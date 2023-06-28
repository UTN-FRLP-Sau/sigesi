from PIL import Image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

razon=1/2
imagen = Image.open(BASE_DIR / 'banner.png')
tamano_destino = (int(imagen.size[0]*razon) ,int(imagen.size[1]*razon))

x='banner'
imagen = Image.open(BASE_DIR / '{}.png'.format(x))
imagen.save('src\static\landing\img\{}_origin.png'.format(x))
reduccion = imagen.resize(tamano_destino, Image.ANTIALIAS)
reduccion.save(BASE_DIR / '{}.png'.format(x))
