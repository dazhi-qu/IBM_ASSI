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

# CCAFS = spacex_df['CCAFS LC-40']
# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder="place holder here",
                 searchable=True
                 ),
    html.Div(dcc.Graph(id='success-pie-chart')),
    # html.Div(dcc.Graph(id='select-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback function to render success pie chart based on selected site
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(selected_site):
    filtered_df = spacex_df.copy()  # Avoid modifying original dataframe

    if selected_site == "ALL":
        pie_chart = px.pie(
            filtered_df, values="class", names='Launch Site', title='Success Rate by Launch Site'
        )
    else:
        df = filtered_df[filtered_df["Launch Site"] == selected_site]
        # print(selected_site)
        success_count = df[(df["class"] == 1)]["class"].count()
        fail_count = df[(df["class"] == 0)]["class"].count()
        pie_chart = px.pie(
            values=[success_count, fail_count],
            names=["Success", "Failure"],
            title=f"Launch Success Rates at {selected_site}",
        )

    return pie_chart


# 添加回调函数
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, selected_payload_range):
    if selected_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
