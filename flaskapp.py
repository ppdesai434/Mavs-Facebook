from flask import Flask,render_template, request, jsonify
from flaskext.mysql import MySQL
import base64
import datetime
import os
import csv
app = Flask(__name__)

mysql = MySQL()
#mysql credentials
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''


mysql.init_app(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')

@app.route('/')
def hello():
        #with open(os.path.join(APP_STATIC, 'UsersAccess.txt')) as f:
            #reader = csv.reader(f ,delimiter=',', quotechar="'")
            #print "Hello" #reader
        return render_template('index.html')


@app.route('/choice', methods=['POST','GET'])
def validate():
    vname = request.args.get('name1')
    options = request.args.get('options')
    print vname
    print options
    conn = mysql.connect()
    cursor = conn.cursor()
    if options == 'value1':
        return render_template('create.html', dd=vname)
    else:
        identities = cursor.execute("select id, name,caption,image_data,createdtime,rating_count,vcount from myalbumnewest")
        # creatorname = cursor.execute("select name from myalbumnewest")
        # captionget = cursor.execute("select caption from myalbumnewest")
        # imagedata = cursor.execute("select image_data from myalbumnewest")
        data = cursor.fetchall()
        for row in data:
            print row[0]
        return render_template('view.html', dd=vname,data=data)
    return 'Connection Done'


@app.route('/rating',methods=['POST','GET'])
def rating():
    givenrating = request.args.get('rating')
    givenid = request.args.get('id')
    print givenrating
    print givenid
    conn = mysql.connect()
    cursor = conn.cursor()
    countinc = cursor.execute("select vcount from myalbumnewest where id="+givenid+";")
    countdata = cursor.fetchone()
    print countdata[0]
    ratingcountquery = cursor.execute("select rating_count from myalbumnewest where id="+givenid+";")
    ratingdata = cursor.fetchone()
    setcount = countdata[0] + 1
    setrating = ratingdata[0] + int(givenrating)
    updatequery = cursor.execute("update myalbumnewest set vcount = "+str(setcount)+", rating_count="+str(setrating)+" where id="+givenid+";")
    conn.commit()
    calculatedrating = round( setrating / setcount )
    return jsonify(rating = calculatedrating, count = setcount)




@app.route('/upload',methods=['POST','GET'])
def upload():
        print request
        caption1 = request.form.get('caption')
        person_name = request.form.get('person_name')
        file = request.files['file']
        print caption1
        print person_name
        file_content = file.read()
        size = len(file_content)/1024
        if size > 1024:
                return "File Size Larger than 1 Mb"
        print size
        sixtyfour = base64.b64encode(file_content)
        print sixtyfour

        conn = mysql.connect()
        cursor = conn.cursor()
        query = "insert into myalbumnewest(name,caption,image_data,rating_count,vcount,createdtime) values('"+person_name+"','"+caption1+"','"+sixtyfour+"',"+str(1)+","+str(1)+",'"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"')"
        print query
        cursor.execute(query)
        conn.commit()
        return ''' <img src="data:image/png;base64, {0}">'''.format(sixtyfour)

# @app.route("/")
# def hello():
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("select name from asshole")
#         conn.commit()
#         data = cursor.fetchone()
#         if data:
#                 return data
#         return "Dint work"


if __name__ == '__main__':
    app.run(debug=True)
