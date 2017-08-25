from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse

from MPDController import MPDController
 
app = Flask(__name__)
mpd_controller = MPDController()
 
@app.route('/', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    response_str = mpd_controller.handle_sms_request(request)

 
    resp = MessagingResponse()
    resp.message(response_str)
    return str(resp)
 
if __name__ == '__main__':
    app.run(debug=True)
