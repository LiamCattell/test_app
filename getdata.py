import pandas as pd
import urllib2
import requests
import random
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
# COUNTIES DATA
###############################################################################
def download_counties(fips, name_root='data/countydata'):
    """
    Get the corresponding county for every reasonably sized town and city in 
    the US (via http://www.citypopulation.de)
    """
    # Get a list of US states
    states_long = fips['state_long'].unique()
    states = fips['state'].unique()
    
    pairs = []
    
    # Loop over each state
    for state,state_long in zip(states,states_long):
        print state, state_long
        
        # Get the data page corresponding to this state
        url = 'http://www.citypopulation.de/php/usa-census-%s.php' % state_long.replace(' ','')
        header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
        req = urllib2.Request(url,headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
        
        # Find the table within the html
        table = soup.find('table', {'class': 'data', 'id': 'ts'})
        
        # Loop over the rows in the table
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            
            if len(cells) >= 3:
                city = cells[0].findAll(text=True)[0].lower()
                county = cells[2].findAll(text=True)[0].lower()
                
                # Some cities are in multiple counties
                for c in county.split(' / '):
                    c = c.replace('.', '')
                    c = c.replace("'", "")
                    pairs.append([state, state_long, city, c])
            
    counties = pd.DataFrame(pairs, columns=['state','state_long','city','county'])
    
    # Save the dataframe
    counties.to_pickle(name_root)
    print 'Saved counties data!'
    
    return
 
   
def load_counties(name_root='data/countydata'):
    """
    Load counties data from a pickle file
    """
    return pd.read_pickle(name_root)
    

###############################################################################
# POPULATION DATA
###############################################################################
def download_populations(fips, name_root='data/populationdata'):
    """
    Get the population of each US county from the last three censuses (censi?)
    """
    # Get a list of US states
    states_long = fips['state_long'].unique()
    states = fips['state'].unique()
    
    pairs = []
    
    # Loop over each state
    for state,state_long in zip(states,states_long):
        print state, state_long
        
        # Get the data page corresponding to this state
        url = 'http://www.citypopulation.de/php/usa-census-%s.php' % state_long.replace(' ','')
        header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
        req = urllib2.Request(url,headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
        
        # Find the table within the html
        table = soup.find('table', {'class': 'data', 'id': 'tl'})
        
        # Loop over the rows in the table
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            
            if len(cells) >= 5:
                county = cells[0].findAll(text=True)[0].lower()
                county = county.replace('.', '')
                county = county.replace("'", "")
                
                pops = []
                for i in range(2,5):
                    pop = cells[i].findAll(text=True)[0]
                    if pop == '...':
                        pops.append(None)
                    else:
                        pops.append(int(pop.replace(',','')))
    
                pairs.append([state, state_long, county] + pops)
                
    populations = pd.DataFrame(pairs, columns=['state','state_long','county','population1990','population2000','population2010'])
    
    # Save the dataframe
    populations.to_pickle(name_root)
    print 'Saved populations data!'
    
    return


def load_populations(name_root='data/populationdata'):
    """
    Load populations data from a pickle file
    """
    return pd.read_pickle(name_root)


###############################################################################
# JOBS DATA
###############################################################################
fips = get_fips_data()
counties = load_counties()

def split_location(x):
    """
    Split the default location column into city, state, country, county, and 
    FIPS code
    """
    empty = pd.Series(['n/a'] * 5)
    if (None in x[0]) or (x[0]['country'] != 'US'):
        print ' No location info'
        return empty

    city = x[0]['city'].lower()
    state = x[0]['state'].lower()
    country = x[0]['country'].lower()
    
    # Annoyingly, sometimes ApplyQ puts the county in the 'city' field, so we
    # have to check for that
    if 'county' in city:
        countys = counties.loc[(counties['state'] == state) & (counties['county'] == city.replace(' county','')), 'county'].values
    else:
        countys = counties.loc[(counties['state'] == state) & (counties['city'] == city), 'county'].values

    if len(countys) == 0:
        print 'No county'
        return empty
    # If the city is in multiple counties, randomly select a county
    county = countys[random.choice(range(len(countys)))]

    # Find the FIPS code that corresponds to the county
    codes = fips.loc[(fips['state'] == state) & (fips['county'] == county), ['fips_state','fips_county']].values
    if len(codes) != 1:
        print 'No FIPS code'
        return empty
    
    return pd.Series([city, state, country, county, tuple(codes[0])])


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
        jobs[['city','state','country', 'county', 'fips']] = jobs['location'].apply(split_location)
        jobs.drop('location', axis=1, inplace=True)
        jobs = jobs.loc[jobs['city'] != 'n/a']
    
        # Final tidying
        jobs = jobs.convert_objects(convert_numeric=True)
        
    if jobs is None:
        print 'Found None jobs'
    else:
        print 'Found %s %s jobs' % (len(jobs), search_params['pro'])
    
    return jobs
    

def download_jobs(profession_key, radius=70, name_root='data/jobsdata', num_cities_per_state=5):
    """
    Download and save jobs data as a pickle file
    """
    fips = get_fips_data()
    cities = get_cities_data()
    
    # Get state abbreviation from long state name
    cities = pd.merge(cities, fips.groupby(['state_long','state']).count().reset_index()[['state_long','state']], how='left', on=['state_long'])

    # Remove Hawaii and Alaska
    #cities = cities[(cities.state != 'hi') & (cities.state != 'ak')]
    cities = cities.loc[cities['rank'] < num_cities_per_state+1]
    
    search_params = {'pro': profession_key, 'radius': radius}

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
    Get average house price in each STATE (via Trulia)
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
    
    
def download_houseprices(fips, name_root='data/housepricesdata'):
    """
    Get average house price in each COUNTY (via Trulia)
    """
    # Get a list of US states
    states_long = fips['state_long'].unique()
    states = fips['state'].unique()
    
    prices = []
    
    # Loop over each state
    for state,state_long in zip(states,states_long):
        print state, state_long
    
        url = 'http://www.trulia.com/home_prices/%s/' % state_long.title().replace(' ','_')
        header = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
         
        # Find div containing prices table
        div = soup.find('div', { 'id' : 'heatmap_table' })
        
        for tab in div.findAll('table'):
            for row in tab.findAll('tr')[2:]:
                cells = row.findAll('td')
                
                if len(cells) > 2:
                    county = cells[0].find(text=True).lower()
                    county = county.replace(".","")
                    county = county.replace("'","")
                    
                    price_text = cells[1].find(text=True)
                    
                    if price_text != '-':
                        price = float(sub(r'[^\d.]', '', cells[1].find(text=True)))
                        prices.append([state, state_long, county, price])
            
    average_prices = pd.DataFrame(prices, columns=['state','state_long','county','average_price'])
    
    average_prices.to_pickle(name_root)
    print 'Saved houseprices data!'
    
    return
    

def load_houseprices(name_root='data/housepricesdata'):
    """
    Load average house price data from a pickle file
    """
    return pd.read_pickle(name_root)