from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['POST'])
def upload():
    print('hi')
    name = request.form['name']
    regno = request.form['regNo']
    filename = photos.save(request.files['timetable'])
    print(name, regno)
    return 'Uploaded successfully'


@app.route('/findMembers', methods=['POST'])
def findMembers():
    print(request.json['day'], request.json['tabId'])
    day = request.json['day']
    tabId = request.json['tabId']
    return 'recieved info successfully'


if __name__ == '__main__':
    app.run(debug=True, port=5000)

