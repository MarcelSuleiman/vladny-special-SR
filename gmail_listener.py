import imaplib, email

imap_url = 'imap.gmail.com'

def get_body(raw):

	if raw.is_multipart():
	
		# prejdi cez jednotlive casti mailu
		for part in raw.walk():
			# vytiahni z mailu content type
			content_type = part.get_content_type()
			content_disposition = str(part.get("Content-Disposition"))
			try:
				# vytiahni telo mailu
				body = part.get_payload(decode=True).decode()
			except:
				pass
			if content_type == "text/plain" and "attachment" not in content_disposition:
				# vrat text/plain mailu a preskoc prilohy
				return body
		#return get_body(raw.get_payload(0))
	else:
		return raw.get_payload(None,True)


def scarpe(user, password):

	con = imaplib.IMAP4_SSL(imap_url)
	con.login(user, password)
	con.select('INBOX')

	resp, items = con.search(None, '(UNSEEN)') # UNSEEN MAIL

	if items != [b'']:

		a = items
		b = a[0].decode('utf-8')
		b = b.split(' ')

		mails = {}

		for value in b:
			mail_data = []

			result, data = con.fetch(value, '(RFC822)')

			raw = email.message_from_bytes(data[0][1])
			text = str(get_body(raw))

			mail_key = str(value) + str(raw['From'])

			mail_data.append(raw['Date'])
			mail_data.append(raw['From'])
			mail_data.append(raw['Subject'])
			mail_data.append(text)

			mails[mail_key] = mail_data

		return mails

	else:
		return {}
