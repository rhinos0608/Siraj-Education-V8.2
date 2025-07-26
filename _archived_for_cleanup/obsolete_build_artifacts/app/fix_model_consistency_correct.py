#!/usr/bin/env python3
"""
SIRAJ Educational AI - Correct Model Consistency Fix
===================================================

Updates backend to use Gemma 3n models (the launcher is already correct)
"""

import os
import sys
from pathlib import Path

def fix_model_consistency_correct():
    """Fix model names - update backend to use Gemma 3n like the launcher"""
    
    project_root = Path(__file__).parent
    
    # Files to update (backend needs to match launcher)
    files_to_update = [
        project_root / "backend" / "main.py",
        project_root / "backend" / "backend_router.py"
    ]
    
    # Model fixes - update backend to use Gemma 3n
    model_fixes = {
        # Update backend to use Gemma 3n models
        'gemma2:9b-instruct-q4_k_m': 'gemma3n:e4b',
        'gemma2:2b-instruct-q4_k_m': 'gemma3n:e2b',
        'GEMMA_PRIMARY_MODEL = "gemma2:9b-instruct-q4_k_m"': 'GEMMA_PRIMARY_MODEL = "gemma3n:e4b"',
        'GEMMA_LIGHTWEIGHT_MODEL = "gemma2:2b-instruct-q4_k_m"': 'GEMMA_LIGHTWEIGHT_MODEL = "gemma3n:e2b"',
        '"gemma2:9b-instruct-q4_k_m"': '"gemma3n:e4b"',
        '"gemma2:2b-instruct-q4_k_m"': '"gemma3n:e2b"'
    }
    
    fixed_files = []
    
    for file_path in files_to_update:
        if file_path.exists():
            print(f"🔧 Updating {file_path.name} to use Gemma 3n models...")
            
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
                print(f"✅ Updated {file_path.name} to use Gemma 3n")
            else:
                print(f"ℹ️  No changes needed in {file_path.name}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n🎉 Model consistency fix complete!")
    print(f"✅ Backend now uses Gemma 3n models to match launcher")
    print(f"Fixed files: {', '.join(fixed_files) if fixed_files else 'None needed fixing'}")
    
    return fixed_files

if __name__ == "__main__":
    fix_model_consistency_correct()
