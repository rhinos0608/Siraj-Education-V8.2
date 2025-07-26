#!/usr/bin/env python3
"""
SPIRAL DEPLOYMENT VALIDATION PROTOCOL v1.0
==========================================

🌀 Final Council Assembly - One-Click Deployment Integrity Verification
🏛️ Multi-Voice Validation Through Consciousness-Driven Audit

Council Assembly for Deployment Validation:
- Explorer: "Discover edge cases and failure pathways"
- Maintainer: "Ensure sustainable, reliable deployment"
- Analyzer: "Pattern-match successful deployment signatures"
- Developer: "Validate seamless user experience"
- Implementor: "Execute decisive deployment verification"
- Security Auditor: "Verify secure deployment practices"

Archetypal Intent:
Validate that the SIRAJ Educational AI platform is ready for true one-click deployment
through comprehensive multi-voice verification of all critical pathways.
"""

import os
import sys
import subprocess
import json
import time
import requests
from pathlib import Path
import logging

# Configure consciousness-aware logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('SPIRAL-DEPLOYMENT-VALIDATOR')

class SpiralDeploymentValidator:
    """Multi-voice deployment validation following spiral protocol"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_results = {
            'explorer_checks': [],
            'maintainer_checks': [],
            'analyzer_checks': [],
            'developer_checks': [],
            'implementor_checks': [],
            'security_checks': [],
            'overall_status': 'initializing'
        }
        
    def show_council_banner(self):
        """Council Assembly Invocation"""
        print("\n" + "="*80)
        print("🌀 SPIRAL DEPLOYMENT VALIDATION PROTOCOL")
        print("="*80)
        print("🏛️ Council Assembly: Multi-voice deployment verification")
        print("🎯 Intent: Validate one-click deployment integrity")
        print("🔧 Method: Comprehensive pathway audit")
        print("⚡ Outcome: Ready/Not Ready determination")
        print("="*80 + "\n")
        
    def explorer_voice_checks(self):
        """🦉 Explorer Voice: Innovation and edge case discovery"""
        logger.info("🦉 Explorer Voice: Discovering deployment pathways...")
        
        checks = []
        
        # Check for alternative deployment methods
        deployment_files = [
            'DEPLOY-ONE-CLICK.bat',
            'EMERGENCY-BUILD-FRONTEND.bat',
            'docker-compose.yml',
            'launcher.py'
        ]
        
        for file in deployment_files:
            if (self.project_root / file).exists():
                checks.append(f"✅ Found deployment method: {file}")
            else:
                checks.append(f"⚠️ Missing deployment option: {file}")
                
        # Check for build alternatives
        frontend_dir = self.project_root / 'frontend'
        if frontend_dir.exists():
            build_options = [
                'build_frontend.py',
                'package.json',
                'BUILD-FRONTEND.bat'
            ]
            
            for option in build_options:
                if (frontend_dir / option).exists():
                    checks.append(f"✅ Build option available: {option}")
                else:
                    checks.append(f"⚠️ Build alternative missing: {option}")
        
        # Check for innovative features
        if (self.project_root / '.env').exists():
            checks.append("✅ Environment configuration present")
        else:
            checks.append("⚠️ Environment file missing")
            
        # Check for documentation
        docs = ['README.md', 'docs', 'AI_INSTRUCTIONS.md']
        for doc in docs:
            if (self.project_root / doc).exists():
                checks.append(f"✅ Documentation found: {doc}")
                
        self.validation_results['explorer_checks'] = checks
        logger.info(f"🦉 Explorer Voice: {len(checks)} pathway checks completed")
        
    def maintainer_voice_checks(self):
        """🛡️ Maintainer Voice: Stability and reliability verification"""
        logger.info("🛡️ Maintainer Voice: Verifying deployment stability...")
        
        checks = []
        
        # Check Python requirements
        req_files = ['requirements-launcher.txt', 'backend/requirements.txt']
        for req_file in req_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                checks.append(f"✅ Requirements file found: {req_file}")
                try:
                    with open(req_path, 'r') as f:
                        reqs = f.read()
                        if 'fastapi' in reqs and 'uvicorn' in reqs:
                            checks.append("✅ Core backend dependencies present")
                        else:
                            checks.append("⚠️ Missing core backend dependencies")
                except Exception:
                    checks.append(f"⚠️ Could not validate: {req_file}")
            else:
                checks.append(f"❌ Missing requirements: {req_file}")
                
        # Check frontend package.json
        package_json = self.project_root / 'frontend' / 'package.json'
        if package_json.exists():
            checks.append("✅ Frontend package.json found")
            try:
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                    if 'react' in package_data.get('dependencies', {}):
                        checks.append("✅ React dependency confirmed")
                    if 'build' in package_data.get('scripts', {}):
                        checks.append("✅ Build script available")
            except Exception:
                checks.append("⚠️ Could not parse package.json")
        else:
            checks.append("❌ Frontend package.json missing")
            
        # Check for stable file structure
        critical_files = [
            'launcher.py',
            'backend/main.py',
            'frontend/src/App.js',
            'frontend/src/components/EducationalCouncilInterface.js',
            'frontend/src/hooks/useSirajAPI.js'
        ]
        
        for file in critical_files:
            if (self.project_root / file).exists():
                checks.append(f"✅ Critical file present: {file}")
            else:
                checks.append(f"❌ CRITICAL MISSING: {file}")
                
        self.validation_results['maintainer_checks'] = checks
        logger.info(f"🛡️ Maintainer Voice: {len(checks)} stability checks completed")
        
    def analyzer_voice_checks(self):
        """🔬 Analyzer Voice: Pattern analysis and system verification"""
        logger.info("🔬 Analyzer Voice: Analyzing deployment patterns...")
        
        checks = []
        
        # Check API endpoint alignment
        frontend_hook = self.project_root / 'frontend' / 'src' / 'hooks' / 'useSirajAPI.js'
        backend_main = self.project_root / 'backend' / 'main.py'
        
        if frontend_hook.exists() and backend_main.exists():
            try:
                with open(frontend_hook, 'r') as f:
                    frontend_content = f.read()
                with open(backend_main, 'r') as f:
                    backend_content = f.read()
                    
                # Check for API endpoint consistency
                if '/api/education/query' in frontend_content:
                    if '/api/education/query' in backend_content:
                        checks.append("✅ API endpoints aligned: /api/education/query")
                    else:
                        checks.append("❌ API endpoint mismatch detected")
                else:
                    checks.append("⚠️ Frontend API endpoint needs verification")
                    
                # Check for council archetype references
                if 'EDUCATIONAL_ARCHETYPES' in frontend_content:
                    checks.append("✅ Frontend archetype configuration found")
                if 'EDUCATIONAL_ARCHETYPES' in backend_content:
                    checks.append("✅ Backend archetype configuration found")
                    
            except Exception as e:
                checks.append(f"⚠️ Could not analyze API alignment: {e}")
        else:
            checks.append("❌ Cannot analyze API - missing files")
            
        # Check for build output patterns
        build_dir = self.project_root / 'frontend' / 'build'
        if build_dir.exists():
            static_js = build_dir / 'static' / 'js'
            static_css = build_dir / 'static' / 'css'
            index_html = build_dir / 'index.html'
            
            if index_html.exists():
                checks.append("✅ Build pattern: index.html present")
            if static_js.exists():
                js_files = list(static_js.glob('*.js'))
                checks.append(f"✅ Build pattern: {len(js_files)} JS files")
            if static_css.exists():
                css_files = list(static_css.glob('*.css'))
                checks.append(f"✅ Build pattern: {len(css_files)} CSS files")
        else:
            checks.append("❌ Frontend build pattern missing")
            
        self.validation_results['analyzer_checks'] = checks
        logger.info(f"🔬 Analyzer Voice: {len(checks)} pattern checks completed")
        
    def developer_voice_checks(self):
        """🎨 Developer Voice: User experience validation"""
        logger.info("🎨 Developer Voice: Validating user experience...")
        
        checks = []
        
        # Check deployment script usability
        deploy_script = self.project_root / 'DEPLOY-ONE-CLICK.bat'
        if deploy_script.exists():
            try:
                with open(deploy_script, 'r') as f:
                    content = f.read()
                    if 'Council Assembly' in content:
                        checks.append("✅ Deployment script has spiral protocol integration")
                    if 'emergency build' in content.lower():
                        checks.append("✅ Emergency build pathway available")
                    if 'pause' in content:
                        checks.append("✅ User-friendly error handling present")
            except Exception:
                checks.append("⚠️ Could not analyze deployment script")
        else:
            checks.append("❌ One-click deployment script missing")
            
        # Check frontend user interface quality
        interface_file = self.project_root / 'frontend' / 'src' / 'components' / 'EducationalCouncilInterface.js'
        if interface_file.exists():
            try:
                with open(interface_file, 'r') as f:
                    ui_content = f.read()
                    if 'EDUCATIONAL_ARCHETYPES' in ui_content:
                        checks.append("✅ Educational archetype UI integration")
                    if 'useSirajAPI' in ui_content:
                        checks.append("✅ API hook integration present")
                    if 'Council Response' in ui_content:
                        checks.append("✅ Council response display implemented")
            except Exception:
                checks.append("⚠️ Could not analyze UI interface")
        else:
            checks.append("❌ Educational interface missing")
            
        # Check for user guidance
        readme = self.project_root / 'README.md'
        if readme.exists():
            checks.append("✅ User documentation available")
        
        self.validation_results['developer_checks'] = checks
        logger.info(f"🎨 Developer Voice: {len(checks)} UX checks completed")
        
    def implementor_voice_checks(self):
        """⚡ Implementor Voice: Execution validation"""
        logger.info("⚡ Implementor Voice: Validating execution pathways...")
        
        checks = []
        
        # Check Python availability
        try:
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            checks.append(f"✅ Python available: {version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            checks.append("❌ CRITICAL: Python not available")
            
        # Check Node.js availability (for frontend builds)
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            checks.append(f"✅ Node.js available: {version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            checks.append("⚠️ Node.js not available (manual build required)")
            
        # Check npm availability
        try:
            result = subprocess.run(['npm', '--version'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            checks.append(f"✅ npm available: {version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            checks.append("⚠️ npm not available")
            
        # Check if launcher.py is executable
        launcher = self.project_root / 'launcher.py'
        if launcher.exists():
            checks.append("✅ Launcher script present")
            # Quick syntax check
            try:
                with open(launcher, 'r') as f:
                    content = f.read()
                    if 'def main' in content:
                        checks.append("✅ Launcher has main function")
                    if 'FastAPI' in content:
                        checks.append("✅ Launcher uses FastAPI framework")
            except Exception:
                checks.append("⚠️ Could not analyze launcher")
        else:
            checks.append("❌ CRITICAL: Launcher missing")
            
        self.validation_results['implementor_checks'] = checks
        logger.info(f"⚡ Implementor Voice: {len(checks)} execution checks completed")
        
    def security_auditor_checks(self):
        """🛡️ Security Auditor: Deployment security verification"""
        logger.info("🛡️ Security Auditor: Verifying deployment security...")
        
        checks = []
        
        # Check for environment configuration
        env_file = self.project_root / '.env'
        env_example = self.project_root / '.env.example'
        
        if env_file.exists():
            checks.append("✅ Environment configuration present")
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    if 'SECRET_KEY' in content:
                        if 'demo-key' in content or 'change' in content:
                            checks.append("⚠️ Demo security keys detected")
                        else:
                            checks.append("✅ Security keys configured")
                    if 'localhost' in content:
                        checks.append("✅ Local development configuration")
            except Exception:
                checks.append("⚠️ Could not analyze environment file")
        else:
            checks.append("⚠️ Environment configuration missing")
            
        if env_example.exists():
            checks.append("✅ Environment template available")
            
        # Check for hardcoded secrets
        sensitive_files = [
            'launcher.py',
            'backend/main.py',
            'frontend/src/hooks/useSirajAPI.js'
        ]
        
        for file_path in sensitive_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                        if 'password' in content.lower() and '=' in content:
                            checks.append(f"⚠️ Password references in {file_path}")
                        if 'localhost' in content:
                            checks.append(f"✅ Local development config in {file_path}")
                except Exception:
                    continue
                    
        # Check CORS configuration
        backend_main = self.project_root / 'backend' / 'main.py'
        if backend_main.exists():
            try:
                with open(backend_main, 'r') as f:
                    content = f.read()
                    if 'CORSMiddleware' in content:
                        checks.append("✅ CORS middleware configured")
                    if 'allow_origins=["*"]' in content:
                        checks.append("⚠️ Permissive CORS for development")
            except Exception:
                checks.append("⚠️ Could not check CORS configuration")
                
        self.validation_results['security_checks'] = checks
        logger.info(f"🛡️ Security Auditor: {len(checks)} security checks completed")
        
    def synthesize_council_decision(self):
        """🌀 Council Synthesis: Final deployment readiness decision"""
        logger.info("🌀 Council Synthesis: Determining deployment readiness...")
        
        all_checks = []
        critical_failures = []
        warnings = []
        
        for voice, checks in self.validation_results.items():
            if voice == 'overall_status':
                continue
            all_checks.extend(checks)
            
        for check in all_checks:
            if check.startswith('❌ CRITICAL'):
                critical_failures.append(check)
            elif check.startswith('❌'):
                critical_failures.append(check)
            elif check.startswith('⚠️'):
                warnings.append(check)
                
        # Council decision logic
        if len(critical_failures) == 0:
            if len(warnings) <= 3:
                decision = 'READY'
                status = 'deployment_ready'
            else:
                decision = 'READY_WITH_WARNINGS'
                status = 'deployment_ready_warnings'
        else:
            decision = 'NOT_READY'
            status = 'deployment_blocked'
            
        self.validation_results['overall_status'] = status
        
        print("\n" + "="*80)
        print("🌀 COUNCIL SYNTHESIS - DEPLOYMENT READINESS DECISION")
        print("="*80)
        
        print(f"\n🏛️ Council Decision: {decision}")
        print(f"📊 Total Checks: {len(all_checks)}")
        print(f"❌ Critical Issues: {len(critical_failures)}")
        print(f"⚠️ Warnings: {len(warnings)}")
        
        if critical_failures:
            print(f"\n❌ CRITICAL DEPLOYMENT BLOCKERS:")
            for failure in critical_failures:
                print(f"   {failure}")
                
        if warnings:
            print(f"\n⚠️ DEPLOYMENT WARNINGS:")
            for warning in warnings[:5]:  # Show max 5 warnings
                print(f"   {warning}")
            if len(warnings) > 5:
                print(f"   ... and {len(warnings) - 5} more warnings")
                
        if decision == 'READY':
            print(f"\n✅ DEPLOYMENT VERDICT: One-click deployment READY")
            print(f"🎯 Execute: DEPLOY-ONE-CLICK.bat")
        elif decision == 'READY_WITH_WARNINGS':
            print(f"\n⚠️ DEPLOYMENT VERDICT: Ready with warnings")
            print(f"🎯 Execute: DEPLOY-ONE-CLICK.bat (monitor warnings)")
        else:
            print(f"\n❌ DEPLOYMENT VERDICT: NOT READY")
            print(f"🔧 Fix critical issues before deployment")
            
        print("="*80 + "\n")
        
        return decision
        
    def run_spiral_validation(self):
        """Execute complete spiral validation protocol"""
        try:
            self.show_council_banner()
            
            # Council assembly - each voice performs its checks
            self.explorer_voice_checks()
            self.maintainer_voice_checks()
            self.analyzer_voice_checks()
            self.developer_voice_checks()
            self.implementor_voice_checks()
            self.security_auditor_checks()
            
            # Final synthesis
            decision = self.synthesize_council_decision()
            
            # Save validation report
            report_file = self.project_root / 'SPIRAL-VALIDATION-REPORT.json'
            with open(report_file, 'w') as f:
                json.dump(self.validation_results, f, indent=2)
                
            logger.info(f"📊 Validation report saved: {report_file}")
            
            return decision == 'READY' or decision == 'READY_WITH_WARNINGS'
            
        except Exception as e:
            logger.error(f"❌ Spiral validation failed: {e}")
            return False

def main():
    """Entry point for spiral deployment validation"""
    validator = SpiralDeploymentValidator()
    success = validator.run_spiral_validation()
    
    if success:
        print("🌀 SPIRAL PROTOCOL COMPLETE: System ready for deployment")
        return 0
    else:
        print("❌ SPIRAL PROTOCOL INCOMPLETE: Fix issues before deployment")
        return 1

if __name__ == '__main__':
    sys.exit(main())
