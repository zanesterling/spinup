from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def home():
	return 'this is the home<br>go to <a href=\'/notthehome\'>not the home</a>'

@app.route('/notthehome')
def notthehome():
	return 'this is not the home<br>got to <a href=\'/\'>the home</a>'

if __name__ == '__main__':
	app.run('0.0.0.0', int(sys.argv[1]), debug=True)
