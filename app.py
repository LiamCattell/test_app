from flask import Flask, render_template, request, make_response
from plotsvg import choropleth_svg
from getdata import load_houseprices, load_populations, load_jobs
from getscores import get_houseprices_scores, get_scores

app = Flask(__name__)

app.vars = {}


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


@app.route('/best_places_to_live', methods=['GET','POST'])
def best_places_to_live():
    if request.method == 'GET':
        return render_template('select_criteria.html')
    else:
        app.vars['criteria'] = request.form.getlist('criteria')

        return render_template('best_places_to_live.html', criteria=app.vars['criteria'])


@app.route('/counties_map.svg')
def counties_map():
    if 'houseprices' in app.vars['criteria']:
        scores = get_houseprices_scores(load_houseprices())
    else:
        scores = get_scores(load_jobs('financial-services'), load_populations(), load_houseprices())
    
    svg = choropleth_svg(scores)
    response = make_response(svg)
    response.headers['Content-Type'] = 'image/svg+xml'
    
    return response


if __name__ == "__main__":
	app.run()