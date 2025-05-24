#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for Django
Run this script and copy the output to your .env file
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Generated SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")
    print(f"\nCopy the line above to your .env file")