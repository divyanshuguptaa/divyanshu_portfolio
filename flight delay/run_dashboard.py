"""Quick launcher for the dashboard"""
import subprocess
import sys
import time
import webbrowser
from threading import Timer

def open_browser():
    """Open browser after a delay"""
    print("\n🌐 Opening browser...")
    webbrowser.open('http://127.0.0.1:8001')

if __name__ == '__main__':
    print("=" * 80)
    print("✈️  LAUNCHING FLIGHT DELAY DASHBOARD 2024")
    print("=" * 80)
    print("📦 Loading data...")
    print("🎨 Initializing visualizations...")
    print("🛫 Starting 3D plane animations...")
    print("=" * 80)
    
    # Open browser after 8 seconds
    timer = Timer(8.0, open_browser)
    timer.start()
    
    # Run the dashboard
    try:
        subprocess.run([sys.executable, 'flight_delay_dashboard.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("✋ Dashboard stopped by user")
        print("=" * 80)

