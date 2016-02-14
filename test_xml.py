import xml.etree.ElementTree as et

tree = et.parse('data/us_counties.svg')
root = tree.getroot()

path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;'
path_style += 'stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;'
path_style += 'stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

for p in root.findall('{http://www.w3.org/2000/svg}path'):
    p.set('style', path_style+'#C994C7')
    print p.attrib['style']
      
tree.write('test_counties2.svg')