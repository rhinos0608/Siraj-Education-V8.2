#!/usr/bin/env python3
"""
SIRAJ Educational AI - Model Consistency Fix
============================================

This script aligns model names between launcher and backend
"""

import os
import sys
from pathlib import Path

def fix_model_consistency():
    """Fix model name consistency across the project"""
    
    project_root = Path(__file__).parent
    
    # Files to update
    files_to_update = [
        project_root / "launcher.py",
        project_root / "backend" / "main.py",
        project_root / "backend" / "backend_router.py"
    ]
    
    # Model mapping
    model_fixes = {
        # Standardize on gemma2 (more stable/available)
        "gemma3n:e2b": "gemma2:2b-instruct-q4_k_m",
        "gemma3n:e4b": "gemma2:9b-instruct-q4_k_m",
        "GEMMA_PRIMARY_MODEL": '"gemma2:9b-instruct-q4_k_m"',
        "GEMMA_LIGHTWEIGHT_MODEL": '"gemma2:2b-instruct-q4_k_m"'
    }
    
    fixed_files = []
    
    for file_path in files_to_update:
        if file_path.exists():
            print(f"🔧 Fixing model names in {file_path.name}...")
            
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply fixes
            original_content = content
            for old_model, new_model in model_fixes.items():
                content = content.replace(old_model, new_model)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path.name)
                print(f"✅ Updated {file_path.name}")
            else:
                print(f"ℹ️  No changes needed in {file_path.name}")
    
    print(f"\n🎉 Model consistency fix complete!")
    print(f"Fixed files: {', '.join(fixed_files) if fixed_files else 'None needed fixing'}")
    
    return fixed_files

if __name__ == "__main__":
    fix_model_consistency()
