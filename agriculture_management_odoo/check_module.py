#!/usr/bin/env python3
"""
Odoo modül kontrolü için basit script
"""

import os
import sys

def check_module():
    print("=== Odoo Agriculture Management Module Kontrolü ===")
    
    # 1. Temel dosyaların varlığını kontrol et
    required_files = ['__manifest__.py', '__init__.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} mevcut")
        else:
            print(f"✗ {file} eksik!")
            
    # 2. Manifest dosyasını kontrol et
    try:
        with open('__manifest__.py', 'r', encoding='utf-8') as f:
            manifest_content = f.read()
            if "'name'" in manifest_content and "'version'" in manifest_content:
                print("✓ __manifest__.py formatı doğru görünüyor")
            else:
                print("✗ __manifest__.py'de gerekli alanlar eksik")
    except Exception as e:
        print(f"✗ __manifest__.py okunamadı: {e}")
    
    # 3. Models dizinini kontrol et
    if os.path.exists('models') and os.path.exists('models/__init__.py'):
        print("✓ Models dizini ve __init__.py mevcut")
        model_files = [f for f in os.listdir('models') if f.endswith('.py') and f != '__init__.py']
        print(f"  - {len(model_files)} model dosyası bulundu")
    else:
        print("✗ Models dizini veya __init__.py eksik")
    
    # 4. Views dizinini kontrol et
    if os.path.exists('views'):
        view_files = [f for f in os.listdir('views') if f.endswith('.xml')]
        print(f"✓ Views dizini mevcut - {len(view_files)} view dosyası bulundu")
    else:
        print("✗ Views dizini eksik")
    
    # 5. Security dosyalarını kontrol et
    if os.path.exists('security/ir.model.access.csv'):
        print("✓ Security dosyası mevcut")
    else:
        print("✗ Security dosyası eksik")

if __name__ == "__main__":
    check_module()
