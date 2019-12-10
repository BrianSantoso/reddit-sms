# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from config import *

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_text(msg, from_=TWILIO_PHONE, to=RECEIVING_PHONE):
	try:
		message = client.messages.create(
			body=msg,
			from_=from_,
			to=to
		)
		return message.sid
	except TwilioRestException:
		raise Exception('Invalid Phone Number: To: ' + to + ' From: ' + from_)
	