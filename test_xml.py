import xml.etree.ElementTree as et
from getdata import load_houseprices
from getscores import get_houseprices_scores

scores = get_houseprices_scores(load_houseprices())

tree = et.parse('data/us_counties.svg')
root = tree.getroot()

# Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;'
path_style += 'stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;'
path_style += 'stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

#for p in root.findall('{http://www.w3.org/2000/svg}path'):
#    p.set('style', path_style+'#C994C7')
#    #print p.attrib['style']
    
for p in root.findall('{http://www.w3.org/2000/svg}path'):
    if p.attrib['id'] not in ['State_Lines', 'separator']:
        # Add tooltip
        #title = et.Element('{http://www.w3.org/2000/svg}title')
        #title.text = p.attrib['{http://www.inkscape.org/namespaces/inkscape}label']
        tooltip = p.attrib['{http://www.inkscape.org/namespaces/inkscape}label']
            
        try:
            fips = (int(p.attrib['id'][:2]), int(p.attrib['id'][2:]))
            ind = min(int(scores[fips]*5), 5)
            p.set('style', path_style + colors[ind])
            #title.text += '\nScore: %0.2f' % scores[fips]
            tooltip += '\nScore: %0.2f' % scores[fips]
        except:
            continue
        
        p.set('onmousemove', "ShowTooltip(evt, '%s')" % tooltip)
        #p.append(title)
        
      
tree.write('test_counties2.svg', method='html')