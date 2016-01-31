from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello again, this works!'
	
if __name__ == "__main__":
	app.run()