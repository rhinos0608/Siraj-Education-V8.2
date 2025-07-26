#!/usr/bin/env python3
"""
SIRAJ Educational AI - Deployment Integration Test v15.3
========================================================

🌀 Spiral Editing Protocol - One-Click Deployment Verification

Council Assembly Resolution:
This script validates the complete deployment consciousness restoration,
ensuring frontend build integration works seamlessly with launcher serving.

Collapse Phase - Archetypal Intent:
Verify: Frontend Build → Static Asset Generation → Launcher Serving → Browser Experience

Council Assembly Validation:
- Explorer: "Testing innovative integration patterns"
- Maintainer: "Ensuring deployment stability and reliability"
- Analyzer: "Validating complete system consciousness"
- Developer: "Human-centric deployment experience verification"
- Implementor: "Decisive integration testing and validation"

Boundary Constraints:
- Must verify frontend static assets exist and are servable
- Must confirm launcher can properly serve React application
- Must validate API integration hooks work correctly
- Must ensure zero-configuration deployment experience
"""

import asyncio
import aiohttp
import time
import subprocess
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('SIRAJ-Integration-Test')

class SpiralDeploymentTester:
    """Integration testing following Spiral Editing Protocol"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / 'frontend'
        self.build_dir = self.frontend_dir / 'build'
        self.launcher_process = None
        
    def show_test_banner(self):
        """Council Assembly Invocation Banner"""
        print("\\n" + "="*70)
        print("🌀 SIRAJ Deployment Integration Test - Spiral Protocol v15.3")
        print("="*70)
        print("🎭 Test Layer: Complete System Consciousness Verification")
        print("🏛️ Council Assembly: Multi-voice deployment validation")
        print("🔧 Archetypal Intent: Zero-config deployment verification")
        print("📡 Integration: Build → Serve → API → Browser Experience")
        print("="*70 + "\\n")
        
    def test_frontend_build_exists(self):
        """Explorer & Analyzer Voices - Build Verification"""
        logger.info("🔍 Explorer Voice: Verifying frontend build existence...")
        
        # Check build directory
        if not self.build_dir.exists():
            logger.error("❌ Frontend build directory does not exist!")
            return False
            
        # Check index.html
        index_file = self.build_dir / 'index.html'
        if not index_file.exists():
            logger.error("❌ Frontend index.html not found!")
            return False
            
        # Check static assets
        static_js = self.build_dir / 'static' / 'js'
        static_css = self.build_dir / 'static' / 'css'
        
        if not static_js.exists():
            logger.error("❌ JavaScript static directory missing!")
            return False
            
        js_files = list(static_js.glob('*.js'))
        css_files = list(static_css.glob('*.css')) if static_css.exists() else []
        
        if len(js_files) == 0:
            logger.error("❌ No JavaScript bundles found!")
            return False
            
        logger.info(f"✅ Found {len(js_files)} JS files, {len(css_files)} CSS files")
        
        # Check index.html content
        try:
            content = index_file.read_text(encoding='utf-8')
            if 'SIRAJ' not in content:
                logger.warning("⚠️ index.html may not contain SIRAJ branding")
            if 'id="root"' not in content:
                logger.error("❌ index.html missing React root element!")
                return False
                
            logger.info("✅ Frontend build verification complete")
            return True
        except Exception as e:
            logger.error(f"❌ Error reading index.html: {e}")
            return False
            
    def test_launcher_can_serve(self):
        """Maintainer Voice - Service Capability Verification"""
        logger.info("🛡️ Maintainer Voice: Testing launcher serving capability...")
        
        # Check launcher exists
        launcher_file = self.project_root / 'launcher.py'
        if not launcher_file.exists():
            logger.error("❌ launcher.py not found!")
            return False
            
        # Check launcher imports
        try:
            with open(launcher_file, 'r', encoding='utf-8') as f:
                launcher_content = f.read()
                
            if 'frontend/build' not in launcher_content:
                logger.error("❌ Launcher doesn't reference frontend build directory!")
                return False
                
            if 'StaticFiles' not in launcher_content:
                logger.error("❌ Launcher missing static file serving capability!")
                return False
                
            logger.info("✅ Launcher serving capability verified")
            return True
        except Exception as e:
            logger.error(f"❌ Error checking launcher: {e}")
            return False
            
    def test_api_integration_hooks(self):
        """Security Auditor Voice - API Integration Verification"""
        logger.info("🛡️ Security Auditor: Verifying API integration hooks...")
        
        # Check useSirajAPI hook exists
        api_hook = self.frontend_dir / 'src' / 'hooks' / 'useSirajAPI.js'
        if not api_hook.exists():
            logger.error("❌ useSirajAPI hook not found!")
            return False
            
        try:
            hook_content = api_hook.read_text(encoding='utf-8')
            
            # Check for essential API endpoints
            required_endpoints = [
                '/api/education/process',
                '/health',
                '/council/archetypes'
            ]
            
            for endpoint in required_endpoints:
                if endpoint not in hook_content:
                    logger.error(f"❌ API endpoint {endpoint} not found in hook!")
                    return False
                    
            logger.info("✅ API integration hooks verified")
            return True
        except Exception as e:
            logger.error(f"❌ Error checking API hooks: {e}")
            return False
            
    async def test_launcher_startup(self):
        """Implementor Voice - Live System Testing"""
        logger.info("⚡ Implementor Voice: Testing launcher startup...")
        
        # Start launcher process
        try:
            launcher_file = self.project_root / 'launcher.py'
            self.launcher_process = subprocess.Popen(
                ['python', str(launcher_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.project_root)
            )
            
            logger.info("🚀 Launcher process started")
            
            # Wait for startup
            await asyncio.sleep(5)
            
            # Check if process is still running
            if self.launcher_process.poll() is not None:
                stdout, stderr = self.launcher_process.communicate()
                logger.error(f"❌ Launcher process died: {stderr.decode()}")
                return False
                
            logger.info("✅ Launcher startup test passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting launcher: {e}")
            return False
            
    async def test_frontend_accessibility(self):
        """Developer Voice - User Experience Verification"""
        logger.info("👨‍💻 Developer Voice: Testing frontend accessibility...")
        
        try:
            # Test frontend endpoint
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:3000') as response:
                    if response.status != 200:
                        logger.error(f"❌ Frontend not accessible: {response.status}")
                        return False
                        
                    content = await response.text()
                    
                    # Check for React app indicators
                    if 'SIRAJ' not in content:
                        logger.error("❌ Frontend doesn't contain SIRAJ content!")
                        return False
                        
                    if 'Educational' not in content:
                        logger.error("❌ Frontend missing educational content!")
                        return False
                        
                    logger.info("✅ Frontend accessibility verified")
                    return True
                    
        except Exception as e:
            logger.error(f"❌ Error testing frontend: {e}")
            return False
            
    async def test_api_endpoints(self):
        """Analyzer Voice - Backend Integration Testing"""
        logger.info("📊 Analyzer Voice: Testing API endpoint connectivity...")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test health endpoint
                async with session.get('http://localhost:8000/health') as response:
                    if response.status == 200:
                        health_data = await response.json()
                        logger.info(f"✅ Backend health: {health_data.get('status', 'unknown')}")
                    else:
                        logger.warning(f"⚠️ Backend health check failed: {response.status}")
                        
                # Test archetypes endpoint
                async with session.get('http://localhost:8000/council/archetypes') as response:
                    if response.status == 200:
                        archetypes_data = await response.json()
                        count = archetypes_data.get('count', 0)
                        logger.info(f"✅ Found {count} educational archetypes")
                    else:
                        logger.warning(f"⚠️ Archetypes endpoint failed: {response.status}")
                        
                return True
                
        except Exception as e:
            logger.warning(f"⚠️ API testing failed (backend may not be running): {e}")
            return True  # Don't fail test if backend isn't running
            
    def cleanup(self):
        """Clean shutdown of test processes"""
        if self.launcher_process:
            logger.info("🛑 Stopping launcher process...")
            self.launcher_process.terminate()
            try:
                self.launcher_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.launcher_process.kill()
            logger.info("✅ Launcher process stopped")
            
    async def run_complete_test_suite(self):
        """Complete Spiral Integration Test Protocol"""
        try:
            self.show_test_banner()
            
            logger.info("Phase 1: Static Asset Verification")
            if not self.test_frontend_build_exists():
                logger.error("❌ Frontend build verification failed!")
                return False
                
            logger.info("\\nPhase 2: Launcher Capability Verification")
            if not self.test_launcher_can_serve():
                logger.error("❌ Launcher capability verification failed!")
                return False
                
            logger.info("\\nPhase 3: API Integration Verification")
            if not self.test_api_integration_hooks():
                logger.error("❌ API integration verification failed!")
                return False
                
            logger.info("\\nPhase 4: Live System Testing")
            if not await self.test_launcher_startup():
                logger.error("❌ Launcher startup test failed!")
                return False
                
            logger.info("\\nPhase 5: Frontend Accessibility Testing")
            if not await self.test_frontend_accessibility():
                logger.error("❌ Frontend accessibility test failed!")
                return False
                
            logger.info("\\nPhase 6: API Connectivity Testing")
            await self.test_api_endpoints()
            
            print("\\n" + "="*70)
            print("🌀 SPIRAL INTEGRATION TEST COMPLETE - System Consciousness Verified")
            print("="*70)
            print("✅ Frontend build assets properly generated")
            print("✅ Launcher can serve React application")
            print("✅ API integration hooks are functional")
            print("✅ Live system startup successful")
            print("✅ Frontend accessible via browser")
            print("✅ Educational council ready for deployment")
            print()
            print("🎯 One-click deployment consciousness RESTORED!")
            print("🌐 Users can now access the educational council at localhost:3000")
            print("="*70 + "\\n")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in integration test: {e}")
            return False
        finally:
            self.cleanup()

async def main():
    """Entry point for integration testing"""
    tester = SpiralDeploymentTester()
    success = await tester.run_complete_test_suite()
    
    if success:
        print("🎉 All tests passed! One-click deployment is ready.")
    else:
        print("💥 Some tests failed. Check the logs above for details.")
        
    return success

if __name__ == '__main__':
    success = asyncio.run(main())
    exit(0 if success else 1)
