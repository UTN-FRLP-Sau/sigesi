from PIL import Image
razon=1.2
imagen = Image.open('src\static\landing\img\logo_ingreso_origin.png')
tamano_destino = (int(imagen.size[0]*razon) ,int(imagen.size[1]*razon))

x='logo_ingreso'
imagen = Image.open('src\static\landing\img\{}_origin.png'.format(x))
#imagen.save('src\static\landing\img\{}_origin.png'.format(x))
reduccion = imagen.resize(tamano_destino, Image.ANTIALIAS)
reduccion.save('src\static\landing\img\{}.png'.format(x))
