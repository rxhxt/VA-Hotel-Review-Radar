import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load DataFrame from CSV file
df = pd.read_csv("keyword_analysed_hotel_review.csv")

# Define function to generate radar chart for a given hotel
def generate_radar_chart(hotel_name):
    # Filter DataFrame for the selected hotel
    hotel_df = df[df['Name'] == hotel_name]
    
    # Relevant columns and labels
    columns = ['sanitation_score', 'food_score', 'hospitality_score', 'value_for_money_score', 'facilities_score']
    labels = ['Sanitation', 'Food', 'Hospitality', 'Value for Money', 'Facilities']
    
    # Calculate average scores for the selected hotel
    avg_scores = hotel_df[columns].mean()
    
    # Create trace for radar chart
    trace = go.Scatterpolar(
        r=avg_scores.values,
        theta=labels,
        fill='toself',
        name='Average Score'
    )

    # Create layout for the chart
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(avg_scores) + 1]
            )
        ),
        width=800,  # Adjust width of the chart
        height=600,  # Adjust height of the chart
        title=f'Relevance Scores for {hotel_name}'
    )

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig

# Get unique hotel names for dropdown options
hotel_names = df['Name'].unique()

# Create dropdown menu
dropdown_menu = [{'label': hotel_name, 'value': hotel_name} for hotel_name in hotel_names]

# Create initial radar chart with the first hotel in the list
initial_hotel = hotel_names[0]
initial_chart = generate_radar_chart(initial_hotel)

# Create Dash app
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

# Define callback to update radar chart based on dropdown selection
@app.callback(
    Output('radar-chart', 'figure'),
    [Input('hotel-dropdown', 'value')]
)
def update_radar_chart(selected_hotel):
    return generate_radar_chart(selected_hotel)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
