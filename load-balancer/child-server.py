from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'this is the home<br>go to <a href=\'/notthehome\'>not the home</a>'

@app.route('/notthehome')
def notthehome():
	return 'this is not the home<br>got to <a hre=\'/home\'>the home</a>'

if __name__ == '__main__':
	app.run('0.0.0.0', 9003, debug=True)
