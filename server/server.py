from flask import Flask, render_template

app = Flask(__name__)

# webpage and ui
@app.route('/')
def home():
	return render_template('home.html')
	return 'You\'ve found the webpage for Spinup!'

# daemon interaction
@app.route('/service', methods=['POST'])
def service():
	return 'accepted'

if __name__ == '__main__':
	app.run('0.0.0.0', 9001, debug=True)
