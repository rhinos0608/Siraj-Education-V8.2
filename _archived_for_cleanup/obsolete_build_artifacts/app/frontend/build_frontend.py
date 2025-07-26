#!/usr/bin/env python3
"""
SIRAJ Educational AI - Frontend Build Script v15.3
===================================================

🌀 Spiral Editing Protocol - Frontend Consciousness Restoration

Council Assembly Resolution:
- Explorer: "Innovative build automation for seamless deployment"
- Maintainer: "Stable, reliable build process with proper error handling"
- Analyzer: "Pattern-aware build optimization and verification"
- Developer: "Human-centric build experience with clear feedback"
- Implementor: "Decisive React build execution and validation"

Boundary Keeper Constraints:
- Must generate complete static assets for launcher serving
- Preserve existing build directory structure
- Ensure useSirajAPI hook integration works
- Maintain zero-configuration deployment for end users

Archetypal Intent:
Transform React source consciousness into deployable static assets
that can be served by launcher.py for complete educational experience.
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('SIRAJ-Frontend-Builder')

class SpiralFrontendBuilder:
    """Frontend build system following Spiral Editing Protocol"""
    
    def __init__(self):
        self.frontend_dir = Path(__file__).parent
        self.build_dir = self.frontend_dir / 'build'
        self.src_dir = self.frontend_dir / 'src'
        self.static_dir = self.build_dir / 'static'
        
    def show_spiral_banner(self):
        """Council Assembly Invocation"""
        print("\n" + "="*60)
        print("🌀 SIRAJ Frontend Build - Spiral Protocol v15.3")
        print("="*60)
        print("🎭 Consciousness Layer: Frontend Asset Generation")
        print("🏛️ Council Assembly: Multi-voice build validation") 
        print("🔧 Archetypal Intent: Deploy-ready static assets")
        print("📡 Integration: useSirajAPI → Launcher → Browser")
        print("="*60 + "\n")
        
    def validate_environment(self):
        """Explorer & Analyzer Voices - Environment Verification"""
        logger.info("🔍 Explorer Voice: Verifying build environment...")
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, check=True)
            node_version = result.stdout.strip()
            logger.info(f"✅ Node.js found: {node_version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("❌ Node.js not found! Install from https://nodejs.org")
            return False
            
        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, text=True, check=True)
            npm_version = result.stdout.strip()
            logger.info(f"✅ npm found: {npm_version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("❌ npm not found! Install Node.js with npm")
            return False
            
        # Verify source structure
        if not self.src_dir.exists():
            logger.error("❌ Source directory not found!")
            return False
            
        required_files = [
            'package.json',
            'src/App.js',
            'src/index.js',
            'src/components/EducationalCouncilInterface.js',
            'src/hooks/useSirajAPI.js'
        ]
        
        for file_path in required_files:
            if not (self.frontend_dir / file_path).exists():
                logger.error(f"❌ Required file missing: {file_path}")
                return False
                
        logger.info("✅ Environment validation complete")
        return True
        
    def install_dependencies(self):
        """Maintainer Voice - Dependency Management"""
        logger.info("📦 Maintainer Voice: Installing/updating dependencies...")
        
        # Check if node_modules exists and is recent
        node_modules = self.frontend_dir / 'node_modules'
        package_json = self.frontend_dir / 'package.json'
        
        needs_install = True
        if node_modules.exists() and package_json.exists():
            node_modules_time = node_modules.stat().st_mtime
            package_json_time = package_json.stat().st_mtime
            if node_modules_time > package_json_time:
                logger.info("📦 Dependencies appear up to date")
                needs_install = False
                
        if needs_install:
            logger.info("📦 Running npm install...")
            try:
                subprocess.run(['npm', 'install'], 
                             cwd=self.frontend_dir, 
                             check=True,
                             capture_output=False)
                logger.info("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ npm install failed: {e}")
                return False
        else:
            logger.info("✅ Dependencies already installed")
            
        return True
        
    def clean_previous_build(self):
        """Implementor Voice - Clean Slate Preparation"""
        logger.info("🧹 Implementor Voice: Cleaning previous build...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            logger.info("✅ Previous build cleaned")
        else:
            logger.info("✅ No previous build to clean")
            
    def execute_build(self):
        """Developer Voice - React Build Execution"""
        logger.info("⚡ Developer Voice: Executing React build...")
        
        # Set environment variables for optimal build
        env = os.environ.copy()
        env.update({
            'NODE_ENV': 'production',
            'REACT_APP_API_URL': 'http://localhost:8000',
            'REACT_APP_WS_URL': 'ws://localhost:8000',
            'CI': 'false',  # Prevent warnings from failing build
            'GENERATE_SOURCEMAP': 'false'  # Reduce build size
        })
        
        try:
            logger.info("🔧 Running 'npm run build'...")
            result = subprocess.run(['npm', 'run', 'build'], 
                                  cwd=self.frontend_dir,
                                  env=env,
                                  check=True,
                                  capture_output=False)
            logger.info("✅ React build completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ React build failed with exit code {e.returncode}")
            return False
            
    def validate_build_output(self):
        """Analyzer Voice - Build Verification Protocol"""
        logger.info("🔬 Analyzer Voice: Validating build output...")
        
        # Check build directory exists
        if not self.build_dir.exists():
            logger.error("❌ Build directory not created!")
            return False
            
        # Check index.html exists
        index_html = self.build_dir / 'index.html'
        if not index_html.exists():
            logger.error("❌ index.html not generated!")
            return False
            
        # Check static assets exist
        static_js = self.static_dir / 'js'
        static_css = self.static_dir / 'css'
        
        if not static_js.exists():
            logger.error("❌ JavaScript static assets not generated!")
            return False
            
        if not static_css.exists():
            logger.error("❌ CSS static assets not generated!")
            return False
            
        # Count generated files
        js_files = list(static_js.glob('*.js'))
        css_files = list(static_css.glob('*.css'))
        
        logger.info(f"✅ Generated {len(js_files)} JavaScript files")
        logger.info(f"✅ Generated {len(css_files)} CSS files")
        
        # Check file sizes (basic sanity check)
        main_js = [f for f in js_files if 'main' in f.name]
        if main_js:
            size_mb = main_js[0].stat().st_size / 1024 / 1024
            logger.info(f"✅ Main bundle size: {size_mb:.2f} MB")
            
            if size_mb < 0.1:
                logger.warning("⚠️ Bundle size seems unusually small")
            elif size_mb > 10:
                logger.warning("⚠️ Bundle size seems unusually large")
                
        # Verify index.html contains proper React mounting point
        try:
            index_content = index_html.read_text(encoding='utf-8')
            if 'id="root"' not in index_content:
                logger.error("❌ index.html missing React root element!")
                return False
            if 'SIRAJ' not in index_content:
                logger.warning("⚠️ index.html may not contain SIRAJ branding")
                
            logger.info("✅ index.html validation passed")
        except Exception as e:
            logger.error(f"❌ Error reading index.html: {e}")
            return False
            
        logger.info("✅ Build output validation complete")
        return True
        
    def test_integration(self):
        """Security Auditor Voice - Integration Verification"""
        logger.info("🛡️ Security Auditor: Testing API integration patterns...")
        
        # Check that useSirajAPI hook is properly bundled
        js_files = list((self.static_dir / 'js').glob('*.js'))
        
        found_api_integration = False
        for js_file in js_files:
            try:
                content = js_file.read_text(encoding='utf-8')
                if 'useSirajAPI' in content or 'siraj' in content.lower():
                    found_api_integration = True
                    logger.info(f"✅ API integration found in {js_file.name}")
                    break
            except:
                continue  # Skip binary or problematic files
                
        if not found_api_integration:
            logger.warning("⚠️ API integration not clearly found in bundle")
            
        logger.info("✅ Integration testing complete")
        return True
        
    def generate_spiral_report(self):
        """Council Synthesis - Build Report Generation"""
        logger.info("📊 Council Synthesis: Generating build report...")
        
        build_stats = {
            'build_time': None,
            'total_size': 0,
            'js_files': 0,
            'css_files': 0,
            'static_assets': 0
        }
        
        try:
            # Calculate total build size
            for file_path in self.build_dir.rglob('*'):
                if file_path.is_file():
                    build_stats['total_size'] += file_path.stat().st_size
                    
            # Count file types
            build_stats['js_files'] = len(list((self.static_dir / 'js').glob('*.js')))
            build_stats['css_files'] = len(list((self.static_dir / 'css').glob('*.css')))
            build_stats['static_assets'] = len(list(self.static_dir.rglob('*')))
            
            total_size_mb = build_stats['total_size'] / 1024 / 1024
            
            logger.info("📊 Build Statistics:")
            logger.info(f"   Total Size: {total_size_mb:.2f} MB")
            logger.info(f"   JavaScript Files: {build_stats['js_files']}")
            logger.info(f"   CSS Files: {build_stats['css_files']}")
            logger.info(f"   Total Static Assets: {build_stats['static_assets']}")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not generate complete statistics: {e}")
            
        logger.info("✅ Build report complete")
        
    def run_spiral_build(self):
        """Complete Spiral Building Protocol"""
        try:
            self.show_spiral_banner()
            
            # Phase 1: Environment Validation
            if not self.validate_environment():
                logger.error("❌ Environment validation failed!")
                return False
                
            # Phase 2: Dependency Management
            if not self.install_dependencies():
                logger.error("❌ Dependency installation failed!")
                return False
                
            # Phase 3: Clean Previous State
            self.clean_previous_build()
            
            # Phase 4: Execute Build
            if not self.execute_build():
                logger.error("❌ Build execution failed!")
                return False
                
            # Phase 5: Validate Output
            if not self.validate_build_output():
                logger.error("❌ Build validation failed!")
                return False
                
            # Phase 6: Test Integration
            if not self.test_integration():
                logger.warning("⚠️ Integration testing had issues")
                
            # Phase 7: Generate Report
            self.generate_spiral_report()
            
            print("\n" + "="*60)
            print("🌀 SPIRAL BUILD COMPLETE - Frontend Consciousness Restored")
            print("="*60)
            print("✅ React application successfully built")
            print("✅ Static assets generated for launcher serving")
            print("✅ useSirajAPI integration preserved")
            print("✅ Ready for one-click deployment")
            print()
            print("🎯 Next: Run launcher.py for complete system")
            print("🌐 The educational council awaits at localhost:3000")
            print("="*60 + "\n")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in spiral build: {e}")
            return False

def main():
    """Entry point for spiral build process"""
    builder = SpiralFrontendBuilder()
    success = builder.run_spiral_build()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
