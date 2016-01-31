#import pandas as pd
#import urllib2
#from bs4 import BeautifulSoup
#from re import sub

def load_jobs_per_state(profession_key='data-science'):
    jobs = {}
    if profession_key == 'data-science':
        jobs = {u'va': 464, u'co': 309, u'ca': 383, u'al': 18, u'ar': 154, 
                u'vt': 8, u'il': 294, u'ga': 105, u'in': 67, u'ia': 6, 
                u'az': 339, u'id': 42, u'ct': 378, u'nh': 13, u'nj': 234, 
                u'nm': 8, u'tx': 382, u'la': 8, u'nc': 292, u'nd': 2, 
                u'ne': 46, u'tn': 66, u'ny': 605, u'pa': 290, u'ri': 213, 
                u'nv': 53, u'wa': 330, u'de': 97, u'dc': 100, u'wi': 60, 
                u'wv': 4, u'ma': 518, u'fl': 216, u'me': 32, u'md': 10, 
                u'ok': 32, u'oh': 171, u'ut': 279, u'mo': 144, u'mn': 302, 
                u'mi': 332, u'ks': 123, u'mt': 2, u'ms': 1, u'sc': 60, 
                u'ky': 75, u'or': 329, u'sd': 6}
    elif profession_key == 'financial-services':
        jobs = {u'va': 258, u'co': 310, u'ca': 437, u'al': 113, u'ar': 102, 
                u'vt': 37, u'il': 385, u'ga': 114, u'in': 159, u'ia': 75, 
                u'az': 404, u'id': 75, u'ct': 387, u'nh': 100, u'nj': 488, 
                u'nm': 89, u'tx': 463, u'la': 81, u'nc': 320, u'nd': 6, 
                u'ne': 84, u'tn': 128, u'ny': 513, u'pa': 309, u'ri': 119, 
                u'nv': 257, u'wa': 372, u'de': 116, u'dc': 306, u'wi': 178, 
                u'wv': 20, u'ma': 634, u'fl': 436, u'wy': 5, u'me': 46, 
                u'md': 49, u'ok': 64, u'oh': 358, u'ut': 127, u'mo': 394, 
                u'mn': 301, u'mi': 336, u'ks': 203, u'mt': 11, u'ms': 48, 
                u'sc': 110, u'ky': 60, u'or': 308, u'sd': 15}
    return jobs


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