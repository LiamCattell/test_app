import pandas as pd
import numpy as np
from getdata import get_fips_data


def get_state_scores(jobs, prices):
    """
    Scale jobs/state by average house price/state
    """
    # Add state abbreviations to prices dataframe
    fips = get_fips_data()
    prices = pd.merge(prices, fips.groupby(['state_long','state']).count().reset_index()[['state_long','state']], how='left', on=['state_long'])

    jobs_per_state = jobs.groupby(['state'])['id'].count().to_dict()
    prices_per_state = prices[['state','average_price']].set_index('state').to_dict()['average_price']
    
    scores_jobs = []
    scores_prices = []
    for state in jobs_per_state:
        scores_jobs.append(float(jobs_per_state[state]))
        scores_prices.append(float(prices_per_state[state]))
    
    max_job_score = max(scores_jobs)
    max_price_score = max(scores_prices)
    
    scores = [(x/max_job_score)/(y/max_price_score) for x,y in zip(scores_jobs,scores_prices)]
    max_score = max(scores)
    scores = [x/max_score for x in scores]
    
    return dict(zip(jobs_per_state.keys(), scores))
    

def calculate_scores(per_county):
    scores = np.array(per_county.values())
    
    upper = np.percentile(scores, 75)
    lower = np.percentile(scores, 25)
    iqr = upper - lower
    
    #print scores.min(), lower, np.median(scores), upper, scores.max()
    
    scores[scores > upper+1.5*iqr] = upper+1.5*iqr
    scores[scores < lower-1.5*iqr] = lower-1.5*iqr
    
    scores -= scores.min()
    scores /= scores.max()
    
    return dict(zip(per_county.keys(), scores))

    
def get_jobs_scores(jobs):
    jobs_per_county = jobs.groupby(['fips'])['id'].count().to_dict()
    return calculate_scores(jobs_per_county)
    

def get_populations_scores(populations):
    fips = get_fips_data()
    popfips = pd.merge(fips[['state','county','fips_state','fips_county']], populations, on=['county', 'state'])
    
    growth_per_county = dict(zip(zip(popfips['fips_state'], popfips['fips_county']), (popfips['population2010']/popfips['population2000']) - 1.))
    return calculate_scores(growth_per_county)
    

def get_houseprices_scores(houseprices):
    fips = get_fips_data()
    pricefips = pd.merge(fips[['state','county','fips_state','fips_county']], houseprices, on=['county', 'state'])
    
    price_per_county = dict(zip(zip(pricefips['fips_state'], pricefips['fips_county']), -pricefips['average_price'].values))
    return calculate_scores(price_per_county)
       

def get_scores(criteria_scores):
    scores = []
    counties = []
    
    for fips in criteria_scores[0].iterkeys():
        try:
            score = 0.
            for s in criteria_scores:
                score += s[fips]
            scores.append(score)
            counties.append(fips)
        except:
            continue
    
    scores = np.array(scores) / max(scores)
    
    return dict(zip(counties, scores))