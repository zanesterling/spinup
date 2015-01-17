from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'You\'ve found the webpage for Spinup!'

if __name__ == '__main__':
	app.run('0.0.0.0', 9001)
