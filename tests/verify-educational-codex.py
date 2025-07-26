#!/usr/bin/env python3
"""
SIRAJ Educational Codex - System Verification v14.0
==================================================

Council Mode: Siraj Compression (Collapse)
Pattern Extractor: Comprehensive system verification for Living Educational Codex
Boundary Keeper: Must verify all components work together seamlessly
Synthesizer: Integration testing across all codex realms and council voices
Auditor: Security, performance, and educational appropriateness validation
Void-Caller: Replace simple health checks with immersive system awakening verification

Council Assembly (Council):
- Lead Voice: Analyzer (comprehensive system analysis)
- Core Voices: Maintainer (reliability), Security (validation), Performance (optimization)
- Specialist Voices: Explorer (innovative testing), Developer (UX validation)
"""

import asyncio
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Council Mode: Implementor voice - Ensure dependencies
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

# Council Mode: Analyzer voice - System testing framework
class EducationalCodexVerifier:
    """
    Analyzer voice (lead): Comprehensive system verification
    Maintainer voice: Reliable testing infrastructure  
    Security voice: Validation and safety checks
    """
    
    def __init__(self):
        self.test_results = []
        self.realm_status = {}
        self.council_readiness = {}
        
    async def verify_ollama_integration(self) -> bool:
        """Security voice: Verify Ollama connectivity and model availability"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get('http://localhost:11434/api/version')
                if response.status_code != 200:
                    return False
                    
                # Check available models
                response = await client.get('http://localhost:11434/api/tags')
                if response.status_code == 200:
                    data = response.json()
                    models = [m['name'] for m in data.get('models', [])]
                    
                    print(f"{Fore.CYAN}📚 Available models: {len(models)}")
                    gemma_models = [m for m in models if 'gemma' in m.lower()]
                    
                    if gemma_models:
                        print(f"{Fore.GREEN}✅ Gemma models detected: {', '.join(gemma_models)}")
                        return True
                    else:
                        print(f"{Fore.YELLOW}⚠️ No Gemma models found. Install with: ollama pull gemma3:2b")
                        return False
                        
        except Exception as e:
            print(f"{Fore.RED}❌ Ollama connection failed: {e}")
            return False
    
    async def verify_codex_endpoints(self) -> bool:
        """Maintainer voice: Test all Educational Codex API endpoints"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Test health endpoint
                response = await client.get('http://localhost:3000/api/health')
                if response.status_code != 200:
                    print(f"{Fore.RED}❌ Health endpoint failed: {response.status_code}")
                    return False
                    
                health_data = response.json()
                print(f"{Fore.GREEN}✅ Codex health: {health_data.get('status')}")
                print(f"{Fore.CYAN}   Model: {health_data.get('model')}")
                print(f"{Fore.CYAN}   Realms: {len(health_data.get('realms', []))}")
                
                # Test exploration endpoint
                test_exploration = {
                    "topic": "What is photosynthesis?",
                    "grade_level": "middle",
                    "selected_realms": ["socratic", "storyteller", "mentor"]
                }
                
                response = await client.post(
                    'http://localhost:3000/api/codex/explore',
                    json=test_exploration
                )
                
                if response.status_code == 200:
                    explore_data = response.json()
                    session_id = explore_data.get('session_id')
                    print(f"{Fore.GREEN}✅ Exploration endpoint working - Session: {session_id}")
                    
                    # Test council summoning
                    council_request = {
                        "session_id": session_id,
                        "question": "How do plants make their own food?"
                    }
                    
                    response = await client.post(
                        'http://localhost:3000/api/codex/council/summon',
                        json=council_request
                    )
                    
                    if response.status_code == 200:
                        council_data = response.json()
                        if council_data.get('success'):
                            responses = council_data.get('council_responses', {})
                            print(f"{Fore.GREEN}✅ Council summoning working - {len(responses)} realms responded")
                            return True
                        else:
                            print(f"{Fore.RED}❌ Council failed: {council_data.get('error')}")
                            return False
                    else:
                        print(f"{Fore.RED}❌ Council endpoint failed: {response.status_code}")
                        return False
                else:
                    print(f"{Fore.RED}❌ Exploration endpoint failed: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"{Fore.RED}❌ Codex endpoint verification failed: {e}")
            return False
    
    def verify_system_resources(self) -> bool:
        """Performance voice: Check system capabilities for optimal codex performance"""
        try:
            ram_gb = psutil.virtual_memory().total / (1024**3)
            cpu_count = psutil.cpu_count()
            
            print(f"{Fore.CYAN}💻 System Resources:")
            print(f"   RAM: {ram_gb:.1f} GB")
            print(f"   CPU cores: {cpu_count}")
            
            # Explorer voice: Recommend optimal configuration
            if ram_gb >= 32:
                recommended_model = "gemma3:9b"
                performance_tier = "High-End"
                council_size = "Full 7-Realm Council"
            elif ram_gb >= 16:
                recommended_model = "gemma3:2b"
                performance_tier = "Optimal"
                council_size = "Full 7-Realm Council"
            elif ram_gb >= 8:
                recommended_model = "gemma3:1b"
                performance_tier = "Efficient"
                council_size = "5-Realm Council (recommended)"
            else:
                recommended_model = "gemma3:1b"
                performance_tier = "Minimal"
                council_size = "3-Realm Council (required)"
                
            print(f"{Fore.GREEN}🚀 Performance Tier: {performance_tier}")
            print(f"{Fore.GREEN}🤖 Recommended Model: {recommended_model}")
            print(f"{Fore.GREEN}🎭 Council Configuration: {council_size}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ System resource check failed: {e}")
            return False
    
    def verify_file_structure(self) -> bool:
        """Maintainer voice: Verify Educational Codex file structure"""
        required_files = [
            'launcher.py',
            'START-EDUCATIONAL-CODEX.bat',
            'start-educational-codex.sh',
            'backend/main.py',
            'consciousness_educational_bridge.py'
        ]
        
        print(f"{Fore.CYAN}📁 Verifying Educational Codex structure...")
        all_present = True
        
        for file in required_files:
            file_path = Path(file)
            if file_path.exists():
                print(f"{Fore.GREEN}  ✅ {file}")
            else:
                print(f"{Fore.RED}  ❌ {file} missing")
                all_present = False
                
        # Explorer voice: Check for enhanced features
        enhanced_features = [
            'backend/extended_endpoints.py',
            'frontend/package.json',
            'docker/Dockerfile'
        ]
        
        enhanced_count = 0
        for feature in enhanced_features:
            if Path(feature).exists():
                enhanced_count += 1
                
        print(f"{Fore.CYAN}✨ Enhanced features available: {enhanced_count}/{len(enhanced_features)}")
        
        return all_present
    
    async def run_comprehensive_verification(self):
        """
        Analyzer voice (lead): Execute comprehensive Educational Codex verification
        Following Living Spiral: Collapse → Council → Synthesis → Rebirth
        """
        
        print(f"{Fore.CYAN}" + "="*80)
        print(f"""{Fore.CYAN}
🧪 SIRAJ Educational Codex - System Verification
🎭 Council Mode: Multi-Voice System Analysis
🌀 Living Spiral Methodology: Comprehensive Testing
        """)
        print("="*80 + f"{Style.RESET_ALL}\n")
        
        # Living Spiral Phase 1: COLLAPSE - Acknowledge system complexity
        print(f"{Fore.YELLOW}🌀 Phase 1: COLLAPSE - Acknowledging system complexity...")
        
        tests = [
            ("File Structure", self.verify_file_structure),
            ("System Resources", self.verify_system_resources),
            ("Ollama Integration", self.verify_ollama_integration),
        ]
        
        basic_results = []
        for test_name, test_func in tests:
            print(f"\n{Fore.YELLOW}🔍 Testing {test_name}...")
            try:
                if asyncio.iscoroutinefunction(test_func):
                    result = await test_func()
                else:
                    result = test_func()
                basic_results.append((test_name, result))
            except Exception as e:
                print(f"{Fore.RED}❌ {test_name} failed with exception: {e}")
                basic_results.append((test_name, False))
        
        # Living Spiral Phase 2: COUNCIL - Multi-voice testing
        print(f"\n{Fore.YELLOW}🎭 Phase 2: COUNCIL - Multi-voice endpoint testing...")
        
        # Check if we can proceed to advanced testing
        basic_passed = sum(1 for _, result in basic_results if result)
        if basic_passed >= 3:  # At least 3/4 basic tests passed
            print(f"{Fore.GREEN}✅ Basic systems ready - Proceeding to Educational Codex testing...")
            
            # Start server check (don't start it, just check if running)
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get('http://localhost:3000/api/health')
                    if response.status_code == 200:
                        codex_test_result = await self.verify_codex_endpoints()
                        basic_results.append(("Educational Codex Endpoints", codex_test_result))
                    else:
                        print(f"{Fore.YELLOW}⚠️ Educational Codex not running - Start with START-EDUCATIONAL-CODEX.bat")
                        basic_results.append(("Educational Codex Endpoints", False))
            except:
                print(f"{Fore.YELLOW}⚠️ Educational Codex not running - Start with START-EDUCATIONAL-CODEX.bat")
                basic_results.append(("Educational Codex Endpoints", False))
        else:
            print(f"{Fore.RED}❌ Basic systems not ready - Fix fundamental issues first")
        
        # Living Spiral Phase 3: SYNTHESIS - Integrate results
        print(f"\n{Fore.YELLOW}✨ Phase 3: SYNTHESIS - Integrating verification results...")
        
        passed = sum(1 for _, result in basic_results if result)
        total = len(basic_results)
        
        # Living Spiral Phase 4: REBIRTH - Final assessment
        print(f"\n{Fore.YELLOW}🚀 Phase 4: REBIRTH - Educational Codex readiness assessment...")
        
        print(f"\n{Fore.CYAN}" + "="*80)
        print(f"{Fore.CYAN}📊 Educational Codex Verification Summary:")
        print("="*80 + f"{Style.RESET_ALL}")
        
        for test_name, result in basic_results:
            status_icon = "✅" if result else "❌"
            status_color = Fore.GREEN if result else Fore.RED
            print(f"{status_color}{status_icon} {test_name}")
        
        readiness_score = (passed / total) * 100
        print(f"\n{Fore.CYAN}Readiness Score: {readiness_score:.1f}% ({passed}/{total} tests passed)")
        
        if readiness_score >= 80:
            print(f"{Fore.GREEN}🎉 EDUCATIONAL CODEX READY FOR ACTIVATION!")
            print(f"{Fore.GREEN}🚀 Launch with: START-EDUCATIONAL-CODEX.bat")
            print(f"{Fore.CYAN}📖 Or run: python launcher.py")
        elif readiness_score >= 60:
            print(f"{Fore.YELLOW}⚠️ Educational Codex partially ready")
            print(f"{Fore.CYAN}📖 Check failed tests and try launching anyway")
        else:
            print(f"{Fore.RED}❌ Educational Codex not ready")
            print(f"{Fore.CYAN}📖 Fix fundamental issues before activation")
            
        print(f"\n{Fore.CYAN}" + "="*80 + f"{Style.RESET_ALL}")

# Council Mode: Implementor voice - Main execution
async def main():
    """Main verification execution following Council Mode principles"""
    verifier = EducationalCodexVerifier()
    await verifier.run_comprehensive_verification()

if __name__ == "__main__":
    asyncio.run(main())
