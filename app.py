from flask import Flask, render_template, request
from plotchoropleth import choropleth_usa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('jobs_vs_prices.html')


@app.route('/jobs_vs_prices', methods=['POST'])
def jobs_vs_prices():
    #script = '<!-- ff -->'
    #div = '<h3>Backend working</h3>'

    scores = {'tx': 3.4, 'ca': 0.6, 'nc': 2.1}
    
    script, div = choropleth_usa(scores)

    return render_template('jobs_vs_prices_graph.html', script=script, div=div)
	
if __name__ == "__main__":
	app.run()