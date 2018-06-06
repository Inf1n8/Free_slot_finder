from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from screenshotAnalyzer import convertImage2json
from slotToTime import convertSlotToTime
from queryFunctions import findFreeMembers

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_DBNAME'] = 'freeslots'
app.config['MONGO_URI'] = 'mongodb://<dbname>:<dbpwd>@ds147440.mlab.com:47440/freeslots'

mongo = PyMongo(app)

app.config['CORS_HEADERS'] = 'Content-Type'

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/')
@cross_origin()
def main():
	return 'This is something cool will be up soon....'

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    print('hi')
    name = request.form['name']
    regno = request.form['regNo']
    filename = photos.save(request.files['timetable'])
    print(name, regno)
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
@cross_origin()
def findMembers():
    print(request.json['day'], request.json['tabId'])
    day = request.json['day']
    tabId = request.json['tabId']
    user = mongo.db.users
    slots = {}
    for u in user.find():
          del(u['_id'])
          for name in u:
               slots[name] = u[name]
    findFreeMembers(tabId, day, slots)
    return "request processed"

    return 'recieved info successfully'


@app.route('/searchMember', methods=['POST'])
@cross_origin()
def searchMember():
    print(request.json['name'], request.json['day'])
    name = request.json['name']
    day = request.json['day']
    return 'recieved data successfully'

if __name__ == '__main__':
    app.run()
