#!/usr/bin/env python3
"""
Minimal backend test - verify FastAPI can start
"""

try:
    from fastapi import FastAPI
    import uvicorn
    print("✅ FastAPI and uvicorn are installed")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Run: pip install fastapi uvicorn")
    exit(1)

# Create minimal app
app = FastAPI(title="SIRAJ Backend Test")

@app.get("/")
def root():
    return {"status": "Backend test successful", "message": "If you see this, FastAPI is working!"}

@app.get("/health")
def health():
    return {"status": "healthy", "test": True}

if __name__ == "__main__":
    print("🚀 Starting minimal backend test on http://localhost:8000")
    print("   Visit http://localhost:8000 in your browser")
    print("   Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000)
