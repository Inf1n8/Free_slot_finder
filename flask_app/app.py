from flask import Flask, jsonify, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from screenshotAnalyzer import convertImage2json
from slotToTime import convertSlotToTime
from queryFunctions import findFreeMembers
from queryFunctions import findFreeSlots

app = Flask(__name__)
cors = CORS(app)

# Connecting to the database
app.config['MONGO_DBNAME'] = 'freeslots'
app.config['MONGO_URI'] = 'mongodb://dscfreeslots:freeslots1!@ds147440.mlab.com:47440/freeslots'

mongo = PyMongo(app)
app.config['CORS_HEADERS'] = 'Content-Type'
photos = UploadSet('photos', IMAGES)

#specifying temporary location to save timetable photos
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
    club = request.form['clubCode']
    filename = photos.save(request.files['timetable'])
    print(name, club)
    nam, L = convertImage2json(filename)
    data = convertSlotToTime(L)
    print(data)
    temp_dict = {name: data, 'club':club}
    print(temp_dict)
    user = mongo.db.users
    user.insert(temp_dict)
    
    return 'Uploaded successfully'


@app.route('/findMembers', methods=['POST'])
@cross_origin()
def findMembers():
    print(request.json['day'], request.json['tabId'])
    day = request.json['day'][:3]
    tabId = request.json['tabId']
    user = mongo.db.users
    slots = {}
    for u in user.find():

        del (u['_id'])
        for name in u:
            if(name != "club"):
                slots[name] = u[name]

    data = findFreeMembers(tabId, day, slots)
    print(jsonify(data))
    return jsonify(data)

@app.route('/searchMember', methods=['POST'])
@cross_origin()
def searchMember():
    print(request.json['name'], request.json['day'][:3])
    name = request.json['name']
    day = str.lower(request.json['day'][:3])
    user = mongo.db.users
    members = []
    for u in user.find():

        del (u['_id'])
        for nam in u:
            if(name != "club"):
                members.append(nam)
    print(members)

    for u in user.find():
        del (u['_id'])
        for nam in u:
            
            if (nam == name):
                result = findFreeSlots(name, day, u[nam])
                print(result)
                return jsonify(result)

    return 'Member not found!'


if __name__ == '__main__':
    app.run()
