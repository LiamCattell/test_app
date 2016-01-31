from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('jobs_vs_prices.html')


@app.route('/jobs_vs_prices', methods=['POST'])
def jobs_vs_prices():
    script_f = open('test_plot_script.txt', 'r')
    script = script_f.read()
    
    div_f = open('test_plot_div.txt', 'r')
    div = div_f.read()


    return render_template('jobs_vs_prices_graph.html', script=script, div=div)
	
if __name__ == "__main__":
	app.run()