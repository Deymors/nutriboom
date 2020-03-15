import os
from datetime import datetime

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
import logging
from twilio.twiml.messaging_response import MessagingResponse
from flask import request

from respondent.Respondent import Respondent
from sms.SmsManager import SmsManager

app = Flask(__name__,
            static_url_path='',
            static_folder='build')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(700), nullable=False)
    direction = db.Column(db.Boolean)

    def __repr__(self):
        return "(%d, %d, %s, %d)" % (self.id, self.user_id, self.content, self.direction)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    contactable = db.Column(db.Boolean)
    stage = db.Column(db.Integer)
    number_surveyed = db.Column(db.Integer)
    number_sufficient = db.Column(db.Integer)
    number_deficient = db.Column(db.Integer)

    def __repr__(self):
        return "(%d,%s,%d,%d,%d,%d,%d)" % (
            self.id, self.phone, self.contactable, self.stage, self.number_surveyed, self.number_sufficient,
            self.number_deficient)


class Recordings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_surveyed = db.Column(db.Integer)
    number_sufficient = db.Column(db.Integer)
    number_deficient = db.Column(db.Integer)
    data = db.Column(db.Date)

    def __repr__(self):
        return "(%d,%d,%d)" % (self.number_surveyed, self.number_sufficient, self.number_deficient)


@app.route('/')
def webprint():
    return app.send_static_file('index.html')


def get_respondent(phone_number):
    try:
        user_data = User.query.filter_by(phone=phone_number).first()
        if user_data is None:
            new_user = User(phone=phone_number, contactable=True, stage=0)
            db.session.add(new_user)
            db.session.commit()
            respondent = Respondent()
            return respondent
        respondent = Respondent(current_question=user_data.stage, number_surveyed=user_data.number_surveyed,
                                number_sufficient=user_data.number_sufficient,
                                number_deficient=user_data.number_deficient)
        return respondent
    except:
        print("Error with getting respondent data:", sys.exc_info()[0])
        print("Error with getting respondent data:", sys.exc_info()[1])
        print("Error with getting respondent data:", sys.exc_info()[2])


@app.route("/sms-receive", methods=['GET', 'POST'])
def sms_reply():
    incoming_msg = "123123123123"
    incoming_phone_number = "123123123123"
    respondent = None

    response = None
    try:
        incoming_msg = request.values.get('Body', '')
        incoming_phone_number = request.values.get('From', '').lower()
        respondent = get_respondent(incoming_phone_number)
        response = respondent.recordAnswer(incoming_msg)
    except:
        print("Error with response retrieval:", sys.exc_info()[0])
        print("Error with response retrieval:", sys.exc_info()[1])
        print("Error with response retrieval:", sys.exc_info()[2])
        print("Error with response retrieval:", sys.exc_info()[3])
        print("Error with response retrieval:", incoming_phone_number + " " + incoming_msg)
    reply = MessagingResponse()
    print("Message response:",
          response.content + " " + incoming_phone_number + " " + incoming_msg + " " + str(response.stage))
    reply.message(response.content)
    # record data if end of the process
    if response.stage == Respondent.get_num_stages()-1:
        recording = Recordings(number_surveyed=respondent.surveyed, number_sufficient=respondent.sufficient,
                               number_deficient=respondent.deficient, data=datetime.now())
        try:
            db.session.add(recording)
            response.stage = 0
            db.session.commit()
        except:
            print("Error with recording response data:", sys.exc_info()[0])
    # update user data
    try:
        user_data = User.query.filter_by(phone=incoming_phone_number).first()
        user_data.contactable = response.contactable
        user_data.stage = response.stage
        user_data.number_surveyed = respondent.surveyed
        user_data.number_sufficient = respondent.sufficient
        user_data.number_deficient = respondent.deficient
        db.session.commit()
    except:
        print("Error updating user data:", sys.exc_info()[0])
    return str(reply)


@app.route("/sms-send", methods=['GET', 'POST'])
def sms_send():
    smsManager = SmsManager("+15148352375")
    smsManager.send_a_message("boom boom")


@app.route("/get-records", methods=['GET'])
def get_records():
    return jsonify({'recordings': list(map(lambda recording: recording._repr__(), Recordings.query.all()))})


if __name__ == "__main__":
    app.run(debug=True)
