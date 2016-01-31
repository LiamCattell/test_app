from bokeh.sampledata import us_states
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import PuRd5

def choropleth_usa(scores, title='USA Chloropleth'):    
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
    
    return components(p)