import requests, json, crop_image

def scr_apilayer(machine_hex: str , apikey: str, url_map: str) -> str:
	"""
	Funkcia sa aktualne nepouziva - nizky limit screenshotov

	funkcia prijma parametry:
	machine_hex = hexadecimalne cislo sledovaneho lietadla,
	screenshotlayer_key = api key ,
	url_map = url mapy

	funkcia vrati web odkaz na png subor so screenshotom
	a) screenshot stiahnut a orezat
	b) na orezanie vyuzit externu api sluzbu

	"""

	
	url = 'https://api.apilayer.com/screenshot?url=' + url_map.replace('&force=1', '') + machine_hex

	payload = {}
	headers= {
		"apikey": apikey,
	}

	params = {
		"height": "987",
		"width": "1440"
	}

	response = requests.request("GET", url, params=params , headers=headers, data = payload)
	return response

def scr_screenshotlayer(machine_hex: str, screenshotlayer_key: str, url_map: str) -> None:
	"""
	funkcia prijma parametry:
	machine_hex = hexadecimalne cislo sledovaneho lietadla,
	screenshotlayer_key = api key ,
	url_map = url mapy

	Vytvori screenshot a oreze ho na pozadovanu velkost
	"""
	url = 'http://api.screenshotlayer.com/api/capture?access_key=' \
	+ screenshotlayer_key \
	+ url_map \
	+ machine_hex \
	+ '&viewport=1440x987'

	name = 'screenshot.png'

	img_data = requests.get(url).content
	with open(name, 'wb') as handler:
		handler.write(img_data)

	crop_image.crop(name)

def get_screenshot(apikey: str, screenshotlayer_key: str, machine: str , url_map: str) -> None:

	"""
	Povodna myslienka bola na zaklade udalosti rozhodnut, ktore api sa na screenshot pouzije
	ale screenshotlayer ma mesacny free limit 100 a to by na tento projek mohlo stacit
	"""

	with open('./keys/machines.json', 'r') as f:
		machine_dic = json.load(f)

	machine_hex=machine_dic[machine]

	response = scr_screenshotlayer(machine_hex, screenshotlayer_key, url_map)
	#response = scr_apilayer(machine_hex, screenshotlayer_key, url_map)
