#!/usr/bin/env python3
"""
SIRAJ Educational AI - Quick Test v13.0
======================================

Quick verification that everything is working correctly.
"""

import asyncio
import sys
import subprocess
from pathlib import Path

try:
    import httpx
    import psutil
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("📦 Installing test dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'httpx', 'psutil', 'colorama', '--quiet'])
    import httpx
    import psutil
    from colorama import init, Fore, Style
    init(autoreset=True)

async def test_ollama():
    """Test Ollama connectivity"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get('http://localhost:11434/api/version')
            if response.status_code == 200:
                print(f"{Fore.GREEN}✅ Ollama is running")
                return True
            else:
                print(f"{Fore.RED}❌ Ollama returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"{Fore.RED}❌ Ollama not accessible: {e}")
        return False

async def test_models():
    """Test available models"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get('http://localhost:11434/api/tags')
            if response.status_code == 200:
                data = response.json()
                models = [m['name'] for m in data.get('models', [])]
                
                print(f"{Fore.CYAN}📚 Available models: {len(models)}")
                for model in models:
                    if 'gemma' in model.lower():
                        print(f"{Fore.GREEN}  ✅ {model}")
                    else:
                        print(f"{Fore.YELLOW}  📦 {model}")
                        
                # Check for Gemma 3
                gemma3_models = [m for m in models if 'gemma3' in m.lower()]
                if gemma3_models:
                    print(f"{Fore.GREEN}✅ Gemma 3 models ready: {', '.join(gemma3_models)}")
                    return True
                else:
                    print(f"{Fore.YELLOW}⚠️ No Gemma 3 models found")
                    print(f"{Fore.CYAN}📖 Run: ollama pull gemma3:2b")
                    return False
            else:
                print(f"{Fore.RED}❌ Could not fetch models")
                return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error checking models: {e}")
        return False

def test_system_resources():
    """Test system capabilities"""
    try:
        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_count = psutil.cpu_count()
        
        print(f"{Fore.CYAN}💻 System specs:")
        print(f"  RAM: {ram_gb:.1f} GB")
        print(f"  CPU cores: {cpu_count}")
        
        # Recommend model
        if ram_gb >= 32:
            recommended = "gemma3:9b"
            print(f"{Fore.GREEN}  🚀 Recommended: {recommended} (high-end)")
        elif ram_gb >= 16:
            recommended = "gemma3:2b"
            print(f"{Fore.GREEN}  🚀 Recommended: {recommended} (mid-range)")
        else:
            recommended = "gemma3:1b"
            print(f"{Fore.GREEN}  🚀 Recommended: {recommended} (efficient)")
            
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Could not check system: {e}")
        return False

def test_file_structure():
    """Test file structure"""
    files_to_check = [
        'launcher.py',
        'launcher_fixed_browser.py', 
        'START-SIRAJ-FIXED.bat',
        'FIXED-READY-FOR-HACKATHON.md'
    ]
    
    print(f"{Fore.CYAN}📁 Checking file structure...")
    all_good = True
    
    for file in files_to_check:
        if Path(file).exists():
            print(f"{Fore.GREEN}  ✅ {file}")
        else:
            print(f"{Fore.RED}  ❌ {file} missing")
            all_good = False
            
    return all_good

async def main():
    """Run all tests"""
    print(f"{Fore.CYAN}" + "="*60)
    print(f"""{Fore.CYAN}
🧪 SIRAJ Educational AI - System Test
🎭 Verifying everything is ready for hackathon
    """)
    print("="*60 + f"{Style.RESET_ALL}\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("System Resources", test_system_resources),
        ("Ollama Service", test_ollama),
        ("Gemma Models", test_models),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"{Fore.YELLOW}🔍 Testing {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{Fore.RED}❌ {test_name} failed: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print(f"{Fore.CYAN}" + "="*60)
    print(f"{Fore.CYAN}📊 Test Summary:")
    print("="*60 + f"{Style.RESET_ALL}")
    
    passed = 0
    for test_name, result in results:
        if result:
            print(f"{Fore.GREEN}✅ {test_name}")
            passed += 1
        else:
            print(f"{Fore.RED}❌ {test_name}")
    
    print(f"\n{Fore.CYAN}Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print(f"{Fore.GREEN}🎉 ALL TESTS PASSED!")
        print(f"{Fore.GREEN}🚀 SIRAJ is ready for the hackathon!")
        print(f"{Fore.CYAN}📖 Run: START-SIRAJ-FIXED.bat")
    else:
        print(f"{Fore.YELLOW}⚠️ Some issues detected")
        print(f"{Fore.CYAN}📖 Check the failed tests above")
        
    print(f"\n{Fore.CYAN}" + "="*60 + f"{Style.RESET_ALL}")

if __name__ == '__main__':
    asyncio.run(main())
