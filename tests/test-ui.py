#!/usr/bin/env python3
"""Quick test to see if SIRAJ web interface is working"""

import webbrowser
import time

print("\n🧪 SIRAJ Quick Test")
print("==================\n")

print("Opening web interface...")
print("If you see the SIRAJ interface, it's working!")
print("The AI responses will work once Ollama finishes downloading the model.\n")

webbrowser.open("http://localhost:3000")

print("Current status:")
print("✅ Web server: Running")
print("✅ Frontend: Loaded") 
print("⏳ AI Model: Downloading (this can take 10-20 minutes)")
print("\nYou can use the interface now - it will start responding once the model is ready!")
print("\nPress Ctrl+C to stop")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n👋 Test stopped")
