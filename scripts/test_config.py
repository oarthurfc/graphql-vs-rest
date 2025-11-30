#!/usr/bin/env python3
"""Script para testar se o token do GitHub está configurado"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import config
    
    if config.GITHUB_TOKEN and config.GITHUB_TOKEN != "seu_token_aqui":
        print("✓ Token configurado!")
        print(f"  Token: {config.GITHUB_TOKEN[:10]}... (primeiros 10 caracteres)")
    else:
        print("✗ Token NÃO configurado!")
        print("  Crie um arquivo .env na raiz do projeto com:")
        print("  GITHUB_TOKEN=seu_token_github_aqui")
        sys.exit(1)
except Exception as e:
    print(f"✗ Erro ao importar config: {e}")
    sys.exit(1)

