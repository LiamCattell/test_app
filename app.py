from flask import Flask, render_template, request
from getdata import load_jobs
from plotchoropleth import choropleth_usa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('jobs_vs_prices.html')


@app.route('/jobs_vs_prices', methods=['POST'])
def jobs_vs_prices():
    #jobs = load_jobs('data-science')
    
    scores = {'ca': 3.4, 'tx': 0.7, 'nc': 2.1}
    script, div = choropleth_usa(scores, 'loaded some data')
    return render_template('jobs_vs_prices_graph.html', script=script, div=div)
	
if __name__ == "__main__":
	app.run()