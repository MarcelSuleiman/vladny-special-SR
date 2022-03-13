import json
import gmail_listener
import screenshot
import os

from time import sleep
from fb_post import send_post_with_picture
from translate import translate


# nacitanie suboru s prihlasovacimi udajmi a roznymi API klucmi 
with open('./keys/keys.json', 'r') as f:
	keys = json.load(f)

# gmail prihlasovacie udaje
login = keys['gmail']['login']
password = keys['gmail']['pwd']

while True:

	# obcas sa stane ze prihlasenie je neuspesne
	# tak nech sa to nezrube
	try:
		data = gmail_listener.scarpe(login, password)
	except Exception as E:
		print('Nepodarilo sa prihlasit, skusim znova...')
		print(E.__class__.__name__, str(E))
		sleep(5)
		continue

	# precitam jeden mail za druhym
	for key, value in data.items():

		machine = ''

		subject = data[key][2]

		text = data[key][3].split('\n\n')
		text = text[0].split('\r\n\r\n')
		text = text[0]

		# Ak nepriletel, neodletel, nebol videny ,... ignoruj spravu
		# vyplneny letovy plan, zmena kurzu, predpokladany cas priletu a pod
		if 'departed' in subject or 'arrived' in subject or 'spotted' in subject:

			# ak odlieta, pockaj 5min - lepsie to na screenshote vyzera :)
			if 'departed' in subject:
				sleep(60*5)

			temp = subject.split(' ')

			if '/' in temp[0]:
				machine = subject.split(' ')[0].split('/')[1]
			else:
				machine = subject.split(' ')[0]

			if machine != '':
				apikey = keys['apilayer_key']
				screenshotlayer_key = keys['screenshotlayer_key']
				url_map = keys['map']
				screenshot.get_screenshot(apikey, screenshotlayer_key, machine, url_map)
				
				# preklad do SJ
				deepl_api_key = keys['deepl_api_key']
				text = translate(text, deepl_api_key)

				# odoslanie na fb
				page_id = keys['fb_page_id']
				access_token = keys['fb_access_token']
				send_post_with_picture(page_id, access_token, text)

				print(text)

				# odstranenie
				os.remove('screenshot.png')

		else:
			pass

	sleep(5)