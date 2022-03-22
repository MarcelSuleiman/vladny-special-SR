import requests, json, crop_image

def get_universal_screenshot(machine_hex: str) -> None:
	with open('./keys/keys.json', 'r') as f:
		keys = json.load(f)

	screenshotlayer_key = keys['screenshotlayer_key']
	screenshotbird_key = keys['screenshotbird_key']
	apiflash_key = keys['apiflash_key']
	screenshotmachine_key = keys['screenshotmachine_key']

	url_map = keys['map']

	while True:
		"""
		Nekonecny cyklus prejde iba raz, je to iba akasi zaruka
		ze sa vyskusaju vsetky verejne api na screenshot
		
		ak ma jeden v poradi volne requesty, ukonci sa skor
		"""

		url = 'http://api.screenshotlayer.com/api/capture?access_key=' + screenshotlayer_key \
			+ '&force=1&viewport=1440x987&url=' \
			+ url_map + machine_hex
		
		img_data = requests.request("GET", url)
		print(img_data.status_code)
		print(img_data)
		
		status = json.loads(img_data.text)

		if img_data.status_code == 200 and status['success'] != False:
			url_image = 'direct'
			break

		url = 'https://api.screenshotbird.com/screenshot?token=' + screenshotbird_key \
			+ '&browser_width=1440&browser_height=997&block_ads=true&fresh=true&url=' \
			+ url_map + machine_hex
		
		img_data = requests.request("GET", url)
		print(img_data.status_code)
		print(img_data)
		if img_data.status_code == 200:
			url_image = 'url'
			break

		url = 'https://api.apiflash.com/v1/urltoimage?access_key=' + apiflash_key \
			+ '&width=1440&height=997&no_ads=true&no_tracking=true&fresh=true&response_type=json&url=' \
			+ url_map + machine_hex
		
		img_data = requests.request("GET", url)
		print(img_data.status_code)
		print(img_data)
		if img_data.status_code == 200:
			url_image = 'url'
			break

		url = 'https://api.screenshotmachine.com/?key=' + screenshotmachine_key \
			+ '&device=desktop&format=png&dimension=1440x997&url=' \
			+ url_map + machine_hex
		
		img_data = requests.request("GET", url)
		print(img_data.status_code)
		print(img_data)
		if img_data.status_code == 200:
			url_image = 'direct'
			break

		break

	if url_image != 'direct':
		"""
		ak api odpoveda stringom - odkazom na obrazok, vyextrahujeme link
		ak vysledkom api je obrazok, extrakciu preskocime
		"""
		data = json.loads(img_data.text)
		print(data)
		
		url = data[url_image]
		print(url)

	name = 'screenshot.png'

	img_data = requests.get(url).content
	with open(name, 'wb') as handler:
		handler.write(img_data)

	crop_image.crop(name)

def get_screenshot(machine: str) -> None:

	"""
	DOC
	"""
	with open('./keys/machines.json', 'r') as f:
		machine_dic = json.load(f)

	machine_hex = machine_dic[machine]

	get_universal_screenshot(machine_hex)
