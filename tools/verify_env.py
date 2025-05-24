#!/usr/bin/env python3
"""
Verify .env file configuration
Run this before starting Docker containers
"""

import os
from pathlib import Path

def load_env_file():
    """Load and parse .env file"""
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found!")
        return None
    
    env_vars = {}
    with open(env_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

def verify_configuration():
    """Verify all required environment variables"""
    env_vars = load_env_file()
    if not env_vars:
        return False
    
    required_vars = [
        'SECRET_KEY', 'DEBUG', 'DB_NAME', 'DB_USER', 
        'DB_PASSWORD', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD'
    ]
    
    print("🔍 Verifying .env configuration...\n")
    
    all_good = True
    for var in required_vars:
        if var in env_vars:
            value = env_vars[var]
            if var == 'SECRET_KEY':
                if len(value) >= 50:
                    print(f"✅ {var}: Good length ({len(value)} chars)")
                else:
                    print(f"⚠️  {var}: Too short ({len(value)} chars, recommend 50+)")
            elif var == 'DB_PASSWORD' or var == 'POSTGRES_PASSWORD':
                if len(value) >= 8:
                    print(f"✅ {var}: Good length")
                else:
                    print(f"❌ {var}: Too short (minimum 8 chars)")
                    all_good = False
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Missing!")
            all_good = False
    
    # Check matching database credentials
    if env_vars.get('DB_NAME') != env_vars.get('POSTGRES_DB'):
        print("⚠️  DB_NAME and POSTGRES_DB should match")
    if env_vars.get('DB_USER') != env_vars.get('POSTGRES_USER'):
        print("⚠️  DB_USER and POSTGRES_USER should match")
    if env_vars.get('DB_PASSWORD') != env_vars.get('POSTGRES_PASSWORD'):
        print("⚠️  DB_PASSWORD and POSTGRES_PASSWORD should match")
    
    print(f"\n{'✅ Configuration looks good!' if all_good else '❌ Please fix the issues above'}")
    return all_good

if __name__ == "__main__":
    verify_configuration()