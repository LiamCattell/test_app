import pandas as pd
from getdata import get_fips_data, load_populations


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
    
    
def get_county_scores(jobs):
    jobs_per_county = jobs.groupby(['fips'])['id'].count().to_dict()
    
    max_job_score = float(max(jobs_per_county.values()))
    
    scores = [float(x)/max_job_score for x in jobs_per_county.values()]
    
    return dict(zip(jobs_per_county.keys(), scores))
    

fips = get_fips_data()
populations = load_populations()
popfips = pd.merge(fips[['state','county','fips_state','fips_county']], populations, on=['county', 'state'])

pop_per_county = dict(zip(zip(popfips['fips_state'], popfips['fips_county']), 1. - popfips['population2010']/popfips['population2000']))

min_pop_score = float(min(pop_per_county.values()))
max_pop_score = float(max(pop_per_county.values()))
new_max = max_pop_score - min_pop_score

scores = [(float(x)-min_pop_score)/new_max for x in pop_per_county.values()]
scores = dict(zip(pop_per_county.keys(), scores))