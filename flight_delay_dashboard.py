"""
FLIGHT DELAY VISUALIZATION DASHBOARD 2024 - VERCEL VERSION
Interactive Dashboard with 12 Visualizations + 3D Animated Plane Background
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# ====================================
# LOAD AND PREPARE DATA
# ====================================
print("Loading flight data...")

# Try to load from environment variable (for production) or local file (for development)
CSV_URL = os.getenv("CSV_URL")  # Set this in Vercel environment variables

if CSV_URL:
    # Production: load from URL
    df = pd.read_csv(CSV_URL)
    print(f"Loaded data from URL: {CSV_URL}")
else:
    # Development: load from local file
    try:
        df = pd.read_csv('flight delay/flight_data_2024_sample.csv')
        print("Loaded data from local file: flight delay/flight_data_2024_sample.csv")
    except FileNotFoundError:
        df = pd.read_csv('flight_data_2024_sample.csv')
        print("Loaded data from local file: flight_data_2024_sample.csv")

# Data preprocessing
df['fl_date'] = pd.to_datetime(df['fl_date'])
df['month_name'] = df['fl_date'].dt.month_name()
df['day_name'] = df['fl_date'].dt.day_name()

# Create delay categories
def categorize_delay(delay):
    if pd.isna(delay):
        return 'Unknown'
    elif delay <= -15:
        return 'Very Early'
    elif delay <= 0:
        return 'Early'
    elif delay <= 15:
        return 'On Time'
    elif delay <= 30:
        return 'Minor Delay'
    elif delay <= 60:
        return 'Moderate Delay'
    else:
        return 'Major Delay'

df['delay_category'] = df['arr_delay'].apply(categorize_delay)
df['on_time'] = df['arr_delay'].apply(lambda x: 1 if -15 <= x <= 15 else 0)

# Calculate total delays
df['total_delay_minutes'] = df[['carrier_delay', 'weather_delay', 'nas_delay', 
                               'security_delay', 'late_aircraft_delay']].sum(axis=1)

print(f"Data loaded successfully: {len(df)} records")

# ====================================
# CREATE FIGURES
# ====================================

def create_monthly_trends():
    monthly_data = df.groupby(['month_name', 'fl_date']).agg({
        'arr_delay': 'mean',
        'fl_date': 'count'
    }).rename(columns={'fl_date': 'flight_count'}).reset_index()
    
    fig = px.line(monthly_data, x='month_name', y='arr_delay', 
                  title='Average Delay by Month', color_discrete_sequence=['#00d4ff'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='#00ff88'
    )
    return fig

def create_carrier_performance():
    carrier_data = df.groupby('op_unique_carrier').agg({
        'arr_delay': 'mean',
        'fl_date': 'count'
    }).rename(columns={'fl_date': 'flight_count'}).reset_index()
    
    fig = px.bar(carrier_data, x='op_unique_carrier', y='arr_delay',
                 title='Average Delay by Carrier', color_discrete_sequence=['#ff6b6b'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='#00ff88',
        xaxis_title='Carrier'
    )
    return fig

# Create all figures
monthly_fig = create_monthly_trends()
carrier_fig = create_carrier_performance()

# ====================================
# INITIALIZE DASH APP
# ====================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Flight Delay Dashboard 2024"

# ====================================
# APP LAYOUT
# ====================================
app.layout = html.Div([
    html.H1("✈️ Flight Delay Analytics Dashboard 2024", 
            style={'textAlign': 'center', 'color': '#00ff88', 'marginBottom': '2rem'}),
    
    html.Div([
        dcc.Graph(figure=monthly_fig),
        dcc.Graph(figure=carrier_fig)
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '2rem'})
])

# ====================================
# VERCEL COMPATIBILITY
# ====================================
def handler(request):
    return app.server(request)

# For local development
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8001)