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
print(spacex_df.columns)
values_launch_site =  spacex_df["Launch Site"].unique()
launch_site = pd.DataFrame(values_launch_site, columns=['LaunchSite'])

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
                                        {'label': launch_site.iloc[0,0], 'value': launch_site.iloc[0,0]},
                                        {'label': launch_site.iloc[1,0], 'value': launch_site.iloc[1,0]},
                                        {'label': launch_site.iloc[2,0], 'value': launch_site.iloc[2,0]},
                                        {'label': launch_site.iloc[3,0], 'value': launch_site.iloc[3,0]},
                                        ],
                                    value='ALL',
                                    placeholder="Select Launch Site here",
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
                                    min=0, max=10000, step=100,
                                    marks={0: '0', 5000: '5000',
                                    10000: '10000'},
                                    value=[3000, 5000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    filtered_df.rename(columns={"Launch Site": "launchSite"},inplace=True)
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='launchSite',
        title='Successful Landings')
        return fig
    else:
        filtered_ls = filtered_df[filtered_df.launchSite == entered_site]
        filtered_ls['count'] = 1
        filtered_ls = filtered_ls.groupby('class').count().reset_index()
        filtered_ls["class"].replace({0: "failed", 1: "succeed"}, inplace=True)
        fig = px.pie(filtered_ls, values='count',
        names='class',
        title= 'Landing Outcome '+entered_site)
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value"))
def get_pie_chart(entered_site,rangeSlider):
    scatter_df = spacex_df
    scatter_df.rename(columns={"Launch Site": "launchSite","Payload Mass (kg)":"payload"},inplace=True)
    scatter_filtered = scatter_df[(scatter_df.payload >= rangeSlider[0]) & (scatter_df.payload <= rangeSlider[1])]

    if entered_site == 'ALL':
        fig = px.scatter(scatter_filtered, x="payload", y="class", color="Booster Version Category")
        return fig
    else:
        scatter_filtered_plus = scatter_filtered[scatter_filtered.launchSite == entered_site]
        #scatter_filtered_plus['count'] = 1
        #scatter_filtered_plus = scatter_filtered_plus.groupby('class').count().reset_index()
        fig = px.scatter(scatter_filtered_plus, x="payload", y="class", color="Booster Version Category")

        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
