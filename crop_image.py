
from PIL import Image

def crop(name):

	img = Image.open(name)

	left = 0
	top = 87
	right = 800
	bottom = 887

	img_res = img.crop((left, top, right, bottom))
	# prepise sam seba
	img_res.save(name)
