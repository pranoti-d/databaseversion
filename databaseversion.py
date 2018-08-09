from app import server
from app import app
from app.models import test_data_dummy_data

import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from bisect import bisect_left
from datetime import datetime
from copy import deepcopy
import plotly.graph_objs as go
from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_migrate import Migrate

server = Flask(__name__)
app = dash.Dash(__name__, server=server, static_folder='assets')


server.config.from_object(Config)
#db = SQLAlchemy(server)
#migrate = Migrate(server, db)
#data = db.session.query(test_data_dummy_data).all()


# In[2]:


file = pd.read_csv( "Test_Data_Dummy_Data.csv", encoding = "ISO-8859-1")
file.iloc[:,14:50] = file.iloc[:,14:50].apply(lambda x : x.astype('float'))
file.iloc[:,14:50] = file.iloc[:,14:50].apply(lambda x : round(x, 2))


# In[ ]:


def select_chart(x_axis,y_axis,chart_type) :
    data_chart = file
    dataPanda = []
    dataPanda = create_trace(data_chart,x_axis,y_axis,chart_type,dataPanda)
    return dataPanda
     
    
def create_trace(data_chart,x_axis,y_axis,chart_type,dataPanda):    
    if (x_axis == 'Date'):
            dataPanda = create_date_trace(data_chart,x_axis,y_axis,chart_type,dataPanda)
    else:
            dataPanda = create_other_trace(data_chart,x_axis,y_axis,chart_type,dataPanda)
    return dataPanda


def create_date_trace(data_chart,x_axis,y_axis,chart_type,dataPanda) : 
    x=data_chart[data_chart['Metric'] == y_axis]['Date']
    if (chart_type == 'scatter'): 
            for i in data_chart.iloc[:,14:50].columns.unique():
                trace = go.Scatter(
                    x=x,
                    y=data_chart[data_chart['Metric'] == y_axis][i],
                    text= i,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i  ) 
                dataPanda.append(trace)
    else:            
        if (chart_type == 'line'): 
            for i in data_chart.iloc[:,14:50].columns.unique():
                    trace = go.Scatter(
                            x=x,
                            y=data_chart[data_chart['Metric'] == y_axis][i],
                            text= i,
                            mode = 'lines',
                            opacity=0.7,
                            name=i  ) 
                    dataPanda.append(trace)
        else:            
            if (chart_type == 'bar'): 
                for i in data_chart.iloc[:,14:50].columns.unique():
                        trace = go.Bar(
                            x=x,
                            y=data_chart[data_chart['Metric'] == y_axis][i],
                            text= i,
                            opacity=0.7,
                            name=i  ) 
                        dataPanda.append(trace)            
    return dataPanda

def create_other_trace(data_chart,x_axis,y_axis,chart_type,dataPanda) : 
    if (chart_type == 'scatter'): 
            for i in data_chart.iloc[:,14:50].columns.unique():
                trace = go.Scatter(
                    x=data_chart[data_chart['Metric'] == x_axis][i],
                    y=data_chart[data_chart['Metric'] == y_axis][i],
                    text= i,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i  ) 
                dataPanda.append(trace)
    else :            
        if (chart_type == 'line'): 
            for i in data_chart.iloc[:,14:50].columns.unique():
                    trace = go.Scatter(
                                x=data_chart[data_chart['Metric'] == x_axis][i],
                                y=data_chart[data_chart['Metric'] == y_axis][i],
                                text= i,
                                mode = 'lines',
                                opacity=0.7,
                                name=i  ) 
                    dataPanda.append(trace)
        else:            
            if (chart_type == 'bar'): 
                    for i in data_chart.iloc[:,14:50].columns.unique():
                            trace = go.Bar(
                                    x=data_chart[data_chart['Metric'] == x_axis][i],
                                    y=data_chart[data_chart['Metric'] == y_axis][i],
                                    text= i,
                                    opacity=0.7,
                                    name=i  ) 
                            dataPanda.append(trace)            
    return dataPanda


    
def create_layout(x_axis,y_axis) : 
    layout =  go.Layout(
               # autosize=False,
               # width=1000,
                height=700,
                xaxis = dict(title= x_axis),
                yaxis=dict(title=y_axis),
                legend=dict(orientation="h"),
                hovermode='closest'
            )
    return layout


# In[ ]:


#app = dash.Dash(__name__, static_folder='assets')
# app.scripts.config.serve_locally=True
# app.css.config.serve_locally=True
# app.config.supress_callback_exceptions=True


#app = dash.Dash(__name__, server=server, static_folder='assets')

#Define x and y axis options

x_axis_list = file['Metric'].unique().tolist()
y_axis_list = file['Metric'].unique().tolist()
x_axis_list.append('Date')


app.css.append_css({'external_url':
#                 'https://cdn.rawgit.com/gschivley/8040fc3c7e11d2a4e7f0589ffc829a02/raw/fe763af6be3fc79eca341b04cd641124de6f6f0d/dash.css'
                  'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
               })
app.title = 'States of India'
#server = app.server

app.layout = html.Div([
    # title row
    html.Div(
        [
            html.H1(
                'States of India',
                style={'font-family': 'Helvetica',
                       "margin-top": "25",
                       "margin-bottom": "0"},
                className='eight columns',
            ),
             html.P(
                'Explore states of India',
                style={'font-family': 'Helvetica',
                       "font-size": "120%",
                       "width": "80%"},
                className='eight columns',
            ),
        ], 
         className='row'
        ),
    
    # Select visualization
    
     html.Div(
        [
             html.Label('What would you like to visualize?'),
                 dcc.Dropdown(
                    options=[
                        {'label': 'Economy', 'value': 'NYC'},
                        {'label': 'Banking', 'value': 'MTL'},
                        {'label': 'States', 'value': 'SF'}
                            ],
                     value=['MTL', 'SF'],
                     multi=True
                             ),
         ], 
         className='row'
        ),
    
    # selectors
   html.Div(
        [ 
     html.Div(
        [
            html.P('Choose x-axis:'), 
            dcc.Dropdown(
                    id='x_axis',
                    options=[{'label': k, 'value': k} for k in x_axis_list],               
                    value='Date'
                        )
            ],
           className='four columns',
           style={'margin-top': '10'}
     ),
    
    html.Div(
        [
            html.P('Choose y-axis:'), 
            dcc.Dropdown(
                    id='y_axis',
                    options=[{'label': k, 'value': k} for k in y_axis_list],               
                    value='Scheduled Commercial  Bank Offices'
                        )
            ],
           className='four columns',
           style={'margin-top': '10'}
     ),
    
       html.Div(
        [
            html.P('Choose chart-type:'), 
            dcc.Dropdown(
                    id='chart_type',
                    options=[{'label': 'Scatter', 'value': 'scatter'},
                             {'label': 'Line', 'value': 'line'},
                             {'label': 'Bar', 'value': 'bar'}],
                    value='scatter'
                        )
            ],
           className='four columns',
           style={'margin-top': '10'}
     )
        ], className='row'
   ),
    
  #chart
     html.Div(
        [
            dcc.Graph(id='example-graph',
                              #animate=True, 
                              style={'margin-top': '20'}
                              , config = {'showLink': true} 
                              #,config={'displayModeBar': False}
                     )
        ], className='row'
         ),
    
    dcc.Markdown('Created by [Ashutosh Datar](https://twitter.com/adatar)')
   
], className='ten columns offset-by-one')    

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('x_axis', 'value'),
    dash.dependencies.Input('y_axis', 'value'),
    dash.dependencies.Input('chart_type', 'value'),
    ])
def update_output(x_axis, y_axis, chart_type):
    dataPanda = select_chart(x_axis,y_axis,chart_type)
    layout = create_layout(x_axis,y_axis)
    figure = {'data': dataPanda,
            'layout': layout}
    return figure  
    

if __name__ == '__main__':
    app.run_server(debug=True)
