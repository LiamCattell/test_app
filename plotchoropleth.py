from bokeh.sampledata import us_states, us_counties
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import PuRd5


def choropleth_usa_states(scores, filename, title='USA States Choropleth'):
    """
    Plot choropleth of US states based on a score for each state
    """
    states = us_states.data.copy()
    
    del states['HI']
    del states['AK']
    
    state_xs = [states[code]['lons'] for code in states]
    state_ys = [states[code]['lats'] for code in states]
    
    state_colors = []
    for state in states:
        try:
            ind = 4 - min(int(scores[state.lower()]*4), 4)
            state_colors.append(PuRd5[ind])
        except KeyError:
            state_colors.append('white')
    
    p = figure(title=title, toolbar_location='left', plot_width=1100, plot_height=700)
    
    p.patches(state_xs, state_ys, fill_color=state_colors, fill_alpha=0.7,
        line_color='#884444', line_width=2)
    
    output_file(filename, title=title)

    show(p)
    
    return
    

def choropleth_usa_counties(scores, filename, title='USA Counties Choropleth'):
    """
    Plot choropleth of US counties based on a score for each county
    """
    states = us_states.data.copy()
    counties = us_counties.data.copy()
    
    del states['HI']
    del states['AK']
    
    state_xs = [states[code]['lons'] for code in states]
    state_ys = [states[code]['lats'] for code in states]
    
    county_xs = [counties[code]['lons'] for code in counties if counties[code]['state'] not in ['ak', 'hi', 'pr', 'gu', 'vi', 'mp', 'as']]
    county_ys = [counties[code]['lats'] for code in counties if counties[code]['state'] not in ['ak', 'hi', 'pr', 'gu', 'vi', 'mp', 'as']]
    
    county_colors = []
    for county in counties:
        if counties[county]['state'] in ['ak', 'hi', 'pr', 'gu', 'vi', 'mp', 'as']:
            continue
        try:
            ind = 4 - min(int(scores[county]*4), 4)
            county_colors.append(PuRd5[ind])
        except KeyError:
            county_colors.append('white')
    
    p = figure(title=title, toolbar_location='left', plot_width=1100, plot_height=700)
    
    p.patches(county_xs, county_ys, fill_color=county_colors, fill_alpha=0.7, line_color='#DDDDDD', line_width=0.5)
    p.patches(state_xs, state_ys, fill_alpha=0.0, line_color='#884444', line_width=2)
    
    output_file(filename, title=title)

    show(p)
    
    return