from flask import Flask
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
mail = Mail(app)

@app.route("/")
def index():

    msg = Message("Hello",
                  sender="test@admin.com",
                  recipients=["mmaarouf95@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
