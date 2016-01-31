from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/best_places_for_jobs', methods=['GET','POST'])
def best_places_for_jobs():
    if request.method == 'GET':
        return render_template('jobs_vs_prices.html')
    else:
        profession_key = request.form['profession_key']
    
        img_name = 'jobsdata_%s.png' % profession_key
        profession = profession_key.replace('-',' ').title()
        alt_text = 'The best places to live, based on %s job availability and house price.' % profession
    
        return render_template('jobs_vs_prices_graph.html', profession=profession, img_name=img_name, alt_text=alt_text)
        

@app.route('/best_places_for_budget', methods=['GET','POST'])
def best_places_for_budget():
    if request.method == 'GET':
        return render_template('prices_vs_jobs.html')
    else:
        max_price = request.form['max_price']
    
        img_name = 'pricedata_%s.png' % max_price
        alt_text = 'The best places to find technology jobs, based on your %s house budget.' % max_price
    
        return render_template('prices_vs_jobs_graph.html', max_price=max_price, img_name=img_name, alt_text=alt_text)


#@app.route('/jobs_vs_prices', methods=['POST'])
#def jobs_vs_prices():
#    profession_key = request.form['profession_key']
#    
#    img_name = 'jobsdata_%s.png' % profession_key
#    profession = profession_key.replace('-',' ').title()
#    alt_text = 'The best places to live, based on %s job availability and house price.' % profession
#
#    return render_template('jobs_vs_prices_graph.html', profession=profession, img_name=img_name, alt_text=alt_text)

	
if __name__ == "__main__":
	app.run()