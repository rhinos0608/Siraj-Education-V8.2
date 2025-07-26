#!/usr/bin/env python3
"""
Quick diagnostic script to check system status
"""

import subprocess
import sys
import socket
from pathlib import Path

print("🔍 SIRAJ System Diagnostic")
print("="*50)

# Check Python
print(f"✅ Python: {sys.version}")

# Check if ports are in use
def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

print(f"\n📡 Port Status:")
print(f"   Port 3000 (Frontend): {'✅ In use' if check_port(3000) else '❌ Free'}")
print(f"   Port 8000 (Backend): {'✅ In use' if check_port(8000) else '❌ Free'}")

# Check if backend can be imported
print(f"\n🔧 Backend Check:")
backend_path = Path(__file__).parent / "backend" / "main.py"
if backend_path.exists():
    print(f"   ✅ Backend main.py exists")
    # Try to start backend directly
    print(f"   🚀 Attempting to start backend...")
    try:
        # Start backend in background
        backend_process = subprocess.Popen(
            [sys.executable, str(backend_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"   ✅ Backend process started (PID: {backend_process.pid})")
        print(f"   ⏳ Wait a few seconds for it to initialize...")
    except Exception as e:
        print(f"   ❌ Failed to start backend: {e}")
else:
    print(f"   ❌ Backend main.py not found!")

print("\n💡 Recommendations:")
if not check_port(8000):
    print("   1. Backend is not running on port 8000")
    print("   2. Try running backend manually:")
    print("      cd backend && python main.py")
    print("   3. Or restart the launcher")

print("\n✅ Diagnostic complete")
