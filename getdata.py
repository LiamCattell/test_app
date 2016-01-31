import pandas as pd
#import urllib2
#from bs4 import BeautifulSoup
#from re import sub


################################################################################
## FIPS DATA
################################################################################
#def get_fips_data(filepath='data/us_fips_codes.csv'):
#    """
#    Get the FIPS codes for each US county/state
#    """
#    fips = pd.read_csv(filepath)
#    return fips
#    
#
################################################################################
## AVERAGE HOUSE PRICES DATA
################################################################################
#def get_average_prices_data():
#    """
#    Get average house price in each state (via Trulia) and return dict
#    """
#    url = 'http://www.trulia.com/home_prices/'
#    header = {'User-Agent': 'Mozilla/5.0'}
#    req = urllib2.Request(url,headers=header)
#    page = urllib2.urlopen(req)
#    soup = BeautifulSoup(page)
#     
#    # Find div containing prices table
#    div = soup.find('div', { 'id' : 'heatmap_table' })
#    
#    prices = []
#    
#    for tab in div.findAll('table'):
#        for row in tab.findAll('tr')[2:]:
#            cells = row.findAll('td')
#            
#            if len(cells) > 2:
#                state = cells[0].find(text=True)
#                price_text = cells[1].find(text=True)
#                
#                if price_text != '-':
#                    price = float(sub(r'[^\d.]', '', cells[1].find(text=True)))
#                    prices.append([state.lower(), price])
#            
#    average_prices = pd.DataFrame(prices, columns=['state_long','average_price'])    
#    
#    # Add state abbreviations to prices dataframe
#    fips = get_fips_data()
#    average_prices = pd.merge(average_prices, fips.groupby(['state_long','state']).count().reset_index()[['state_long','state']], how='left', on=['state_long'])    
#    
#    average_prices_per_state = average_prices[['state','average_price']].set_index('state').to_dict()['average_price']
#    
#    return average_prices_per_state   
#
#
#def get_state_scores(jobs_per_state, prices_per_state):
#    scores_jobs = []
#    scores_prices = []
#    for state in jobs_per_state:
#        scores_jobs.append(float(jobs_per_state[state]))
#        scores_prices.append(float(prices_per_state[state]))
#    
#    max_job_score = max(scores_jobs)
#    max_price_score = max(scores_prices)
#    
#    scores = [(x/max_job_score)/(y/max_price_score) for x,y in zip(scores_jobs,scores_prices)]
#    max_score = max(scores)
#    scores = [x/max_score for x in scores]
#    
#    return dict(zip(jobs_per_state.keys(), scores))