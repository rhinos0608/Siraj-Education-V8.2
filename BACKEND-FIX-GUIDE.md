# 🚨 BACKEND CONNECTION FIX

## Problem
The backend service isn't starting, causing 404 errors for all API endpoints.

## Solutions (Try in Order)

### 1. **Rebuild Frontend** (Fixes manifest.json error)
```bash
cd frontend
npm run build
cd ..
```

### 2. **Start Backend Manually** (Test if backend works)
```bash
# Option A: Use the new script
START-BACKEND-ONLY.bat

# Option B: Manual start
cd backend
python main.py
```

### 3. **Run Diagnostic**
```bash
python diagnose.py
```

### 4. **Complete Restart**
```bash
# After backend is confirmed working
python launcher.py
```

## What I Fixed

1. ✅ **Created missing manifest.json** - This was causing the syntax error
2. ✅ **Enhanced launcher backend startup** - Better error handling and dependency checking
3. ✅ **Added diagnostic tools** - To help troubleshoot issues

## Expected Behavior

When everything works correctly:
1. Backend starts on port 8000
2. Frontend serves on port 3000
3. API calls are proxied correctly
4. No 404 errors in console

## If Backend Still Won't Start

Check for missing dependencies:
```bash
pip install fastapi uvicorn structlog pydantic httpx python-dotenv
```

Or use minimal requirements:
```bash
cd backend
pip install -r requirements-minimal.txt
```

## Architecture Reminder

```
[Browser:3000] → [Launcher Proxy] → [Backend:8000]
       ↓                ↓                  ↓
   React UI      Serves & Routes      FastAPI
```

The launcher must successfully start BOTH:
- Frontend server (port 3000) ✅ 
- Backend server (port 8000) ❌ (Currently failing)

---
*Council Assembly Resolution: Backend startup enhancement complete*
