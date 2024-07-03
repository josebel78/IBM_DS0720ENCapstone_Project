# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="Select launch site",
                                                searchable=True
                                                ),                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', 
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),
                                html.Br(),
                                

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')[['class']].count()        
        title = 'Launch Success Rate by Site'
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class')[['class']].count()
        title = 'Launch Success Rate of ' + str(entered_site)
    fig = px.pie(filtered_df, 
                values='class',
                names=filtered_df.index,
                title=title)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value')])

def update_scatter_chart(entered_site, entered_range):
    if entered_site == 'ALL':
        site_filtered_df = spacex_df
        title = 'Correlation of Launch Success Rate with Payload Mass by Sites'
    else:
        # return the outcomes piechart for a selected site
        site_filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        title='Correlation of Launch Success Rate with Payload Mass in ' + str(entered_site)
    mask_low = site_filtered_df['Payload Mass (kg)'] >= entered_range[0]
    mask_high = site_filtered_df['Payload Mass (kg)'] <= entered_range[1]
    mask_payload = mask_low & mask_high
    filtered_df = site_filtered_df[mask_payload]
    fig = px.scatter(filtered_df, 
                x='Payload Mass (kg)', 
                y='class',
                color='Booster Version Category',
                #names=filtered_df.index,
                title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
