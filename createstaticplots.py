from getdata import load_jobs, get_average_prices_data
from getscores import get_state_scores
from plotchoropleth import choropleth_usa

prices = get_average_prices_data()

profession_keys = ['data-science', 'financial-services', 'information-technology', 'mobile-app']

for pk in profession_keys:
    jobs = load_jobs(pk)
    scores = get_state_scores(jobs, prices)
 
    choropleth_usa(scores, 'templates/jobsdata_%s.html' % pk, title='')