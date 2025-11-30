# Configurações do Experimento
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# APIs
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "seu_token_aqui")  # Obter em https://github.com/settings/tokens
GITHUB_REST_URL = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Parâmetros do experimento
REPETITIONS = 30
WARMUP_REQUESTS = 5
REQUEST_INTERVAL = 1.5  # segundos

# Tratamentos
TREATMENTS = {
    'T1': {'api': 'REST', 'complexity': 'simple', 'size': 'small'},
    'T2': {'api': 'GraphQL', 'complexity': 'simple', 'size': 'small'},
    'T3': {'api': 'REST', 'complexity': 'medium', 'size': 'medium'},
    'T4': {'api': 'GraphQL', 'complexity': 'medium', 'size': 'medium'},
    'T5': {'api': 'REST', 'complexity': 'complex', 'size': 'large'},
    'T6': {'api': 'GraphQL', 'complexity': 'complex', 'size': 'large'},
}

# Headers
HEADERS_REST = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {GITHUB_TOKEN}',
    'Cache-Control': 'no-cache'
}

HEADERS_GRAPHQL = {
    'Authorization': f'bearer {GITHUB_TOKEN}',
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache'
}

