from bs4 import BeautifulSoup

def choropleth_svg(scores):
    # Load the SVG map
    svg = open('data/us_counties.svg', 'r').read()
    soup = BeautifulSoup(svg, 'xml')
    
    # Find counties
    paths = soup.findAll('path')
    
    # Map colors
    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
    
    path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;'
    path_style += 'stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;'
    path_style += 'stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'
    
    # Color the counties
    for p in paths:
        if p['id'] not in ['State_Lines', 'separator']:
            # pass
            try:
                fips = (int(p['id'][:2]), int(p['id'][2:]))
            except:
                continue
                 
            ind = min(int(scores[fips]*5), 5)
            color = colors[ind]
            p['style'] = path_style + color
    
#    with open('static/test_counties.svg', 'w') as f:
#        f.write(soup.prettify())
        #f.write(unicode(soup.body.next))
        
    return soup.prettify()
