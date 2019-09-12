{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, render_template, flash, request, send_from_directory\n",
    "import pandas as pd\n",
    "import quandl\n",
    "from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField\n",
    "from bokeh.plotting import figure, output_file, show\n",
    "from bokeh.embed import components\n",
    "from bokeh.models import HoverTool, Plot\n",
    "from bokeh.io import output_notebook, push_notebook, show\n",
    "import os\n",
    "import datetime\n",
    "\n",
    "app = Flask(__name__)\n",
    "app.config.from_object(__name__)\n",
    "app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'\n",
    "\n",
    "# We will look at stock prices over 2010\n",
    "start = datetime.date(2010,1,1)\n",
    "end = datetime.date.today()  \n",
    "\n",
    "# Micosoft stock data\n",
    "msft = quandl.get('EOD/MSFT', start_date = start, end_date = end, authtoken=\"JZA5nXmNZk9T2Y96zsEQ\")\n",
    "msft = pd.DataFrame(msft)\n",
    "msft.reset_index(level=0, inplace=True)\n",
    "#msft['date']=pd.to_datetime(msft['date'])\n",
    "\n",
    "# Plot closing price of MSFT and user-selected stock\n",
    "TOOLS = 'save,pan,box_zoom,reset,wheel_zoom,hover'   \n",
    "plot = figure(plot_height=300, sizing_mode='scale_width', x_axis_type=\"datetime\", tools = TOOLS)\n",
    "\n",
    "plot.line(msft['Date'], msft['Close'], legend = \"MSFT\", color = \"blue\")\n",
    "        \n",
    "plot.xaxis.axis_label = 'Time'\n",
    "plot.yaxis.axis_label = 'Close price in USD'\n",
    "plot.legend.location = \"top_left\"\n",
    "\n",
    "plot.select_one(HoverTool).tooltips = [\n",
    "    ('Price', '@y'),\n",
    "]\n",
    "\n",
    "# User chooses AAPL or IBM\n",
    "class ReusableForm(Form):\n",
    "    name = TextField('Compare AAPL or IBM with MSFT.', validators=[validators.required()])\n",
    "\n",
    "    @app.route('/', methods=['GET','POST'])\n",
    "    def input_ticker():\n",
    "\n",
    "        form = ReusableForm(request.form)\n",
    "        \n",
    "        print(form.errors)\n",
    "        if request.method == 'POST':\n",
    "            name = request.form['name']\n",
    "            print(name)\n",
    "            stringcode = \"EOD/\" + str(name)\n",
    "            print(stringcode)\n",
    "            \n",
    "        if form.validate():\n",
    "        \n",
    "            # We will look at stock prices over 2010\n",
    "            start = datetime.date(2010,1,1)\n",
    "            end = datetime.date.today()  \n",
    "                       \n",
    "            anystock = quandl.get(stringcode, start_date = start, end_date = end, returns=\"numpy\", authtoken=\"JZA5nXmNZk9T2Y96zsEQ\")\n",
    "            anystock = pd.DataFrame(anystock)\n",
    "            anystock.reset_index(level=0, inplace=True)\n",
    "            #anystock['date']=pd.to_datetime(msft['date'])\n",
    "            \n",
    "            plot.line(anystock['Date'], anystock['Close'], legend = name, color = \"red\")\n",
    "\n",
    "        script, div = components(plot)\n",
    "        return render_template('graph new.html', script=script, div=div, form=form)\n",
    "  \n",
    "@app.route('/favicon.ico')\n",
    "def favicon():\n",
    "    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    #app.run()\n",
    "    #port = int(os.environ.get(\"PORT\", 5000))\n",
    "    #app.run(host='0.0.0.0', port=port)\n",
    "    app.run(port=33507)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
