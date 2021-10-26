# importing libraries 
from flask import Flask 
from flask_mail import Mail, Message
from flask import Flask, render_template, request,url_for, redirect


app = Flask(__name__) 
mail = Mail(app) # instantiate the mail class 

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bhanuvivek9705@gmail.com'
app.config['MAIL_PASSWORD'] = '9029861004'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

@app.route("/")
def display():
    return render_template("example.html")


# message object mapped to a particular URL ‘/’ 
@app.route("/", methods=["GET","POST"])
def email_sent():
    if request.method == "POST":
        msg = Message( 
                        'WASTE MANAGEMENT', 
                        sender ='bhanuvivek9705@gmail.com', 
                        recipients = ['jigarmange.jm@gmail.com'] 
                    ) 
        msg.body = 'Hello, We have found that there is high usage of plastic in your locality. Please take care of it.'
        mail.send(msg) 
        return render_template("example.html")

if __name__ == '__main__': 
    app.run(debug = True) 
