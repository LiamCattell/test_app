from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('jobs_vs_prices.html')
    else:
        #request was a POST
        return render_template('jobs_vs_prices_graph.html')
	
if __name__ == "__main__":
	app.run()