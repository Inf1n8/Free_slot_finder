from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_pymongo import PyMongo
from screenshotAnalyzer import convertImage2json
from slotToTime import convertSlotToTime
from queryFunctions import findFreeMembers

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'freeslots'
app.config['MONGO_URI'] = 'mongodb://<dbname>:<dbpwd>@ds147440.mlab.com:47440/freeslots'

mongo = PyMongo(app)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/')
def main():
	return 'This is something cool will be up soon....'

@app.route('/upload', methods=['POST'])
def upload():
    print('hi')
    name = request.form['name']
    regno = request.form['regNo']
    filename = photos.save(request.files['timetable'])
    nam, L = convertImage2json(filename)
    data = convertSlotToTime(L)
    print(data)
    temp_dict = {name : data}
    print(temp_dict)
    user = mongo.db.users
    user.insert(temp_dict)
    print(name, regno)
    return 'Uploaded successfully'


@app.route('/findMembers', methods=['POST'])
def findMembers():
    
    day = request.json['day'][:3]
    tabId = request.json['tabId']
    print(day,tabId)
    user = mongo.db.users
    slots = {}
    for u in user.find():
          del(u['_id'])
          for name in u:
               slots[name] = u[name]
    findFreeMembers(tabId, day, slots)
    return "request processed"



if __name__ == '__main__':
    app.run(debug=True, port=5000)

