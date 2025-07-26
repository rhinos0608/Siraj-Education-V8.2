#!/usr/bin/env python3
"""
SIRAJ Educational AI - Build Script
==================================

This script builds the complete SIRAJ Educational AI platform into a standalone executable.
It handles:
- Building the React frontend
- Installing Python dependencies
- Creating the executable with PyInstaller
- Packaging all necessary files
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SIRAJ-Builder')

class SIRAJBuilder:
    """Builder for SIRAJ Educational AI executable"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.backend_dir = self.project_root / 'backend'
        self.frontend_dir = self.project_root / 'frontend'
        self.build_dir = self.project_root / 'build'
        self.dist_dir = self.project_root / 'dist'
        self.platform = platform.system().lower()
        
    def clean(self):
        """Clean previous builds"""
        logger.info("Cleaning previous builds...")
        
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                logger.info(f"Removed: {dir_path}")
                
        # Clean frontend build
        frontend_build = self.frontend_dir / 'build'
        if frontend_build.exists():
            shutil.rmtree(frontend_build)
            logger.info(f"Removed: {frontend_build}")
            
    def install_dependencies(self):
        """Install required Python dependencies"""
        logger.info("Installing Python dependencies...")
        
        # Install PyInstaller if not present
        try:
            import PyInstaller
            logger.info("PyInstaller is already installed")
        except ImportError:
            logger.info("Installing PyInstaller...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            
        # Install backend requirements
        requirements_file = self.backend_dir / 'requirements.txt'
        if requirements_file.exists():
            logger.info("Installing backend requirements...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ])
        else:
            logger.warning("No requirements.txt found, installing essential packages...")
            essential_packages = [
                'fastapi',
                'uvicorn[standard]',
                'sqlalchemy',
                'aiosqlite',
                'python-multipart',
                'python-jose[cryptography]',
                'passlib[bcrypt]',
                'httpx',
                'websockets',
                'aiofiles',
                'email-validator',
                'python-dotenv',
                'requests'
            ]
            for package in essential_packages:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                
    def build_frontend(self):
        """Build the React frontend"""
        logger.info("Building React frontend...")
        
        if not (self.frontend_dir / 'package.json').exists():
            logger.error("Frontend package.json not found!")
            return False
            
        # Check if npm is installed
        try:
            subprocess.run(['npm', '--version'], check=True, capture_output=True)
        except:
            logger.error("npm is not installed! Please install Node.js and npm.")
            return False
            
        # Install frontend dependencies
        logger.info("Installing frontend dependencies...")
        subprocess.check_call(['npm', 'install'], cwd=str(self.frontend_dir))
        
        # Build frontend for production
        logger.info("Building frontend for production...")
        env = os.environ.copy()
        env['REACT_APP_API_URL'] = 'http://localhost:8000'
        env['REACT_APP_WS_URL'] = 'ws://localhost:8000'
        env['CI'] = 'false'  # Disable CI mode to ignore warnings
        
        subprocess.check_call(['npm', 'run', 'build'], cwd=str(self.frontend_dir), env=env)
        
        frontend_build = self.frontend_dir / 'build'
        if not frontend_build.exists():
            logger.error("Frontend build failed!")
            return False
            
        logger.info("Frontend build successful!")
        return True
        
    def create_version_file(self):
        """Create version file for Windows executable"""
        version_content = """
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(8, 1, 0, 0),
    prodvers=(8, 1, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'SIRAJ Educational AI Team'),
        StringStruct(u'FileDescription', u'SIRAJ Educational AI - Multi-Voice Learning Platform'),
        StringStruct(u'FileVersion', u'8.1.0.0'),
        StringStruct(u'InternalName', u'SIRAJ-Educational-AI'),
        StringStruct(u'LegalCopyright', u'© 2025 SIRAJ Educational AI Team. MIT License.'),
        StringStruct(u'OriginalFilename', u'SIRAJ-Educational-AI.exe'),
        StringStruct(u'ProductName', u'SIRAJ Educational AI'),
        StringStruct(u'ProductVersion', u'8.1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        version_file = self.project_root / 'siraj_version.txt'
        version_file.write_text(version_content.strip())
        logger.info(f"Created version file: {version_file}")
        
    def create_icon(self):
        """Create or copy icon file"""
        icon_file = self.project_root / 'siraj_icon.ico'
        
        if not icon_file.exists():
            logger.warning("Icon file not found. Creating placeholder...")
            # In a real scenario, you would have an actual icon file
            # For now, we'll just create an empty file as placeholder
            icon_file.touch()
            
    def build_executable(self):
        """Build the executable using PyInstaller"""
        logger.info("Building executable with PyInstaller...")
        
        # Create version file for Windows
        if self.platform == 'windows':
            self.create_version_file()
            
        # Create or verify icon
        self.create_icon()
        
        # Run PyInstaller
        cmd = [
            sys.executable,
            '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'siraj.spec'
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        subprocess.check_call(cmd, cwd=str(self.project_root))
        
        # Check if build was successful
        exe_name = 'SIRAJ-Educational-AI.exe' if self.platform == 'windows' else 'SIRAJ-Educational-AI'
        exe_path = self.dist_dir / exe_name
        
        if exe_path.exists():
            logger.info(f"✓ Executable created successfully: {exe_path}")
            logger.info(f"  Size: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
            return True
        else:
            logger.error("Failed to create executable!")
            return False
            
    def create_distribution(self):
        """Create final distribution package"""
        logger.info("Creating distribution package...")
        
        # Create distribution directory
        dist_package = self.dist_dir / 'SIRAJ-Educational-AI-Package'
        dist_package.mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        exe_name = 'SIRAJ-Educational-AI.exe' if self.platform == 'windows' else 'SIRAJ-Educational-AI'
        exe_src = self.dist_dir / exe_name
        exe_dst = dist_package / exe_name
        
        if exe_src.exists():
            shutil.copy2(exe_src, exe_dst)
            
        # Copy supporting files
        files_to_copy = [
            '.env.example',
            'README.md',
            'PROJECT_COMPLETE.md',
            'LICENSE'
        ]
        
        for file_name in files_to_copy:
            src = self.project_root / file_name
            if src.exists():
                shutil.copy2(src, dist_package / file_name)
                
        # Create startup script
        if self.platform == 'windows':
            startup_script = dist_package / 'START-SIRAJ.bat'
            startup_script.write_text(
                '@echo off\n'
                'echo Starting SIRAJ Educational AI...\n'
                'SIRAJ-Educational-AI.exe\n'
                'pause\n'
            )
        else:
            startup_script = dist_package / 'START-SIRAJ.sh'
            startup_script.write_text(
                '#!/bin/bash\n'
                'echo "Starting SIRAJ Educational AI..."\n'
                './SIRAJ-Educational-AI\n'
            )
            startup_script.chmod(0o755)
            
        # Create README for distribution
        dist_readme = dist_package / 'QUICK-START.txt'
        dist_readme.write_text("""
SIRAJ Educational AI - Quick Start Guide
========================================

Thank you for downloading SIRAJ Educational AI!

REQUIREMENTS:
1. Ollama must be installed: https://ollama.ai
2. Internet connection for first-time model download

TO START:
- Windows: Double-click START-SIRAJ.bat
- Mac/Linux: Run ./START-SIRAJ.sh

FIRST TIME SETUP:
1. The application will automatically download required AI models
2. This may take 10-15 minutes depending on your internet speed
3. Once started, your browser will open to http://localhost:3000

TROUBLESHOOTING:
- If Ollama is not found, install from https://ollama.ai
- If port 8000 or 3000 is in use, edit the .env file
- Check the console output for error messages

For full documentation, see README.md

Enjoy your AI-powered educational journey!
""")
        
        # Zip the distribution
        logger.info("Creating distribution archive...")
        archive_name = f'SIRAJ-Educational-AI-{self.platform}-v8.1.0'
        shutil.make_archive(
            str(self.dist_dir / archive_name),
            'zip',
            str(dist_package.parent),
            dist_package.name
        )
        
        logger.info(f"✓ Distribution package created: {archive_name}.zip")
        
    def build(self):
        """Run the complete build process"""
        logger.info("=" * 60)
        logger.info("SIRAJ Educational AI - Build Process")
        logger.info(f"Platform: {self.platform}")
        logger.info("=" * 60)
        
        try:
            # Step 1: Clean
            self.clean()
            
            # Step 2: Install dependencies
            self.install_dependencies()
            
            # Step 3: Build frontend
            if not self.build_frontend():
                logger.error("Frontend build failed!")
                return False
                
            # Step 4: Build executable
            if not self.build_executable():
                logger.error("Executable build failed!")
                return False
                
            # Step 5: Create distribution
            self.create_distribution()
            
            logger.info("=" * 60)
            logger.info("✓ Build completed successfully!")
            logger.info(f"✓ Distribution package: dist/SIRAJ-Educational-AI-{self.platform}-v8.1.0.zip")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"Build failed: {e}")
            return False

def main():
    """Main entry point"""
    builder = SIRAJBuilder()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'clean':
            builder.clean()
        elif sys.argv[1] == 'frontend':
            builder.build_frontend()
        elif sys.argv[1] == 'exe':
            builder.build_executable()
        else:
            logger.error(f"Unknown command: {sys.argv[1]}")
            logger.info("Usage: python build_exe.py [clean|frontend|exe]")
            sys.exit(1)
    else:
        # Run full build
        success = builder.build()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
