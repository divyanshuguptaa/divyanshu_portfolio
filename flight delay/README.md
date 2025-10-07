# ✈️ FLIGHT DELAY VISUALIZATION DASHBOARD 2024

## 🚀 Overview
An **interactive, professional-grade dashboard** featuring **12 stunning visualizations** with real-time filtering capabilities and a mesmerizing **3D animated plane background**. Built with Python, Plotly, and Dash.

---

## ✨ Features

### 📊 **12 Interactive Visualizations**
1. **Monthly Delay Trends** - Line chart showing departure and arrival delays across months
2. **Carrier Performance Comparison** - Bar chart ranking airlines by average delays
3. **Delay Category Distribution** - Donut chart showing delay severity breakdown
4. **Delay Attribution Analysis** - Bar chart revealing root causes (carrier, weather, NAS, etc.)
5. **Day/Hour Heatmap** - 2D heatmap showing worst travel times
6. **Distance vs Delay Scatter** - Interactive scatter plot with carrier coloring
7. **Top 15 Worst Routes** - Horizontal bar chart of most delayed city pairs
8. **Cancellation Analysis** - Carrier cancellation rates comparison
9. **On-Time Performance Timeline** - Daily on-time percentage with target line
10. **Delay Distribution Box Plots** - Statistical distribution by carrier
11. **State Performance Map** - Geographic analysis of departure delays
12. **Taxi Time Analysis** - Ground operation efficiency by airport

### 🎛️ **Dynamic Filtering System**
- **Carrier Filter** - Select specific airlines or view all
- **Month Filter** - Focus on particular months or entire year
- **Day of Week Filter** - Analyze specific days or all days
- **Delay Range Slider** - Interactive range selection (-50 to 300 minutes)
- **Real-Time Updates** - All 12 visualizations update instantly

### 🎨 **Visual Excellence**
- **3D Animated Plane Background** - 5 planes flying in different trajectories
- **Cyberpunk Theme** - Neon blue and green color scheme
- **Glassmorphism Cards** - Semi-transparent cards with glow effects
- **Hover Animations** - Interactive card lifting on hover
- **Glowing Title** - Pulsating neon title effect
- **Professional KPI Cards** - 4 key metrics prominently displayed

### 📈 **Key Performance Indicators**
- Total Flights Count
- Average Delay (minutes)
- On-Time Performance Rate
- Cancellation Rate

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Install required packages
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the Dashboard
```bash
python flight_delay_dashboard.py
```

### Access the Dashboard
Open your browser and navigate to:
```
http://127.0.0.1:8050
```

The dashboard will automatically load with the sample dataset (10,000 flights).

---

## 📁 Files

- `flight_delay_dashboard.py` - Main application file
- `requirements.txt` - Python dependencies
- `flight_data_2024_sample.csv` - Sample dataset (10,000 records)
- `flight_data_2024.csv` - Full dataset (~6-7 million records)
- `flight_data_2024_data_dictionary.csv` - Data dictionary

---

## 🎯 Data Columns (35 Total)

### Flight Identification
- year, month, day_of_month, day_of_week, fl_date
- op_unique_carrier, op_carrier_fl_num

### Route Information
- origin, origin_city_name, origin_state_nm
- dest, dest_city_name, dest_state_nm
- distance

### Timing Metrics
- crs_dep_time, dep_time, dep_delay
- crs_arr_time, arr_time, arr_delay
- wheels_off, wheels_on
- taxi_out, taxi_in

### Flight Status
- cancelled, cancellation_code, diverted
- crs_elapsed_time, actual_elapsed_time, air_time

### Delay Attribution
- carrier_delay
- weather_delay
- nas_delay (National Air System)
- security_delay
- late_aircraft_delay

---

## 🎨 Technology Stack

- **Python 3.11** - Core programming language
- **Pandas 2.1.4** - Data manipulation and analysis
- **Plotly 5.18.0** - Interactive visualizations
- **Dash 2.14.2** - Web application framework
- **Dash Bootstrap Components 1.5.0** - UI components
- **NumPy 1.26.2** - Numerical computing
- **SciPy 1.11.4** - Scientific computing

---

## 💡 Tips for Best Experience

1. **Start with Global Filters** - Use the filter panel at the top to narrow down data
2. **Interactive Charts** - Hover over data points for detailed information
3. **Zoom & Pan** - Use Plotly's built-in controls to explore charts
4. **Full Dataset** - To use the full dataset, change line 30 to load `flight_data_2024.csv`
5. **Performance** - Sample dataset loads instantly; full dataset may take 30-60 seconds

---

## 🎬 3D Animation Details

The dashboard features **5 animated planes** flying across the screen:
- **Plane 1** - Left to right, 45-second loop
- **Plane 2** - Right to left, 55-second loop
- **Plane 3** - Diagonal descent, 35-second loop
- **Plane 4** - Delayed left to right, 60-second loop
- **Plane 5** - Delayed right to left, 50-second loop

Each plane has:
- Custom flight path with rotation
- Drop shadow effects
- Semi-transparency for background effect
- Smooth CSS animations

---

## 📊 Insights You Can Discover

1. **Seasonal Patterns** - Which months have the worst delays?
2. **Carrier Reliability** - Which airlines are most punctual?
3. **Root Causes** - Are delays due to weather, carriers, or air traffic?
4. **Route Performance** - Which city pairs are problematic?
5. **Time-of-Day Patterns** - When are delays most likely?
6. **Geographic Hotspots** - Which states/airports struggle most?
7. **Operational Efficiency** - How do taxi times vary by airport?

---

## 🎓 Learning Outcomes

This project demonstrates:
- Advanced data visualization with Plotly
- Interactive web dashboards with Dash
- Real-time filtering and callbacks
- CSS animations and modern web design
- Data analysis with Pandas
- Professional dashboard UI/UX design

---

## 🤝 Credits

**Data Source**: U.S. Department of Transportation - Bureau of Transportation Statistics
**Dashboard Design**: Custom cyberpunk/aviation theme
**Year**: 2024 Flight Data

---

## 📝 License

This project is for educational and analytical purposes.

---

## 🚀 Future Enhancements

Potential additions:
- Machine learning delay prediction
- Real-time data integration
- Export reports to PDF
- Additional geographic visualizations
- Weather data integration
- Airline cost analysis

---

## 📞 Support

For issues or questions:
1. Check that all dependencies are installed
2. Ensure CSV files are in the same directory
3. Verify Python version (3.8+)
4. Check console for error messages

---

**✈️ Happy Analyzing! May your flights be delay-free! ✈️**

