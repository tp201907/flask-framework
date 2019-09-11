from flask import Flask, render_template, flash, request, send_from_directory
import pandas as pd
from yahoo_fin import stock_info as si
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import HoverTool, Plot
from bokeh.io import output_notebook, push_notebook, show



            
app_pradhan = Flask(__name__)
app_pradhan.config.from_object(__name__)
app_pradhan.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'





# We will look at stock prices over 2010
start = datetime.date(2010,1,1)
end = datetime.date.today()  

# Micosoft stock data
msft = si.get_data('msft', start, end).close
msft = pd.DataFrame(msft)
msft.reset_index(level=0, inplace=True)
#msft['date']=pd.to_datetime(msft['date'])
    

# Plot closing price of MSFT and user-selected stock
TOOLS = 'save,pan,box_zoom,reset,wheel_zoom,hover'   
plot = figure(plot_height=300, sizing_mode='scale_width', x_axis_type="datetime", tools = TOOLS)

plot.line(msft['date'], msft['close'], legend = "MSFT", color = "blue")
        
plot.xaxis.axis_label = 'Time'
plot.yaxis.axis_label = 'Close price in USD'
plot.legend.location = "top_left"

plot.select_one(HoverTool).tooltips = [
    ('Price', '@y'),
]


class ReusableForm(Form):
    name = TextField('Input a ticker to compare with MSFT:', validators=[validators.required()])

    @app_pradhan.route('/', methods=['GET','POST'])
    def input_ticker():

        form = ReusableForm(request.form)

        if request.method == 'POST':
            name = request.form['name']
            print(name)
        
        if form.validate():
        
            # We will look at stock prices over 2010
            start = datetime.date(2010,1,1)
            end = datetime.date.today()  

            anystock = si.get_data(name, start, end).close
            anystock = pd.DataFrame(anystock)
            anystock.reset_index(level=0, inplace=True)
            #anystock['date']=pd.to_datetime(msft['date'])
            
            plot.line(anystock['date'], anystock['close'], legend = name, color = "red")

            #output_file("stockchart.html", title = "Stock Chart")
            #show(plot)
        
        #return render_template('make user plot.html', form=form) 
        script, div = components(plot)
    
        return render_template('graph new.html', script=script, div=div, form=form)
        

@app_pradhan.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app_pradhan.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
   app_pradhan.run(port=33507)


