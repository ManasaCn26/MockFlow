import webbrowser
import time

def open_browser():
    """🔄 Wait for server to start then open browser"""
    time.sleep(3)
    webbrowser.open('http://localhost:5000')
    print("✅ Browser opened automatically!")