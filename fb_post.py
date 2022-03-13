import facebook

def send_post_with_picture(page_id: str, access_token: str, msg: str) -> None:
	"""
	Funkcia odosle na FB stravu aj s obrazkom

	param msg: str - Sprava
	param photo: str - path na fotku

	Funkcia nic nevracia
	"""

	photo='screenshot.png'

	graph = facebook.GraphAPI(access_token)

	if msg == None:
		msg = ' '

	# odosli spravu aj s obrazkom
	graph.put_photo(image=open(photo, 'rb'), message=msg)
