from bs4 import BeautifulSoup
from getdata import load_houseprices, load_populations, load_jobs
from getscores import get_houseprices_scores, get_populations_scores, get_jobs_scores, get_scores

#scores = get_houseprices_scores(load_houseprices())
#scores = get_populations_scores(load_populations())
#scores = get_jobs_scores(load_jobs('information-technology'))

scores = get_scores(load_jobs('financial-services'), load_populations(), load_houseprices())


# Load the SVG map
svg = open('data/us_counties.svg', 'r').read()
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

# Set the viewBox to scale the svg (for some reason, bs4 removes the capitalisation)
dimensions = soup.findAll('svg')[0]
soup.find('svg')['viewBox'] = dimensions['viewbox']
soup.find('svg')['preserveAspectRatio'] = dimensions['preserveaspectratio']

# Find counties
paths = soup.findAll('path')

# Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;'
path_style += 'stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;'
path_style += 'stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# Color the counties based on unemployment rate
for p in paths:
    if p['id'] not in ['State_Lines', 'separator']:
        # pass
        try:
            fips = (int(p['id'][:2]), int(p['id'][2:]))
            rate = scores[fips]
        except:
            continue
             
        ind = min(int(scores[fips]*5), 5)
        color = colors[ind]
        p['style'] = path_style + color

with open('test_counties.svg', 'w') as f:
    #f.write(soup.prettify())
    f.write(unicode(soup.body.next))
