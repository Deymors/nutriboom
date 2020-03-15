from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse
from flask import request

from SmsManager import SmsManager

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/sms-receive", methods=['GET', 'POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    resp.message(SmsManager.get_response(incoming_msg))
    return str(resp)


@app.route("/sms-send", methods=['GET', 'POST'])
def sms_reply():
    smsManager = SmsManager("+15148352375")


if __name__ == "__main__":
    app.run(debug=True)
