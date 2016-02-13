import pandas as pd
import urllib2
import requests
import geocoder
from bs4 import BeautifulSoup
from re import sub


"""
Functions to get:
    FIPS data (from .csv)
    Most populous cities in each US state (scraped from Wikipedia)
    Job postings (from Apply Q API)
        Note: can download from ApplyQ API, or load pre-downloaded data 
        directly from .pkl file
    Average house price for each US state (scraped from Trulia)
"""


###############################################################################
# FIPS DATA
###############################################################################
def get_fips_data(filepath='data/us_fips_codes.csv'):
    """
    Get the FIPS codes for each US county/state
    """
    fips = pd.read_csv(filepath)
    return fips

fips = get_fips_data()

###############################################################################
# CITIES DATA
###############################################################################
def get_cities_data():
    """
    Get most populous cities (via Wikipedia)
    """
    wiki = 'https://en.wikipedia.org/wiki/List_of_U.S._states%27_largest_cities_by_population'
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(wiki,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    
    # Find the table within the html
    table = soup.find('table', { 'class' : 'wikitable' })
     
    pairs = []
    
    # Loop over the rows in the table
    for row in table.findAll('tr'):
        cells = row.findAll('td')
        # For each 'tr', assign each 'td' to a variable
        if len(cells) >= 6:
            state = cells[0].findAll(text=True)[1].lower()
            for i in range(1,6):
                pairs.append([state, cells[i].find(text=True).lower(), i])
    
    cities = pd.DataFrame(pairs, columns=['state_long','city','rank'])
    
    return cities
    

###############################################################################
# JOBS DATA
###############################################################################
def split_location(x):
    """
    Split the default location column into city, state, country, latitude, 
    longitude, county, and FIPS code
    """
    empty = pd.Series(['n/a'] * 7)
    if (None in x[0]) or (x[0]['country'] != 'US'):
        #return pd.Series(['n/a', 'n/a', 'n/a'])
        return empty

    location = ', '.join(x[0].values())
    codes = [[0,0]]
    
    # Get the lat, lng, and county
    g = geocoder.google(location)
    if g.county is None:
        print 'None county'
        return empty

    # Find the FIPS code that corresponds to the county
    codes = fips.loc[(fips['state_long'] == g.state_long.lower()) & (fips['county'] == g.county.lower().replace(' county','')), ['fips_state','fips_county']].values
    if len(codes) != 1:
        return empty
    
    return pd.Series([v.lower() for v in x[0].values()] + [g.lat, g.lng, g.county.lower(), tuple(codes[0])])


def search_jobs(search_params={'pro': 'librarian', 'geo': 'durham, nc'}):
    """
    Search for jobs on ApplyQ based on some criteria
    """
    # Start session
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    
    # Get the jobs that meet the criteria
    jobs_raw = session.get('https://www.applyq.com/jobfeed_json', params=search_params)
    
    jobs = None
    
    # If there are jobs...
    if len(jobs_raw.json()['list']) > 0:
        jobs = pd.DataFrame(jobs_raw.json()['list'].values())
        
        # Clean up location get long state name from FIPS
        #jobs[['city','state','country']] = jobs['location'].apply(split_location)
        jobs[['city','state','country', 'latitude', 'longitude', 'county', 'fips']] = jobs['location'].apply(split_location)
        jobs.drop('location', axis=1, inplace=True)
        jobs = jobs.loc[jobs['city'] != 'n/a']
    
        # Final tidying
        jobs = jobs.convert_objects(convert_numeric=True)
        
    if jobs is None:
        print 'Found None jobs'
    else:
        print 'Found %s %s jobs' % (len(jobs), search_params['pro'])
    
    return jobs
    

def download_jobs(profession_key, name_root='data/jobsdata', num_cities_per_state=5):
    """
    Download and save jobs data as a pickle file
    """
    fips = get_fips_data()
    cities = get_cities_data()
    
    # Get state abbreviation from long state name
    cities = pd.merge(cities, fips.groupby(['state_long','state']).count().reset_index()[['state_long','state']], how='left', on=['state_long'])

    # Remove Hawaii and Alaska
    cities = cities[(cities.state != 'hi') & (cities.state != 'ak')]
    cities = cities.loc[cities['rank'] < num_cities_per_state+1]
    
    search_params = {'pro': profession_key}

    jobs = None
    
    for index, city in cities.iterrows():
        search_params['geo'] = city['city'] + ', ' + city['state']

        print search_params['geo']        
        
        new_jobs = search_jobs(search_params)
        
        if (new_jobs is not None) and (jobs is None):
            jobs = new_jobs
        elif (new_jobs is not None):
            jobs = pd.concat([jobs, new_jobs], ignore_index=True)
    
    jobs.to_pickle(name_root + '_' + profession_key)
    print 'Saved %s job data!' % profession_key
    
    return
    

def load_jobs(profession_key, name_root='data/jobsdata'):
    """
    Load jobs data from a pickle file
    """
    return pd.read_pickle(name_root + '_' + profession_key)


###############################################################################
# AVERAGE HOUSE PRICES DATA
###############################################################################
def get_average_prices_data():
    """
    Get average house price in each state (via Trulia)
    """
    url = 'http://www.trulia.com/home_prices/'
    header = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
     
    # Find div containing prices table
    div = soup.find('div', { 'id' : 'heatmap_table' })
    
    prices = []
    
    for tab in div.findAll('table'):
        for row in tab.findAll('tr')[2:]:
            cells = row.findAll('td')
            
            if len(cells) > 2:
                state = cells[0].find(text=True)
                price_text = cells[1].find(text=True)
                
                if price_text != '-':
                    price = float(sub(r'[^\d.]', '', cells[1].find(text=True)))
                    prices.append([state.lower(), price])
            
    average_prices = pd.DataFrame(prices, columns=['state_long','average_price'])    
    
    return average_prices