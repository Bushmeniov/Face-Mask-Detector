import os
from PIL import  Image
import hashlib

dict = "/home/vladislav/Рабочий стол/djdf/"
files = os.listdir(dict)

to_dawload="/home/vladislav/Рабочий стол/djdf/"
for file in files :

	image = Image.open(dict+file)
	image = image.resize((300, 300))
	path = os.path.join(to_dawload, file)

	with open(path, "wb") as f:
		image.save(f, "JPEG", quality=85)

