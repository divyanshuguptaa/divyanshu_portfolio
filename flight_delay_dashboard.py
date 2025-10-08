"""
FLIGHT DELAY VISUALIZATION DASHBOARD 2024
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
warnings.filterwarnings('ignore')

# ====================================
# LOAD AND PREPARE DATA
# ====================================
print("Loading flight data...")
import os

# Try to load from environment variable (for production) or local file (for development)
CSV_URL = os.getenv("CSV_URL")  # Set this in Render environment variables

if CSV_URL:
    # Production: load from URL (Google Drive) with timeout handling
    print(f"Attempting to load data from URL...")
    print(f"This may take a few minutes for large files...")
    try:
        # Set longer timeout for large file downloads
        import socket
        socket.setdefaulttimeout(300)  # 5 minutes timeout
        df = pd.read_csv(CSV_URL, low_memory=False)
        print(f"✓ SUCCESS! Loaded data from URL")
        print(f"✓ Total records: {len(df):,}")
    except Exception as e:
        print(f"⚠ Error loading from URL: {type(e).__name__}: {str(e)[:200]}")
        print("⚠ Falling back to sample data...")
        try:
            df = pd.read_csv('flight_data_2024_sample.csv')
            print(f"✓ Loaded sample data: {len(df):,} records")
        except Exception as e2:
            print(f"✗ CRITICAL ERROR: Cannot load any data: {e2}")
            raise
else:
    # Development: load from local file
    print("No CSV_URL found, loading local data...")
    try:
        # Try full dataset first
        df = pd.read_csv('flight_data_2024.csv', low_memory=False)
        print(f"✓ Loaded FULL dataset: {len(df):,} records")
    except FileNotFoundError:
        # Fall back to sample
        print("Full dataset not found, using sample...")
        df = pd.read_csv('flight_data_2024_sample.csv')
        print(f"✓ Loaded sample data: {len(df):,} records")

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

print(f"SUCCESS: Loaded {len(df):,} flight records")
print(f"Date range: {df['fl_date'].min()} to {df['fl_date'].max()}")

# ====================================
# 3D ANIMATED PLANE BACKGROUND CSS
# ====================================
plane_animation_css = """
@keyframes float-plane {
    0% { transform: translate(-100vw, 20vh) rotate(0deg); }
    25% { transform: translate(25vw, 10vh) rotate(5deg); }
    50% { transform: translate(50vw, 30vh) rotate(-5deg); }
    75% { transform: translate(75vw, 15vh) rotate(3deg); }
    100% { transform: translate(120vw, 25vh) rotate(0deg); }
}

@keyframes float-plane-2 {
    0% { transform: translate(120vw, 60vh) rotate(180deg); }
    25% { transform: translate(75vw, 70vh) rotate(175deg); }
    50% { transform: translate(50vw, 50vh) rotate(185deg); }
    75% { transform: translate(25vw, 65vh) rotate(178deg); }
    100% { transform: translate(-100vw, 60vh) rotate(180deg); }
}

@keyframes float-plane-3 {
    0% { transform: translate(50vw, -20vh) rotate(45deg) scale(0.7); }
    50% { transform: translate(60vw, 90vh) rotate(40deg) scale(0.7); }
    100% { transform: translate(70vw, 120vh) rotate(45deg) scale(0.7); }
}

.plane-bg {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 0;
    overflow: hidden;
    background: linear-gradient(180deg, #0a0e27 0%, #1a1f3a 50%, #0f1428 100%);
}

.plane {
    position: absolute;
    font-size: 40px;
    opacity: 0.15;
    filter: drop-shadow(0 0 10px #00d4ff);
}

.plane-1 {
    animation: float-plane 45s linear infinite;
    top: 0;
}

.plane-2 {
    animation: float-plane-2 55s linear infinite;
    top: 0;
    animation-delay: -20s;
}

.plane-3 {
    animation: float-plane-3 35s linear infinite;
    left: 0;
    animation-delay: -10s;
}

.plane-4 {
    animation: float-plane 60s linear infinite;
    top: 0;
    animation-delay: -30s;
    font-size: 35px;
}

.plane-5 {
    animation: float-plane-2 50s linear infinite;
    top: 0;
    animation-delay: -40s;
    font-size: 45px;
}

.content-wrapper {
    position: relative;
    z-index: 1;
}

.dashboard-title {
    text-align: center;
    color: #00d4ff;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 0 0 20px #00d4ff, 0 0 40px #00d4ff;
    margin: 20px 0;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 30px #00d4ff; }
    to { text-shadow: 0 0 20px #00d4ff, 0 0 30px #00d4ff, 0 0 40px #00d4ff, 0 0 50px #00ff88; }
}

.filter-card {
    background: rgba(10, 20, 40, 0.9) !important;
    border: 1px solid #00d4ff;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    padding: 15px;
    margin: 10px 0;
}

.viz-card {
    background: rgba(10, 20, 40, 0.85) !important;
    border: 1px solid #00d4ff;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    padding: 20px;
    margin: 15px 0;
    transition: transform 0.3s, box-shadow 0.3s;
}

.viz-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 30px rgba(0, 255, 136, 0.4);
}

.kpi-card {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 136, 0.1));
    border: 2px solid #00d4ff;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.4);
}

.kpi-value {
    font-size: 2.5em;
    font-weight: bold;
    color: #00ff88;
    text-shadow: 0 0 10px #00ff88;
}

.kpi-label {
    font-size: 1em;
    color: #00d4ff;
    margin-top: 10px;
}
"""

# ====================================
# INITIALIZE DASH APP
# ====================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Flight Delay Dashboard 2024"
server = app.server  # Expose server for deployment (Render, Heroku, etc.)

# Inject custom CSS into the app
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
        ''' + plane_animation_css + '''
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Color scheme for a professional look
colors = {
    'background': '#0a0e27',
    'text': '#00d4ff',
    'card_bg': 'rgba(10, 20, 40, 0.8)',
    'accent': '#00ff88'
}

# ====================================
# CREATE VISUALIZATION FUNCTIONS
# ====================================

def create_monthly_trend(filtered_df, chart_type='both'):
    """Viz 1: Monthly Delay Trends"""
    monthly = filtered_df.groupby('month_name').agg({
        'dep_delay': 'mean',
        'arr_delay': 'mean',
        'op_carrier_fl_num': 'count'
    }).reset_index()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly['month_name'] = pd.Categorical(monthly['month_name'], categories=month_order, ordered=True)
    monthly = monthly.sort_values('month_name')
    
    fig = go.Figure()
    
    if chart_type in ['both', 'dep']:
        fig.add_trace(go.Scatter(x=monthly['month_name'], y=monthly['dep_delay'],
                                 name='Departure Delay', mode='lines+markers',
                                 line=dict(color='#ff6b6b', width=3),
                                 marker=dict(size=10)))
    if chart_type in ['both', 'arr']:
        fig.add_trace(go.Scatter(x=monthly['month_name'], y=monthly['arr_delay'],
                                 name='Arrival Delay', mode='lines+markers',
                                 line=dict(color='#4ecdc4', width=3),
                                 marker=dict(size=10)))
    
    fig.update_layout(
        title='📈 Monthly Delay Trends',
        xaxis_title='Month',
        yaxis_title='Average Delay (minutes)',
        template='plotly_dark',
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_carrier_performance(filtered_df, min_flights=10):
    """Viz 2: Carrier Performance Comparison"""
    carrier_stats = filtered_df.groupby('op_unique_carrier').agg({
        'arr_delay': 'mean',
        'on_time': 'mean',
        'cancelled': 'mean',
        'op_carrier_fl_num': 'count'
    }).reset_index()
    carrier_stats.columns = ['Carrier', 'Avg Delay', 'On-Time Rate', 'Cancel Rate', 'Flights']
    carrier_stats = carrier_stats[carrier_stats['Flights'] >= min_flights]
    carrier_stats['On-Time Rate'] = carrier_stats['On-Time Rate'] * 100
    carrier_stats['Cancel Rate'] = carrier_stats['Cancel Rate'] * 100
    carrier_stats = carrier_stats.sort_values('Avg Delay')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=carrier_stats['Carrier'],
        y=carrier_stats['Avg Delay'],
        marker=dict(color=carrier_stats['Avg Delay'],
                   colorscale='RdYlGn_r',
                   showscale=True),
        text=carrier_stats['Avg Delay'].round(1),
        textposition='outside',
        name='Avg Delay'
    ))
    
    fig.update_layout(
        title='🏆 Carrier Performance - Average Delays',
        xaxis_title='Carrier',
        yaxis_title='Average Delay (minutes)',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_delay_distribution(filtered_df):
    """Viz 3: Delay Category Distribution"""
    delay_counts = filtered_df['delay_category'].value_counts()
    
    colors_pie = ['#00ff88', '#4ecdc4', '#45b7d1', '#ffd93d', '#ff6b6b', '#8b5cf6']
    
    fig = go.Figure(data=[go.Pie(
        labels=delay_counts.index,
        values=delay_counts.values,
        hole=0.4,
        marker=dict(colors=colors_pie, line=dict(color='#000000', width=2)),
        textinfo='label+percent',
        textfont=dict(size=14)
    )])
    
    fig.update_layout(
        title='Delay Category Distribution',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff'),
        showlegend=True
    )
    return fig

def create_delay_attribution(filtered_df):
    """Viz 4: Delay Attribution Breakdown"""
    delay_types = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']
    delay_sums = filtered_df[delay_types].sum()
    
    fig = go.Figure(data=[go.Bar(
        x=['Carrier', 'Weather', 'NAS', 'Security', 'Late Aircraft'],
        y=delay_sums.values,
        marker=dict(color=['#ff6b6b', '#4ecdc4', '#ffd93d', '#8b5cf6', '#ff8c42'],
                   line=dict(color='#000000', width=2)),
        text=delay_sums.values,
        textposition='outside'
    )])
    
    fig.update_layout(
        title='🔍 Delay Root Cause Analysis',
        xaxis_title='Delay Type',
        yaxis_title='Total Delay Minutes',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_heatmap_delays(filtered_df, hour_range=[0, 23]):
    """Viz 5: Day of Week vs Hour Heatmap"""
    # Extract hour from departure time
    filtered_df['dep_hour'] = (filtered_df['dep_time'] // 100).fillna(0).astype(int)
    
    # Filter by hour range
    filtered_df = filtered_df[(filtered_df['dep_hour'] >= hour_range[0]) & 
                               (filtered_df['dep_hour'] <= hour_range[1])]
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    heatmap_data = filtered_df.groupby(['day_name', 'dep_hour'])['arr_delay'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='day_name', columns='dep_hour', values='arr_delay')
    heatmap_pivot = heatmap_pivot.reindex(day_order)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        colorscale='RdYlGn_r',
        colorbar=dict(title='Avg Delay (min)'),
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='📅 Delay Heatmap: Day of Week vs Hour',
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_distance_delay_scatter(filtered_df, sample_size=1000):
    """Viz 6: Distance vs Delay Analysis"""
    sample_data = filtered_df.dropna(subset=['distance', 'arr_delay']).sample(min(sample_size, len(filtered_df)))
    
    fig = px.scatter(
        sample_data,
        x='distance',
        y='arr_delay',
        color='op_unique_carrier',
        size='total_delay_minutes',
        hover_data=['origin', 'dest'],
        title='🛫 Flight Distance vs Arrival Delay',
        template='plotly_dark'
    )
    
    fig.update_layout(
        xaxis_title='Distance (miles)',
        yaxis_title='Arrival Delay (minutes)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_top_routes(filtered_df, top_n=15):
    """Viz 7: Top N Worst Routes"""
    routes = filtered_df.groupby(['origin', 'dest']).agg({
        'arr_delay': 'mean',
        'op_carrier_fl_num': 'count'
    }).reset_index()
    routes = routes[routes['op_carrier_fl_num'] >= 5]
    routes['route'] = routes['origin'] + ' → ' + routes['dest']
    routes = routes.nlargest(top_n, 'arr_delay')
    
    fig = go.Figure(go.Bar(
        x=routes['arr_delay'],
        y=routes['route'],
        orientation='h',
        marker=dict(color=routes['arr_delay'],
                   colorscale='Reds',
                   showscale=True),
        text=routes['arr_delay'].round(1),
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f'🚨 Top {top_n} Most Delayed Routes',
        xaxis_title='Average Delay (minutes)',
        yaxis_title='Route',
        template='plotly_dark',
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_cancellation_analysis(filtered_df):
    """Viz 8: Cancellation Analysis"""
    cancel_by_carrier = filtered_df.groupby('op_unique_carrier').agg({
        'cancelled': 'sum',
        'op_carrier_fl_num': 'count'
    }).reset_index()
    cancel_by_carrier['cancel_rate'] = (cancel_by_carrier['cancelled'] / 
                                         cancel_by_carrier['op_carrier_fl_num'] * 100)
    cancel_by_carrier = cancel_by_carrier[cancel_by_carrier['op_carrier_fl_num'] >= 10]
    cancel_by_carrier = cancel_by_carrier.sort_values('cancel_rate', ascending=False).head(10)
    
    fig = go.Figure(go.Bar(
        x=cancel_by_carrier['op_unique_carrier'],
        y=cancel_by_carrier['cancel_rate'],
        marker=dict(color='#ff6b6b', line=dict(color='#000000', width=2)),
        text=cancel_by_carrier['cancel_rate'].round(2),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='❌ Cancellation Rates by Carrier',
        xaxis_title='Carrier',
        yaxis_title='Cancellation Rate (%)',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_on_time_performance(filtered_df):
    """Viz 9: On-Time Performance Timeline"""
    daily_otp = filtered_df.groupby('fl_date').agg({
        'on_time': 'mean',
        'op_carrier_fl_num': 'count'
    }).reset_index()
    daily_otp['on_time_pct'] = daily_otp['on_time'] * 100
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_otp['fl_date'],
        y=daily_otp['on_time_pct'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#00ff88', width=2),
        fillcolor='rgba(0, 255, 136, 0.2)'
    ))
    
    fig.add_hline(y=80, line_dash="dash", line_color="red",
                  annotation_text="Target: 80%")
    
    fig.update_layout(
        title='⏱️ On-Time Performance Trend',
        xaxis_title='Date',
        yaxis_title='On-Time Performance (%)',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_box_plot_carriers(filtered_df):
    """Viz 10: Delay Distribution by Carrier (Box Plot)"""
    top_carriers = filtered_df['op_unique_carrier'].value_counts().head(10).index
    box_data = filtered_df[filtered_df['op_unique_carrier'].isin(top_carriers)]
    
    fig = go.Figure()
    for carrier in top_carriers:
        carrier_data = box_data[box_data['op_unique_carrier'] == carrier]['arr_delay'].dropna()
        fig.add_trace(go.Box(
            y=carrier_data,
            name=carrier,
            boxmean='sd'
        ))
    
    fig.update_layout(
        title='Delay Distribution by Top Carriers',
        yaxis_title='Arrival Delay (minutes)',
        xaxis_title='Carrier',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff'),
        showlegend=False
    )
    return fig

def create_state_performance(filtered_df):
    """Viz 11: State Performance Map"""
    state_stats = filtered_df.groupby('origin_state_nm').agg({
        'arr_delay': 'mean',
        'op_carrier_fl_num': 'count'
    }).reset_index()
    state_stats = state_stats[state_stats['op_carrier_fl_num'] >= 10]
    
    fig = px.bar(
        state_stats.nlargest(15, 'arr_delay'),
        x='origin_state_nm',
        y='arr_delay',
        color='arr_delay',
        color_continuous_scale='RdYlGn_r',
        title='🗺️ Average Delays by Departure State (Top 15)'
    )
    
    fig.update_layout(
        xaxis_title='State',
        yaxis_title='Average Delay (minutes)',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

def create_taxi_time_analysis(filtered_df):
    """Viz 12: Taxi Time Analysis"""
    taxi_data = filtered_df.groupby('origin').agg({
        'taxi_out': 'mean',
        'taxi_in': 'mean',
        'op_carrier_fl_num': 'count'
    }).reset_index()
    taxi_data = taxi_data[taxi_data['op_carrier_fl_num'] >= 20].nlargest(15, 'taxi_out')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=taxi_data['origin'],
        y=taxi_data['taxi_out'],
        name='Taxi Out',
        marker_color='#ff6b6b'
    ))
    fig.add_trace(go.Bar(
        x=taxi_data['origin'],
        y=taxi_data['taxi_in'],
        name='Taxi In',
        marker_color='#4ecdc4'
    ))
    
    fig.update_layout(
        title='🛬 Average Taxi Times by Airport',
        xaxis_title='Airport',
        yaxis_title='Average Time (minutes)',
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00d4ff')
    )
    return fig

# ====================================
# APP LAYOUT
# ====================================

app.layout = html.Div([
    # 3D Animated Plane Background
    html.Div(className='plane-bg', children=[
        html.Div('✈️', className='plane plane-1'),
        html.Div('✈️', className='plane plane-2'),
        html.Div('✈️', className='plane plane-3'),
        html.Div('🛫', className='plane plane-4'),
        html.Div('🛬', className='plane plane-5'),
    ]),
    
    # Main Content
    html.Div(className='content-wrapper', children=[
        dbc.Container([
            # Header
            html.Div([
                html.H1('✈️ FLIGHT DELAY ANALYTICS DASHBOARD 2024 ✈️', 
                       className='dashboard-title'),
                html.P('Interactive Visualization Platform with Real-Time Filtering',
                      style={'textAlign': 'center', 'color': '#00ff88', 'fontSize': '1.3em'})
            ]),
            
            html.Hr(style={'borderColor': '#00d4ff', 'borderWidth': '2px'}),
            
            # Dataset Overview Section
            dbc.Row([
                dbc.Col([
                    html.Div(className='filter-card', children=[
                        html.H4('About This Dataset', style={'color': '#00ff88', 'textAlign': 'center', 'marginBottom': '15px'}),
                        html.P([
                            html.Strong('Problem: '), 
                            'US flight delays cost billions annually, affecting millions of passengers. This dashboard analyzes 10,000+ flights from 2024 to identify delay patterns, root causes, and problematic routes—helping travelers plan better and airlines improve operations.'
                        ], style={'color': '#fff', 'fontSize': '1em', 'marginBottom': '15px'}),
                        html.Hr(style={'borderColor': '#00d4ff', 'margin': '15px 0'}),
                        html.H5('Key Terms Explained', style={'color': '#00d4ff', 'marginBottom': '10px'}),
                        html.Div([
                            html.P([html.Strong('Carrier: '), 'Airline code (e.g., AA=American, DL=Delta, UA=United, WN=Southwest)'], 
                                   style={'color': '#fff', 'fontSize': '0.9em', 'marginBottom': '8px'}),
                            html.P([html.Strong('NAS: '), 'National Airspace System delays (air traffic control, weather, airport operations)'], 
                                   style={'color': '#fff', 'fontSize': '0.9em', 'marginBottom': '8px'}),
                            html.P([html.Strong('On-Time: '), 'Flight arrives within ±15 minutes of scheduled time'], 
                                   style={'color': '#fff', 'fontSize': '0.9em', 'marginBottom': '8px'}),
                            html.P([html.Strong('Origin/Dest: '), 'Departure and arrival airports (3-letter codes like JFK, LAX, ORD)'], 
                                   style={'color': '#fff', 'fontSize': '0.9em', 'marginBottom': '8px'}),
                            html.P([html.Strong('Taxi Time: '), 'Time aircraft spends moving on ground before takeoff/after landing'], 
                                   style={'color': '#fff', 'fontSize': '0.9em', 'marginBottom': '0px'}),
                        ])
                    ])
                ], width=12)
            ], style={'marginTop': '20px', 'marginBottom': '20px'}),
            
            html.Hr(style={'borderColor': '#00d4ff', 'borderWidth': '2px'}),
            
            # KPI Cards Row
            dbc.Row([
                dbc.Col([
                    html.Div(className='kpi-card', children=[
                        html.Div(id='kpi-total-flights', className='kpi-value'),
                        html.Div('Total Flights', className='kpi-label')
                    ])
                ], width=3),
                dbc.Col([
                    html.Div(className='kpi-card', children=[
                        html.Div(id='kpi-avg-delay', className='kpi-value'),
                        html.Div('Avg Delay (min)', className='kpi-label')
                    ])
                ], width=3),
                dbc.Col([
                    html.Div(className='kpi-card', children=[
                        html.Div(id='kpi-ontime-rate', className='kpi-value'),
                        html.Div('On-Time Rate', className='kpi-label')
                    ])
                ], width=3),
                dbc.Col([
                    html.Div(className='kpi-card', children=[
                        html.Div(id='kpi-cancel-rate', className='kpi-value'),
                        html.Div('Cancellation Rate', className='kpi-label')
                    ])
                ], width=3),
            ], style={'marginTop': '20px', 'marginBottom': '30px'}),
            
            # Global Filters
            html.Div(className='filter-card', children=[
                html.H3('🎛️ GLOBAL FILTERS', style={'color': '#00ff88', 'textAlign': 'center'}),
                dbc.Row([
                    dbc.Col([
                        html.Label('Select Carrier:', style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='carrier-filter',
                            options=[{'label': 'All Carriers', 'value': 'ALL'}] + 
                                   [{'label': c, 'value': c} for c in sorted(df['op_unique_carrier'].unique())],
                            value='ALL',
                            style={'backgroundColor': '#1a1f3a', 'color': '#000'}
                        )
                    ], width=4),
                    dbc.Col([
                        html.Label('Select Month:', style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='month-filter',
                            options=[{'label': 'All Months', 'value': 'ALL'}] + 
                                   [{'label': m, 'value': m} for m in df['month_name'].unique()],
                            value='ALL',
                            style={'backgroundColor': '#1a1f3a', 'color': '#000'}
                        )
                    ], width=4),
                    dbc.Col([
                        html.Label('Select Day of Week:', style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                        dcc.Dropdown(
                            id='day-filter',
                            options=[{'label': 'All Days', 'value': 'ALL'}] + 
                                   [{'label': d, 'value': d} for d in df['day_name'].unique()],
                            value='ALL',
                            style={'backgroundColor': '#1a1f3a', 'color': '#000'}
                        )
                    ], width=4),
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Label('Delay Range (minutes):', style={'color': '#00d4ff', 'fontWeight': 'bold'}),
                        dcc.RangeSlider(
                            id='delay-slider',
                            min=-50,
                            max=300,
                            step=10,
                            value=[-50, 300],
                            marks={i: str(i) for i in range(-50, 301, 50)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], width=12)
                ], style={'marginTop': '20px'})
            ]),
            
            html.Hr(style={'borderColor': '#00d4ff', 'borderWidth': '2px', 'margin': '30px 0'}),
            
            # Visualizations Grid
            dbc.Row([
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        html.Div([
                            html.Label('Chart Type:', style={'color': '#00d4ff', 'fontWeight': 'bold', 'marginRight': '10px'}),
                            dcc.RadioItems(
                                id='viz1-filter',
                                options=[
                                    {'label': ' Departure & Arrival', 'value': 'both'},
                                    {'label': ' Departure Only', 'value': 'dep'},
                                    {'label': ' Arrival Only', 'value': 'arr'}
                                ],
                                value='both',
                                inline=True,
                                style={'color': '#fff'},
                                labelStyle={'marginRight': '15px'}
                            )
                        ], style={'marginBottom': '15px'}),
                        dcc.Graph(id='viz-1-monthly-trend')
                    ])
                ], width=6),
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        html.Div([
                            html.Label('Min Flight Count:', style={'color': '#00d4ff', 'fontWeight': 'bold', 'marginRight': '10px'}),
                            dcc.Dropdown(
                                id='viz2-filter',
                                options=[
                                    {'label': 'All Carriers', 'value': 0},
                                    {'label': '10+ Flights', 'value': 10},
                                    {'label': '50+ Flights', 'value': 50},
                                    {'label': '100+ Flights', 'value': 100}
                                ],
                                value=10,
                                style={'width': '200px', 'backgroundColor': '#1a1f3a', 'color': '#000'}
                            )
                        ], style={'marginBottom': '15px'}),
                        dcc.Graph(id='viz-2-carrier-performance')
                    ])
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        dcc.Graph(id='viz-3-delay-distribution')
                    ])
                ], width=6),
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        dcc.Graph(id='viz-4-delay-attribution')
                    ])
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        html.Div([
                            html.Label('Show Hour Range:', style={'color': '#00d4ff', 'fontWeight': 'bold', 'marginRight': '10px'}),
                            dcc.RangeSlider(
                                id='viz5-filter',
                                min=0,
                                max=23,
                                step=1,
                                value=[0, 23],
                                marks={i: f'{i}:00' for i in range(0, 24, 4)},
                                tooltip={"placement": "bottom", "always_visible": False}
                            )
                        ], style={'marginBottom': '25px'}),
                        dcc.Graph(id='viz-5-heatmap')
                    ])
                ], width=12),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        html.Div([
                            html.Label('Sample Size:', style={'color': '#00d4ff', 'fontWeight': 'bold', 'marginRight': '10px'}),
                            dcc.Dropdown(
                                id='viz6-filter',
                                options=[
                                    {'label': '500 points', 'value': 500},
                                    {'label': '1000 points', 'value': 1000},
                                    {'label': '2000 points', 'value': 2000},
                                    {'label': 'All data', 'value': 10000}
                                ],
                                value=1000,
                                style={'width': '200px', 'backgroundColor': '#1a1f3a', 'color': '#000'}
                            )
                        ], style={'marginBottom': '15px'}),
                        dcc.Graph(id='viz-6-distance-scatter')
                    ])
                ], width=6),
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        html.Div([
                            html.Label('Show Top:', style={'color': '#00d4ff', 'fontWeight': 'bold', 'marginRight': '10px'}),
                            dcc.Dropdown(
                                id='viz7-filter',
                                options=[
                                    {'label': 'Top 10 Routes', 'value': 10},
                                    {'label': 'Top 15 Routes', 'value': 15},
                                    {'label': 'Top 20 Routes', 'value': 20},
                                    {'label': 'Top 25 Routes', 'value': 25}
                                ],
                                value=15,
                                style={'width': '200px', 'backgroundColor': '#1a1f3a', 'color': '#000'}
                            )
                        ], style={'marginBottom': '15px'}),
                        dcc.Graph(id='viz-7-top-routes')
                    ])
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        dcc.Graph(id='viz-8-cancellation')
                    ])
                ], width=6),
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        dcc.Graph(id='viz-9-ontime-performance')
                    ])
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        dcc.Graph(id='viz-10-box-plot')
                    ])
                ], width=6),
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        dcc.Graph(id='viz-11-state-performance')
                    ])
                ], width=6),
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div(className='viz-card', children=[
                        dcc.Graph(id='viz-12-taxi-analysis')
                    ])
                ], width=12),
            ]),
            
            # Footer
            html.Hr(style={'borderColor': '#00d4ff', 'borderWidth': '2px', 'margin': '50px 0 20px 0'}),
    html.Div([
                html.P('✈️ Flight Delay Analytics Dashboard 2024 | Data-Driven Insights for Aviation Excellence',
                      style={'textAlign': 'center', 'color': '#00d4ff', 'fontSize': '1.1em'}),
                html.P('Featuring 12 Interactive Visualizations with Real-Time Filtering & 3D Animated Background',
                      style={'textAlign': 'center', 'color': '#00ff88', 'marginBottom': '30px'})
            ])
            
        ], fluid=True)
    ])
], style={'backgroundColor': colors['background'], 'minHeight': '100vh'})

# ====================================
# CALLBACKS
# ====================================

@app.callback(
    [Output('kpi-total-flights', 'children'),
     Output('kpi-avg-delay', 'children'),
     Output('kpi-ontime-rate', 'children'),
     Output('kpi-cancel-rate', 'children'),
     Output('viz-1-monthly-trend', 'figure'),
     Output('viz-2-carrier-performance', 'figure'),
     Output('viz-3-delay-distribution', 'figure'),
     Output('viz-4-delay-attribution', 'figure'),
     Output('viz-5-heatmap', 'figure'),
     Output('viz-6-distance-scatter', 'figure'),
     Output('viz-7-top-routes', 'figure'),
     Output('viz-8-cancellation', 'figure'),
     Output('viz-9-ontime-performance', 'figure'),
     Output('viz-10-box-plot', 'figure'),
     Output('viz-11-state-performance', 'figure'),
     Output('viz-12-taxi-analysis', 'figure')],
    [Input('carrier-filter', 'value'),
     Input('month-filter', 'value'),
     Input('day-filter', 'value'),
     Input('delay-slider', 'value'),
     Input('viz1-filter', 'value'),
     Input('viz2-filter', 'value'),
     Input('viz5-filter', 'value'),
     Input('viz6-filter', 'value'),
     Input('viz7-filter', 'value')]
)
def update_dashboard(carrier, month, day, delay_range, viz1_type, viz2_min, viz5_hours, viz6_sample, viz7_top):
    """Update all visualizations based on filters"""
    # Filter data
    filtered_df = df.copy()
    
    if carrier != 'ALL':
        filtered_df = filtered_df[filtered_df['op_unique_carrier'] == carrier]
    
    if month != 'ALL':
        filtered_df = filtered_df[filtered_df['month_name'] == month]
    
    if day != 'ALL':
        filtered_df = filtered_df[filtered_df['day_name'] == day]
    
    filtered_df = filtered_df[
        (filtered_df['arr_delay'].fillna(0) >= delay_range[0]) &
        (filtered_df['arr_delay'].fillna(0) <= delay_range[1])
    ]
    
    # Calculate KPIs
    total_flights = f"{len(filtered_df):,}"
    avg_delay = f"{filtered_df['arr_delay'].mean():.1f}"
    ontime_rate = f"{filtered_df['on_time'].mean() * 100:.1f}%"
    cancel_rate = f"{filtered_df['cancelled'].mean() * 100:.2f}%"
    
    # Generate all visualizations with individual filters
    return (
        total_flights,
        avg_delay,
        ontime_rate,
        cancel_rate,
        create_monthly_trend(filtered_df, viz1_type),
        create_carrier_performance(filtered_df, viz2_min),
        create_delay_distribution(filtered_df),
        create_delay_attribution(filtered_df),
        create_heatmap_delays(filtered_df, viz5_hours),
        create_distance_delay_scatter(filtered_df, viz6_sample),
        create_top_routes(filtered_df, viz7_top),
        create_cancellation_analysis(filtered_df),
        create_on_time_performance(filtered_df),
        create_box_plot_carriers(filtered_df),
        create_state_performance(filtered_df),
        create_taxi_time_analysis(filtered_df)
    )

# ====================================
# RUN APP
# ====================================

if __name__ == '__main__':
    print("=" * 80)
    print("FLIGHT DELAY ANALYTICS DASHBOARD 2024")
    print("=" * 80)
    print("Starting dashboard server...")
    print("Features: 12 Interactive Visualizations + 3D Animated Background")
    print("Global Filters: Carrier, Month, Day, Delay Range")
    print(f"Data loaded: {len(df):,} records")
    print("=" * 80)
    # Use environment variable for port (Render provides this)
    port = int(os.getenv("PORT", 10000))
    print(f"Server starting on port {port}...")
    app.run_server(debug=False, host='0.0.0.0', port=port)

