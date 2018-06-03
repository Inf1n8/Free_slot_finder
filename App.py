from flask import Flask, request

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    print('hi')
    name = request.form['name']
    regno = request.form['regNo']
    print(name, regno,request)
    return 'Uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
