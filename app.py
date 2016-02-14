from flask import Flask, render_template, request, redirect
from plotsvg import choropleth_svg
from getdata import load_houseprices
from getscores import get_houseprices_scores

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


@app.route('/test_counties')
def test_counties():
    scores = {(34, 7): 0, (19, 113): 0, (19, 19): 0, (42, 71): 0, (13, 121): 0, 
              (47, 149): 0, (36, 17): 0, (48, 439): 0, (12, 31): 0, (1, 83): 0,
              (32, 31): 0, (39, 17): 0, (12, 115): 0, (37, 97): 0, (8, 5): 1, 
              (30, 13): 0, (12, 117): 0, (1, 117): 0, (34, 29): 0, (47, 37): 0,
              (34, 23): 0, (4, 19): 0, (45, 35): 0, (39, 45): 0, (39, 151): 0, 
              (8, 41): 0, (19, 153): 0, (54, 39): 0, (48, 367): 0, (31, 19): 0, 
              (27, 131): 0, (38, 17): 0, (29, 47): 0, (20, 45): 0, (26, 161): 0, 
              (24, 37): 0, (26, 125): 1, (9, 3): 1, (6, 85): 1, (53, 67): 0, 
              (1, 101): 0, (49, 35): 1, (21, 37): 0, (12, 11): 0, (19, 13): 0, 
              (18, 127): 0, (25, 21): 1, (37, 183): 0, (20, 209): 0, 
              (29, 37): 0, (44, 3): 0, (12, 97): 0, (1, 89): 0, (22, 71): 0, 
              (45, 15): 0, (51, 59): 1, (8, 31): 1, (36, 5): 0, (36, 55): 0, 
              (17, 163): 0, (39, 113): 0, (40, 145): 0, (6, 87): 0, (8, 101): 0, 
              (36, 29): 0, (17, 197): 0, (8, 35): 0, (29, 95): 0, (25, 5): 0, 
              (9, 9): 0, (39, 165): 0, (1, 73): 0, (34, 25): 0, (48, 473): 0, 
              (21, 49): 0, (37, 119): 1, (10, 3): 1, (22, 33): 0, (39, 41): 0, 
              (48, 113): 0, (39, 61): 0, (42, 11): 0, (37, 81): 0, (18, 5): 0, 
              (41, 67): 1, (39, 153): 0, (9, 11): 0, (32, 3): 0, (5, 119): 0, 
              (28, 89): 0, (18, 97): 0, (39, 35): 0, (6, 73): 1, (37, 63): 1, 
              (26, 81): 0, (18, 57): 0, (37, 71): 0, (25, 25): 1, (18, 145): 0, 
              (37, 179): 0, (12, 95): 0, (17, 89): 0, (13, 247): 0, (36, 85): 0, 
              (51, 87): 0, (27, 137): 0, (8, 69): 0, (29, 165): 0, (40, 143): 0, 
              (9, 13): 0, (23, 5): 0, (37, 37): 0, (27, 53): 1, (5, 7): 1, 
              (12, 57): 1, (24, 25): 0, (47, 157): 0, (12, 81): 0, (51, 99): 0, 
              (40, 17): 0, (54, 33): 0, (45, 63): 0, (25, 9): 0, (48, 397): 0, 
              (48, 209): 0, (36, 67): 0, (8, 13): 0, (45, 19): 0, (34, 21): 0, 
              (26, 163): 1, (48, 257): 0, (49, 51): 0, (22, 103): 0, (27, 37): 0, 
              (41, 5): 1, (40, 27): 0, (48, 141): 0, (12, 86): 0, (25, 23): 0, 
              (42, 95): 0, (13, 215): 0, (18, 67): 0, (39, 49): 0, (42, 17): 0, 
              (46, 83): 0, (36, 47): 0, (33, 17): 0, (21, 67): 0, (4, 13): 1, 
              (47, 93): 0, (48, 497): 0, (48, 339): 0, (33, 11): 0, (37, 67): 0, 
              (20, 173): 0, (48, 491): 0, (21, 111): 0, (40, 109): 0, (17, 93): 0, 
              (36, 81): 0, (2, 20): 0, (34, 33): 0, (17, 31): 1, (30, 49): 0, 
              (6, 59): 1, (35, 49): 0, (55, 25): 0, (12, 53): 0, (13, 129): 0, 
              (21, 117): 0, (48, 201): 0, (49, 43): 0, (46, 103): 0, (5, 45): 0, 
              (16, 27): 0, (29, 183): 0, (48, 85): 0, (39, 159): 0, (42, 129): 0, 
              (51, 13): 1, (9, 1): 1, (23, 27): 0, (25, 17): 1, (24, 41): 0, 
              (36, 103): 0, (55, 133): 0, (27, 123): 0, (42, 49): 0, (47, 187): 0, 
              (35, 1): 0, (41, 9): 0, (15, 3): 0, (25, 27): 0, (42, 91): 0, 
              (55, 79): 0, (42, 29): 0, (39, 89): 0, (12, 99): 0, (42, 101): 1, 
              (17, 91): 0, (45, 13): 0, (8, 1): 0, (29, 135): 0, (45, 79): 0, 
              (36, 119): 0, (13, 135): 0, (55, 139): 0, (48, 121): 0, (55, 89): 0, 
              (42, 3): 1, (49, 49): 1, (6, 37): 0, (48, 453): 0, (29, 189): 0, 
              (45, 3): 0, (48, 157): 0, (42, 45): 0, (53, 11): 0, (48, 29): 0, 
              (37, 45): 0, (36, 59): 0, (39, 57): 0, (46, 99): 0, (55, 101): 0, 
              (29, 77): 0, (18, 105): 0, (26, 139): 0, (51, 149): 0, (6, 19): 0, 
              (31, 109): 0, (18, 3): 0, (12, 103): 0, (36, 61): 0, (6, 107): 0, 
              (44, 7): 1, (13, 245): 0, (42, 19): 0, (17, 97): 0, (47, 65): 0, 
              (41, 71): 0, (31, 55): 0, (53, 33): 1, (41, 51): 1, (37, 61): 0, (20, 91): 1}

    scores_prices = get_houseprices_scores(load_houseprices())
    
    choropleth_svg(scores_prices)
    
    return redirect('/test_counties_graph')
    #return render_template('test_counties.html', img_name='test_counties.svg', alt_text='testx')
    #return render_template('test_counties.html', svg_image=svg)
    #return render_template('test_counties.html', svg_image=svg), 200, {'Content-Type': 'image/svg+xml'}
    #return Response(svg, mimetype='image/svg+xml')
    
@app.route('/test_counties_graph')
def test_counties_graph():
    return render_template('test_counties.html', img_name='test_counties.svg', alt_text='testx')

if __name__ == "__main__":
	app.run()