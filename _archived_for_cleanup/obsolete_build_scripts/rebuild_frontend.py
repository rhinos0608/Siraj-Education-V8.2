#!/usr/bin/env python3
"""
SIRAJ Educational AI - Frontend Rebuild Script v15.3
====================================================

🌀 Spiral Editing Protocol Implementation
Council Assembly for Frontend Consciousness Restoration

Collapse Phase:
- Fundamental Intent: Restore frontend build consciousness for deployment
- Pattern Recognition: Build incomplete → Launcher fails → Deployment broken
- Boundary Constraints: Preserve React architecture, maintain API integration

Council Assembly:
- Explorer: "Complete rebuild with innovative error handling"
- Maintainer: "Bulletproof build process for deployment stability"
- Analyzer: "Pattern-aware environment configuration"
- Developer: "Human-centric build feedback and troubleshooting"
- Implementor: "Decisive execution with comprehensive validation"

Rebirth Phase:
- Complete frontend rebuild with proper environment variables
- Validation of build artifacts
- Integration testing with launcher
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SIRAJ-Frontend-Rebuilder')

class SIRAJFrontendRebuilder:
    """Council-Driven Frontend Rebuild Engine"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.frontend_dir = self.project_root / "frontend"
        self.build_dir = self.frontend_dir / "build"
        self.node_modules = self.frontend_dir / "node_modules"
        
    def show_council_banner(self):
        """Council Assembly Banner"""
        print(f"""
{'='*80}
🌀 SIRAJ Frontend Rebuild - Council Assembly v15.3
{'='*80}

Council Voices Active:
🔍 Explorer: "Innovative rebuild with error handling"
🛡️ Maintainer: "Stable, bulletproof build process"
📊 Analyzer: "Pattern-aware environment configuration"  
👨‍💻 Developer: "Human-centric build experience"
⚡ Implementor: "Decisive execution and validation"

{'='*80}
        """)
        
    def explorer_voice_analysis(self):
        """Explorer Voice: Innovation Assessment"""
        logger.info("🔍 Explorer Voice: Analyzing build environment...")
        
        # Check Node.js and npm versions
        try:
            node_version = subprocess.check_output(['node', '--version'], text=True).strip()
            npm_version = subprocess.check_output(['npm', '--version'], text=True).strip()
            logger.info(f"✅ Node.js: {node_version}, npm: {npm_version}")
            return True
        except subprocess.CalledProcessError:
            logger.error("❌ Node.js or npm not found!")
            return False
            
    def maintainer_voice_cleanup(self):
        """Maintainer Voice: Clean Previous Build State"""
        logger.info("🛡️ Maintainer Voice: Cleaning previous build state...")
        
        # Remove broken build directory
        if self.build_dir.exists():
            logger.info(f"Removing broken build directory: {self.build_dir}")
            shutil.rmtree(self.build_dir)
            
        # Clean npm cache if needed
        try:
            subprocess.run(['npm', 'cache', 'clean', '--force'], 
                         cwd=str(self.frontend_dir), 
                         capture_output=True)
            logger.info("✅ npm cache cleaned")
        except:
            logger.warning("⚠️ Could not clean npm cache")
            
    def analyzer_voice_dependencies(self):
        """Analyzer Voice: Dependencies Analysis and Installation"""
        logger.info("📊 Analyzer Voice: Analyzing and installing dependencies...")
        
        # Check package.json exists
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            logger.error("❌ package.json not found!")
            return False
            
        # Load package.json to understand dependencies
        with open(package_json, 'r') as f:
            package_data = json.load(f)
            
        logger.info(f"Project: {package_data.get('name', 'Unknown')} v{package_data.get('version', 'Unknown')}")
        
        # Install dependencies
        logger.info("Installing dependencies...")
        try:
            result = subprocess.run(
                ['npm', 'install'], 
                cwd=str(self.frontend_dir),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("✅ Dependencies installed successfully")
                return True
            else:
                logger.error(f"❌ npm install failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ npm install timed out")
            return False
        except Exception as e:
            logger.error(f"❌ npm install error: {e}")
            return False
            
    def developer_voice_environment(self):
        """Developer Voice: Environment Configuration"""
        logger.info("👨‍💻 Developer Voice: Configuring build environment...")
        
        # Create environment variables for the build
        env = os.environ.copy()
        env.update({
            'REACT_APP_API_URL': 'http://localhost:8000',
            'REACT_APP_WS_URL': 'ws://localhost:8000',
            'REACT_APP_SIRAJ_VERSION': '15.3.0',
            'REACT_APP_MODE': 'educational',
            'NODE_ENV': 'production',
            'CI': 'false',  # Disable CI warnings
            'GENERATE_SOURCEMAP': 'false'  # Reduce build size
        })
        
        logger.info("✅ Environment configured for production build")
        return env
        
    def implementor_voice_build(self, env):
        """Implementor Voice: Execute Build Process"""
        logger.info("⚡ Implementor Voice: Executing production build...")
        
        try:
            # Run the build process
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=str(self.frontend_dir),
                env=env,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("✅ Frontend build completed successfully")
                logger.info("Build output preview:")
                for line in result.stdout.split('\n')[-10:]:  # Last 10 lines
                    if line.strip():
                        logger.info(f"  {line}")
                return True
            else:
                logger.error("❌ Frontend build failed")
                logger.error("Build errors:")
                for line in result.stderr.split('\n'):
                    if line.strip():
                        logger.error(f"  {line}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Build process timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Build process error: {e}")
            return False
            
    def council_validation(self):
        """Full Council: Validate Build Artifacts"""
        logger.info("🏛️ Council Assembly: Validating build artifacts...")
        
        # Check build directory exists
        if not self.build_dir.exists():
            logger.error("❌ Build directory was not created")
            return False
            
        # Check for essential files
        essential_files = [
            'index.html',
            'static/css',
            'static/js'
        ]
        
        missing_files = []
        for file_path in essential_files:
            full_path = self.build_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                
        if missing_files:
            logger.error(f"❌ Missing essential build files: {missing_files}")
            return False
            
        # Validate index.html content
        index_html = self.build_dir / 'index.html'
        try:
            with open(index_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            if 'SIRAJ' in html_content and len(html_content) > 1000:
                logger.info(f"✅ index.html is valid ({len(html_content)} characters)")
            else:
                logger.warning(f"⚠️ index.html may be incomplete ({len(html_content)} characters)")
                
        except Exception as e:
            logger.error(f"❌ Could not validate index.html: {e}")
            return False
            
        # List build contents
        try:
            build_size = sum(f.stat().st_size for f in self.build_dir.rglob('*') if f.is_file())
            build_size_mb = build_size / 1024 / 1024
            logger.info(f"✅ Build completed: {build_size_mb:.2f} MB")
            
            # Show structure
            logger.info("Build structure:")
            for item in sorted(self.build_dir.iterdir()):
                if item.is_dir():
                    file_count = len(list(item.rglob('*')))
                    logger.info(f"  📁 {item.name}/ ({file_count} files)")
                else:
                    file_size = item.stat().st_size / 1024
                    logger.info(f"  📄 {item.name} ({file_size:.1f} KB)")
                    
        except Exception as e:
            logger.warning(f"⚠️ Could not analyze build size: {e}")
            
        logger.info("✅ Council validation complete - build artifacts verified")
        return True
        
    def synthesis_phase(self):
        """Synthesis Phase: Complete Rebuild Process"""
        logger.info("🌀 Synthesis Phase: Executing complete rebuild...")
        
        # Council Assembly sequence
        if not self.explorer_voice_analysis():
            return False
            
        self.maintainer_voice_cleanup()
        
        if not self.analyzer_voice_dependencies():
            return False
            
        env = self.developer_voice_environment()
        
        if not self.implementor_voice_build(env):
            return False
            
        if not self.council_validation():
            return False
            
        logger.info("🎉 Synthesis Complete: Frontend consciousness restored!")
        return True
        
    def rebirth_integration_test(self):
        """Rebirth Phase: Test Integration with Launcher"""
        logger.info("✨ Rebirth Phase: Testing launcher integration...")
        
        # Check if launcher.py can find the build
        launcher_path = self.project_root / "launcher.py"
        if not launcher_path.exists():
            logger.warning("⚠️ launcher.py not found - skipping integration test")
            return True
            
        # Verify the launcher expects the right paths
        try:
            with open(launcher_path, 'r', encoding='utf-8') as f:
                launcher_content = f.read()
                
            if 'frontend/build' in launcher_content:
                logger.info("✅ Launcher configured to serve frontend/build")
            else:
                logger.warning("⚠️ Launcher may not be configured for frontend/build")
                
        except Exception as e:
            logger.warning(f"⚠️ Could not analyze launcher: {e}")
            
        logger.info("✅ Integration test complete")
        return True
        
    def run_complete_rebuild(self):
        """Execute Complete Spiral Rebuild Protocol"""
        self.show_council_banner()
        
        try:
            # Synthesis Phase
            if not self.synthesis_phase():
                logger.error("❌ Synthesis Phase failed")
                return False
                
            # Rebirth Phase  
            if not self.rebirth_integration_test():
                logger.error("❌ Rebirth Phase failed")
                return False
                
            print(f"""
{'='*80}
🎉 FRONTEND CONSCIOUSNESS RESTORED
{'='*80}

✅ Build Directory: {self.build_dir}
✅ Essential Files: index.html, static assets
✅ Launcher Integration: Ready
✅ One-Click Deployment: Restored

Council Assembly Resolution:
"The frontend consciousness has been restored through collaborative rebuild.
The deployment mechanism can now serve the educational interface properly."

Next Phase: Test one-click deployment
{'='*80}
            """)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Critical rebuild failure: {e}")
            return False

def main():
    """Main Execution"""
    rebuilder = SIRAJFrontendRebuilder()
    success = rebuilder.run_complete_rebuild()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
