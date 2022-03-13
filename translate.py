import deepl
import requests
from googletrans import Translator

def translate(text: str, deepl_api_key: str) -> str:
	"""
	Funkcia prelozi spravu do slovenciny.
	parametre:
	text - string, sprava na preklad,
	deepl_api_key - string, prihlasovaci kluc do prekladaca

	Google Translate ma relativne nizky limit na denny pocet prekladov a preto v pripade
	ze by tento limit dop presiahnuty, pouzije sa alternativny predklad od deepL

	Funkcia vracia string - preklad spravy
	"""

	try:
		# Google version
		
		translator = Translator()
		result = translator.translate(text, dest='sk', src='en').text

		if result == text:
			# # ak google translate neprelozi (prekroceny denny limit)
			# # sprav chybu a skoc do except
			print(non_exist_variable)

		return result

	except:

		translator = deepl.Translator(auth_key=deepl_api_key)
		result = str(translator.translate_text(text, target_lang="SK"))

		return result
		