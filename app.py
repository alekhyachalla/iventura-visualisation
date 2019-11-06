import dash
import pandas as pd

import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from os import listdir
from os.path import isfile, join
import numpy as np
from plotly import graph_objs as go
import plotly_express as px
import dash_table
import pickle

chart_colors = ['#FF7F0E','#1F77B4', '#2CA02C']
charts_type = ['3D scatter','bar graph', 'pie chart','line graph','scatter']
two_dim_charts = ['3D scatter','bar graph','line graph','scatter']

USERNAME_PASSWORD_PAIRS=[
    ['ajay','prodevans'],['priyag','prodevans'],['alekhya','prodevans'],['iventura','prodevans']
    ]
app=dash.Dash(
     __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
suppress_callback_exceptions=True

gapminder = px.data.gapminder()

mypath = 'files/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

x_labels=['Negative', 'Neutral', 'Positive']
pie_colors = ['#FF7F0E','#1F77B4', '#2CA02C']


#  not so general stuff

infile2 = open("files/senti_predi.pickle","rb")
senti_df = pickle.load(infile2)
infile2.close()

# print('###################################')

# print(senti_df)

# print('###################################')

x1 = senti_df[senti_df['sent_textblob']=='negative']
neg_count = x1.shape[0]
# print("the negative count ", neg_count)

x2 = senti_df[senti_df['sent_textblob']=='positive']
pos_count = x2.shape[0]
# print("the positive count ", pos_count)

x3 = senti_df[senti_df['sent_textblob']=='neutral']
neutral_count = x3.shape[0]
# print("the nagative count ", neutral_count)


x_labels_general = []

# print(onlyfiles)
# dimensions = ["x", "y", "colour", "facet_col", "facet_row"]
app.layout = html.Div([

    html.H1(children='Welcome to Iventura Platform',style={
        'textAlign': 'center',
        'color': colors['text']}),
         html.Hr(),  # add a horizontal rule

         html.H2(" Data Detective Platform",style={
        'textAlign': 'center',
        'color': 'grey'}),
       

    html.H5(" Choose the data file"),
    dcc.Dropdown(
        id='file-dropdown',
        options=[{'label': k, 'value': k} for k in onlyfiles],
        value='train.csv'
    ),

    # html.Hr(),
    html.H5(" Choose the graph type"),
    dcc.Dropdown(
            id='graph-type',
            # options=[{'label': i, 'value': i} for i in charts_type],
            value=''
        ),

    html.Hr(),
    html.Div(id='output-data-upload'),
    html.Hr(),
    # original x and y dropdown options 
    html.Div([
    html.H5(" x :"),
    dcc.Dropdown(id='dropdowna'),
    html.H5(" y :"),
    dcc.Dropdown(id='dropdownb'),
    html.H5(" z/colour:"),
    dcc.Dropdown(id='dropdownc'),
    html.H5(" facet_col :"),
    dcc.Dropdown(id='dropdownd'),
    html.H5(" facet_row :"),
    dcc.Dropdown(id='dropdowne'),
    ],style={"width": "25%", "float": "left"},
    
    ),
    
    # html.Br(),
    # html.Br(),

    # html.Div(id='graph', style={'width': '75%', 'display': 'inline-block', 'padding': '0 20'}),
    dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),

])

def parse_path(filename):
    path=mypath+filename
    return path 

#  returns respective dataframe
def parse_file(filename):
    path = parse_path(filename)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        if isfile(path):
            df = pd.read_csv(path)
            return df
            
    elif 'pickle' in filename:
        # Assume that the user uploaded an pickle file
        infile = open(path,'rb')
        df =pickle.load(infile)
        infile.close()
        return df

#  returns the column values of the dataframe
def parse_contents(filename):
    df = parse_file(filename)
    return [dict(label=x, value=x) for x in df.columns]
 
# returns head values  of the file
def table(filename):
    df = parse_file(filename)
    df2 = df.head()
    return html.Div([
        html.H5("Record portion for "+filename),
        dash_table.DataTable(
            data=df2.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df2.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
                ),
    ])

def list_of_graphs(filename):
    if 'CCC' in filename:
        charts_type = ['3D scatter','line graph','scatter']
        return charts_type
    if 'forecast_sales' in filename:
        charts_type = ['3D scatter','bar graph','line graph','scatter']
        return charts_type
    if 'Fraud' in filename:
        charts_type = ['3D scatter','bar graph','line graph','scatter']
        return charts_type
    if 'senti_predi' in filename:
        charts_type = ['3D scatter','bar graph', 'pie chart','line graph','scatter']
        return charts_type
    if 'csv' in filename:
        charts_type = ['3D scatter','bar graph','line graph','scatter']
        return charts_type



@app.callback(dash.dependencies.Output('graph-type', 'options'),
              [dash.dependencies.Input('file-dropdown', 'value'),],
             )
def graph_list(filename):
    if filename is not None:
        graph_values = list_of_graphs(filename)
        print("**************** graph values", graph_values)
        return [{'label': i, 'value': i} for i in graph_values]

@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              [dash.dependencies.Input('file-dropdown', 'value'),
               dash.dependencies.Input('graph-type', 'value')],
             )
def update_output(filename, type_of_graph):
    if filename is not None:
        children=[
            table(filename)
        ]
        return children
    



@app.callback([
    dash.dependencies.Output('dropdowna', 'options'),
    dash.dependencies.Output('dropdownb', 'options'),
    dash.dependencies.Output('dropdownc', 'options'),
    dash.dependencies.Output('dropdownd', 'options'),
    dash.dependencies.Output('dropdowne', 'options')],
    [dash.dependencies.Input('file-dropdown', 'value')],
    [dash.dependencies.State('graph-type', 'value')])
def set_cities_optionsa(selected_filenamea, graph_type):
    # if graph_type in "scatter" :
    #     if selected_filenamea is not None:
    #         column_values = parse_contents(selected_filenamea)
    #         return column_values ,column_values , column_values, column_values, column_values
    # else:
    #     return [], [] , [] , [] , []
    if selected_filenamea is not None:
        column_values = parse_contents(selected_filenamea)
        return column_values ,column_values , column_values, column_values, column_values
    

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdowna', 'value'),
    dash.dependencies.Input('dropdownb', 'value'),
    dash.dependencies.Input('dropdownc', 'value'),  
    dash.dependencies.Input('dropdownd', 'value'),  
    dash.dependencies.Input('dropdowne', 'value'),
    dash.dependencies.Input('file-dropdown', 'value'),
    dash.dependencies.Input('graph-type', 'value')])
    
def make_figurea(x, y, colour, facet_col, facet_row, filename, type_of_graph):
    path = parse_path(filename)
    df_val = parse_file(filename)
    column_values = df_val.columns

    if x not in column_values:
        print("x is ", x)
        x = None
        print("x after none is ", x)
    if y not in column_values:
        print("x is ", y)
        y = None
        print("x after none is ", y)
    if colour not in column_values:
        print("x is ", colour)
        colour = None
        print("x after none is ", colour)
    if facet_col not in column_values:
        print("x is ", facet_col)
        facet_col = None
        print("x after none is ", facet_col)
    if facet_row not in column_values:
        print("x is ", facet_row)
        facet_row = None
        print("x after none is ", facet_row)
    pass_count = 5
        #  part 1 of trial
    # dropdown_list = ["x","y","colour","facet_col","facet_row"]
    # print("first drop down list",dropdown_list)
    # for p in dropdown_list:
    #     print(" globals", globals()[p])
    #     if globals()[p] in column_values:
    #         pass_count +=1
    #     elif globals()[p] not in column_values:
    #         print("p",globals()[p]," before none is ", globals()[p])
    #         globals()[p] = None
    #         print("p",globals()[p]," after none is ", globals()[p])
    #         pass_count +=1
    # dropdown_list2 = [x,y,colour,facet_col,facet_row]
    # print("second dropdown list", dropdown_list2)
    #  part2 of trial
    # pass_count=0
    # if (type_of_graph):
    #     for p in dropdown_list:
    #         if p in column_values or ( p == None):
    #             pass_count += 1
    #         if pass_count ==5:
    #             print("banzaiiiiiiiiiiiiiiiiiiiiiiiiiii")
    # else:
    #     #print some pop up message to give graph type
    #     print("pop up message")
    if(type_of_graph):
        if type_of_graph == "3D scatter":
            if 'csv' in path:
                tips=pd.read_csv(path)
                pass_count = 0
                return px.scatter_3d(
                tips,
                x=x,
                y=y,
                z = colour,
                color=colour,
                # facet_col=facet_col,
                # facet_row=facet_row,
                # height=700,
                )
            else:
                infile = open(path,'rb')
                df =pickle.load(infile)
                infile.close()
                pass_count = 0
                return px.scatter_3d(
                df,
                x=x,
                y=y,
                z=colour,
                # facet_col=facet_col,
                # facet_row=facet_row,
                # height=700,
                )
        elif type_of_graph == "scatter":
            if 'csv' in path:
                tips=pd.read_csv(path)
                pass_count = 0
                return px.scatter(
                tips,
                x=x,
                y=y,
                color=colour,
                facet_col=facet_col,
                facet_row=facet_row,
                height=700,
                )
            else:
                infile = open(path,'rb')
                df =pickle.load(infile)
                infile.close()
                pass_count = 0
                return px.scatter(
                df,
                x=x,
                y=y,
                color=colour,
                facet_col=facet_col,
                facet_row=facet_row,
                height=700,
                )
        elif type_of_graph in "bar graph":
            if 'csv' in path:
                tips=pd.read_csv(path)
                pass_count = 0
                return px.bar(
                tips,
                x=x,
                y=y,
                color=colour,
                facet_col=facet_col,
                facet_row=facet_row,
                height=700,
                )
            else:
                infile = open(path,'rb')
                df =pickle.load(infile)
                infile.close()
                pass_count = 0
                return px.bar(
                df,
                x=x,
                y=y,
                color=colour,
                facet_col=facet_col,
                facet_row=facet_row,
                height=700,
                )
        elif type_of_graph in "line graph":
            if 'csv' in path:
                tips=pd.read_csv(path)
                pass_count = 0
                return px.line(
                tips,
                x=x,
                y=y,
                color=colour,
                facet_col=facet_col,
                facet_row=facet_row,
                height=700,
                )
            else:
                infile = open(path,'rb')
                df =pickle.load(infile)
                infile.close()
                pass_count = 0
                return px.line(
                df,
                x=x,
                y=y,
                color=colour,
                facet_col=facet_col,
                facet_row=facet_row,
                height=700,
                )
        elif type_of_graph in "pie chart":
            if 'csv' in path:
                pass_count = 0
                print("csv pie")
                return piechart(filename)
            else:
                pass_count = 0
                print("pickle pie")
                return piechart(filename)
            
    else:
        return {}
        

# the following is something else

# @app.callback(
#     dash.dependencies.Output('graph', 'figure'),
#     [
#      dash.dependencies.Input('graph-type', 'value'),
#     ])
# def graphType( xaxis_column_name):
#     if xaxis_column_name in ['bar graph']:
#         return bargraph()
#     else:
#         return piechart()


# def bargraph():
#     return {
       
#         'data': [
#                  go.Bar(x=x_labels, y=[neg_count, neutral_count, pos_count], marker_color=colors),
#         ],
#     }

def piechart(filename):
    if 'senti_predi.pickle' in filename:
        return {
            'data': [
                    go.Pie(labels=x_labels, values=[neg_count, neutral_count, pos_count]),
                ],
        }
    if 'CCC.pickle' in filename:
        return {
    
        }
    if 'forecast_sales.pickle' in filename:
        return {
            'data': [
                    go.Pie(labels=x_labels, values=[neg_count, neutral_count, pos_count]),
                ],
        }
    if 'Fraud_detection.pickle' in filename:
        return {
            'data': [
                    go.Pie(labels=x_labels, values=[neg_count, neutral_count, pos_count]),
                ],
        }
    if 'csv' in filename:
        return {
        
        }

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')