from twilio.rest import Client
from .SmsConfig import SmsConfig


class SmsManager:

    def __init__(self, to_phone_number):
        self.to_phone_number = to_phone_number

    def process_incoming_message(self, respondent, incoming_message):
        response = respondent.recordAnswer(incoming_message)
        if response.is_message_valid:
            self.send_a_message(response.content)
        return response

    def send_a_message(self, message):
        account_sid = SmsConfig.get_account_sid()
        auth_token = SmsConfig.get_auth_token()
        from_phone_number = SmsConfig.get_from_phone_number()
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=message,
            from_=from_phone_number,
            to=self.to_phone_number
        )
        print(message.sid)
