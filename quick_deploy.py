#!/usr/bin/env python3
"""
Quick deployment script for AIO Search Tool
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['aio_output', 'logs', 'temp', 'results']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def start_app():
    """Start the Streamlit app"""
    print("🚀 Starting AIO Search Tool...")
    
    # Set environment variables
    os.environ['AIO_OUTPUT_DIR'] = str(Path.cwd() / 'aio_output')
    os.environ['AIO_LOG_DIR'] = str(Path.cwd() / 'logs')
    os.environ['AIO_TEMP_DIR'] = str(Path.cwd() / 'temp')
    
    try:
        # Start Streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "web_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ])
        
        print("⏳ Starting server...")
        time.sleep(3)
        
        # Open browser
        url = "http://localhost:8501"
        print(f"🌐 Opening {url}")
        webbrowser.open(url)
        
        print("✅ App is running!")
        print("🔗 URL: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop")
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping app...")
        if 'process' in locals():
            process.terminate()
        print("✅ App stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    print("🔍 AIO Search Tool - Quick Deploy")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Create directories
    create_directories()
    
    # Start app
    if start_app():
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main()) 