from flask import Flask, request

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    print('hi')
    name = request.form['name']
    regno = request.form['regNo']
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

