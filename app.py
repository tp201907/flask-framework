from flask import Flask, render_template, flash, request, send_from_directory
import pandas as pd
import quandl
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import HoverTool, Plot
from bokeh.io import output_notebook, push_notebook, show
import os
import datetime

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# We will look at stock prices over 2010
start = datetime.date(2010,1,1)
end = datetime.date.today()  

# Micosoft stock data
msft = quandl.get('EOD/MSFT', start_date = start, end_date = end, authtoken="JZA5nXmNZk9T2Y96zsEQ")
msft = pd.DataFrame(msft)
msft.reset_index(level=0, inplace=True)
#msft['date']=pd.to_datetime(msft['date'])

# Plot closing price of MSFT and user-selected stock
TOOLS = 'save,pan,box_zoom,reset,wheel_zoom,hover'   
plot = figure(plot_height=300, sizing_mode='scale_width', x_axis_type="datetime", tools = TOOLS)

plot.line(msft['Date'], msft['Close'], legend = "MSFT", color = "blue")
        
plot.xaxis.axis_label = 'Time'
plot.yaxis.axis_label = 'Close price in USD'
plot.legend.location = "top_left"

plot.select_one(HoverTool).tooltips = [
    ('Price', '@y'),
]

# User chooses AAPL or IBM
class ReusableForm(Form):
    name = TextField('Compare AAPL or IBM with MSFT.', validators=[validators.required()])

    @app.route('/', methods=['GET','POST'])
    def input_ticker():

        form = ReusableForm(request.form)
        
        print(form.errors)
        if request.method == 'POST':
            name = request.form['name']
            print(name)
            stringcode = "EOD/" + str(name)
            print(stringcode)
            
        if form.validate():
        
            # We will look at stock prices over 2010
            start = datetime.date(2010,1,1)
            end = datetime.date.today()  
                       
            anystock = quandl.get(stringcode, start_date = start, end_date = end, returns="numpy", authtoken="JZA5nXmNZk9T2Y96zsEQ")
            anystock = pd.DataFrame(anystock)
            anystock.reset_index(level=0, inplace=True)
            #anystock['date']=pd.to_datetime(msft['date'])
            
            plot.line(anystock['Date'], anystock['Close'], legend = name, color = "red")

        script, div = components(plot)
        return render_template('graph new.html', script=script, div=div, form=form)
  
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
       
    #app.run(port=3456)
        
    app.run(port=33507)
    
    #port = int(os.environ.get("PORT", 5000))

