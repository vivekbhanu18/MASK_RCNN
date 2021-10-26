from flask import Flask, render_template, request,url_for, redirect
from PIL import Image
from test1 import garbage_predict
from flask_mail import Mail, Message
import os
import pandas as pd
import pygal
from pygal.style import DarkStyle
app = Flask(__name__, static_folder='static')
app.debug= True

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bhanuvivek9705@gmail.com'
app.config['MAIL_PASSWORD'] = '9029861004'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 




@app.route("/")
def index(): 
    data=pd.read_csv('output.csv')
    data=data.dropna()
    new_data=data.groupby(['location'],sort=False).sum()
    location=list(set(list(data['location'])))
    graph = pygal.Bar(style=DarkStyle)    
    graph.title="usage of plastic (ACCORDING TO LOCATIONS)"
    graph.x_labels=location
    graph.add('plastic',list(new_data['plastic']))
    graph.add('Non-plastic',list(new_data['non_plastic']))
    graph_data=graph.render_data_uri()

    new_data1=data.groupby(['date_created'],sort=False).sum()
    date=list(set(list(data['date_created'])))
    graph1 = pygal.Bar(style=DarkStyle)    
    graph1.title="usage of plastic (ACCORDING TO DATES)"
    graph1.x_labels=date
    graph1.add('plastic',list(new_data1['plastic']))
    graph1.add('Non-plastic',list(new_data1['non_plastic']))
    graph_data1=graph1.render_data_uri()

    fr_chart = pygal.maps.fr.Departments(human_readable=True,style=DarkStyle)
    fr_chart.title = 'Population by department'
    fr_chart.add('In 2011', {
    '01': 603827, '02': 541302, '03': 342729, '04': 160959, '05': 138605, '06': 1081244, '07': 317277, '08': 283110, '09': 152286, '10': 303997, '11': 359967, '12': 275813, '13': 1975896, '14': 685262, '15': 147577, '16': 352705, '17': 625682, '18': 311694, '19': 242454, '2A': 145846, '2B': 168640, '21': 525931, '22': 594375, '23': 122560, '24': 415168, '25': 529103, '26': 487993, '27': 588111, '28': 430416, '29': 899870, '30': 718357, '31': 1260226, '32': 188893, '33': 1463662, '34': 1062036, '35': 996439, '36': 230175, '37': 593683, '38': 1215212, '39': 261294, '40': 387929, '41': 331280, '42': 749053, '43': 224907, '44': 1296364, '45': 659587, '46': 174754, '47': 330866, '48': 77156, '49': 790343, '50': 499531, '51': 566571, '52': 182375, '53': 307031, '54': 733124, '55': 193557, '56': 727083, '57': 1045146, '58': 218341, '59': 2579208, '60': 805642, '61': 290891, '62': 1462807, '63': 635469, '64': 656608, '65': 229228, '66': 452530, '67': 1099269, '68': 753056, '69': 1744236, '70': 239695, '71': 555999, '72': 565718, '73': 418949, '74': 746994, '75': 2249975, '76': 1251282, '77': 1338427, '78': 1413635, '79': 370939, '80': 571211, '81': 377675, '82': 244545, '83': 1012735, '84': 546630, '85': 641657, '86': 428447, '87': 376058, '88': 378830, '89': 342463, '90': 143348, '91': 1225191, '92': 1581628, '93': 1529928, '94': 1333702, '95': 1180365, '971': 404635, '972': 392291, '973': 237549, '974': 828581, '976': 212645
    })
    map_data=fr_chart.render_data_uri()
    return render_template("page.html",chart=graph_data,chart2=graph_data1,chart3=map_data)

@app.route("/")
def fileFrontPage():
    return render_template('page.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            src=photo.filename
            dst=os.path.join('C:/Users/vivek/.conda/envs/MaskRCNN/Mask_RCNN/Dataset/test', "test.jpg")
            photo.save(dst)
            #photo.save(os.path.join('C:/Users/vivek/.conda/envs/MaskRCNN/Mask_RCNN/Dataset/test', photo.filename))
    return redirect(url_for('fileFrontPage'))


@app.route("/", methods=["GET","POST"])
def disp_img():
    if request.method == "POST":
        '''loc_lat = request.form['locLat']
        loc_lng = request.form['locLng']
        print(loc)
        print(loc_lat, loc_lng)
        
        image = request.files["image"]
        # print(image)
        img = Image.open(image)
        img.save("C:\\Users\\vivek\\.conda\\envs\\MaskRCNN\\Mask_RCNN\\Dataset\\val")'''
        loc=request.form['location']
        garbage_predict(loc)
        msg = Message( 
                        'WASTE MANAGEMENT', 
                        sender ='bhanuvivek9705@gmail.com', 
                        recipients = ['jigarmange.jm@gmail.com'] 
                    ) 
        msg.body = 'Hello, We have found that there is high usage of plastic in your locality. Please take care of it.'
        mail.send(msg)

    return render_template("page.html")

if __name__ == "__main__":
    app.run()