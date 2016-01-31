import pandas as pd
from getdata import load_jobs, get_average_prices_data, get_fips_data
from plotchoropleth import choropleth_usa


profession_keys = ['data-science', 'financial-services', 'information-technology', 'mobile-app']

jobs = None

for pk in profession_keys:
    if jobs is None:
        jobs = load_jobs(pk)
    else:
        new_jobs = load_jobs(pk)
        jobs = pd.concat((jobs, new_jobs), ignore_index=True)

jobs_per_state = jobs.groupby(['state'])['id'].count().to_dict()


prices = get_average_prices_data()

# Add state abbreviations to prices dataframe
fips = get_fips_data()
prices = pd.merge(prices, fips.groupby(['state_long','state']).count().reset_index()[['state_long','state']], how='left', on=['state_long'])

for p in range(12):
    max_price = 150000. + float(p)*50000
    prices_per_state = prices.loc[prices['average_price'] < max_price, ['state','average_price']].set_index('state').to_dict()['average_price']

    if len(prices_per_state) > 0:
        counts = []
        for state in prices_per_state:
            try:
                counts.append(float(jobs_per_state[state]))
            except KeyError:
                continue
    
        max_jobs = max(counts)
        counts = [v/max_jobs for v in counts]
        scores = dict(zip(jobs_per_state.keys(), counts))
    else:
        scores = {}
    
    choropleth_usa(scores, 'templates/pricedata_%s.html' % int(max_price), title='')