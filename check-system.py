#!/usr/bin/env python3
"""
SIRAJ Educational AI - Quick System Check
========================================
🌀 Quick verification that system is ready for deployment
"""

import os
import sys
from pathlib import Path

def check_system():
    """Quick system readiness check"""
    print("\n🌀 SIRAJ Educational AI - System Check")
    print("="*50)
    
    issues = []
    warnings = []
    
    # Check Python
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check critical files
    critical_files = [
        'launcher.py',
        'backend/main.py',
        'frontend/package.json',
        'frontend/src/App.js',
        '.env'
    ]
    
    root = Path(__file__).parent
    for file in critical_files:
        if (root / file).exists():
            print(f"✅ {file} found")
        else:
            issues.append(f"❌ Missing: {file}")
    
    # Check if frontend is built
    if (root / 'frontend' / 'build' / 'index.html').exists():
        print("✅ Frontend build exists")
    else:
        warnings.append("⚠️ Frontend not built (run EMERGENCY-BUILD-FRONTEND.bat)")
    
    # Check deployment scripts
    deployment_scripts = [
        'START-SIRAJ.bat',
        'DEPLOY-ONE-CLICK.bat',
        'EMERGENCY-BUILD-FRONTEND.bat'
    ]
    
    for script in deployment_scripts:
        if (root / script).exists():
            print(f"✅ {script} ready")
        else:
            issues.append(f"❌ Missing: {script}")
    
    print("\n" + "="*50)
    
    if issues:
        print("❌ CRITICAL ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        print("\n❌ System NOT ready for deployment")
        return False
    elif warnings:
        print("⚠️ WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
        print("\n⚠️ System ready with warnings")
        return True
    else:
        print("✅ System READY for deployment!")
        print("🎯 Run START-SIRAJ.bat to launch")
        return True

if __name__ == '__main__':
    ready = check_system()
    sys.exit(0 if ready else 1)
