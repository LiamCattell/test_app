import xml.etree.ElementTree as et

def choropleth_svg(scores):
    tree = et.parse('data/us_counties.svg')
    root = tree.getroot()
    
    root.set('type', 'image/svg+xml')
    
    # Map colors
    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
    
    path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;'
    path_style += 'stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;'
    path_style += 'stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'  
        
    for p in root.findall('{http://www.w3.org/2000/svg}path'):
        if p.attrib['id'] not in ['State_Lines', 'separator']:
            # Add a tooltip to label the state
            title = et.Element('{http://www.w3.org/2000/svg}title')
            title.text = p.attrib['{http://www.inkscape.org/namespaces/inkscape}label']  
            p.append(title)
            
            try:
                fips = (int(p.attrib['id'][:2]), int(p.attrib['id'][2:]))
                ind = min(int(scores[fips]*5), 5)
                p.set('style', path_style + colors[ind])
            except:
                continue
            
          
    #tree.write('static/test_counties.svg')
    #return    
    return et.tostring(root)