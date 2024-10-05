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
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS', 'value': 'CCAFS'},
                                                    {'label': 'VAFB', 'value': 'VAFB'},
                                                    {'label': 'KSC', 'value': 'KSC'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # If 'ALL' is selected, show total success counts for all sites
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df, 
            names='Launch Site',  # Pie chart groups by launch site
            values='class',  # Sum of successes for each site
            title='Total Successful Launches by Site'
        )
    else:
        # Filter the data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Create a pie chart showing success vs failed launches for the selected site
        fig = px.pie(
            filtered_df, 
            names='class',  # Group by success (1) and failure (0)
            title=f'Success vs Failed Launches for {entered_site}',
            # Customize labels if needed: {1: 'Success', 0: 'Failed'}
        )

    # Return the figure to be rendered
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    # Filter the dataframe by payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    # If 'ALL' is selected, display data for all sites
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',  # Payload on the x-axis
            y='class',  # Launch outcome (success/failure) on the y-axis
            color='Booster Version Category',  # Color by Booster Version Category
            title='Correlation between Payload and Success for All Sites',
            labels={'class': 'Launch Outcome'}
        )
    else:
        # Filter dataframe for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

        # Create a scatter plot for the selected site
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {entered_site}',
            labels={'class': 'Launch Outcome'}
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
