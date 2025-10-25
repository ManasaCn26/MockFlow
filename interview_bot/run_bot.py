import webbrowser
import time
import os

print("🚀 LAUNCHING INTERVIEW BOT...")
print("⏳ Please wait...")

# Open browser first
time.sleep(2)
webbrowser.open('http://localhost:5000')

# Then start the server
os.system('python app.py')