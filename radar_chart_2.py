import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


df = pd.read_csv("keyword_analysed_hotel_review.csv")


def generate_radar_chart(hotel_name):

    hotel_df = df[df['Name'] == hotel_name]
    columns = ['sanitation_score', 'food_score', 'hospitality_score', 'value_for_money_score', 'facilities_score']
    labels = ['Sanitation', 'Food', 'Hospitality', 'Value for Money', 'Facilities']
    avg_scores = hotel_df[columns].mean()
    trace = go.Scatterpolar(
        r=avg_scores.values,
        theta=labels,
        fill='toself',
        name='Average Score'
    )
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(avg_scores) + 1]
            )
        ),
        width=800, 
        height=600,  
        title=f'Relevance Scores for {hotel_name}'
    )
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig

hotel_names = df['Name'].unique()

dropdown_menu = [{'label': hotel_name, 'value': hotel_name} for hotel_name in hotel_names]

initial_hotel = hotel_names[0]
initial_chart = generate_radar_chart(initial_hotel)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='hotel-dropdown',
        options=dropdown_menu,
        value=initial_hotel
    ),
    dcc.Graph(
        id='radar-chart',
        figure=initial_chart
    )
])

@app.callback(
    Output('radar-chart', 'figure'),
    [Input('hotel-dropdown', 'value')]
)
def update_radar_chart(selected_hotel):
    return generate_radar_chart(selected_hotel)

if __name__ == '__main__':
    app.run_server(debug=True)
