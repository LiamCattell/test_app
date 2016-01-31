from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('jobs_vs_prices.html')


@app.route('/jobs_vs_prices', methods=['POST'])
def jobs_vs_prices():
    profession_key = request.form['profession_key']
    
    img_name = 'jobsdata_%s.png' % profession_key
    profession = profession_key.replace('-',' ').title()
    alt_text = 'Available %s jobs (scaled by average house price)' % profession

    return render_template('jobs_vs_prices_graph.html', profession=profession, img_name=img_name, alt_text=alt_text)

	
if __name__ == "__main__":
	app.run()