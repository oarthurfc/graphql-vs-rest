# Instruções de Instalação e Configuração

## Pré-requisitos

- Python 3.9 ou superior
- Conta no GitHub
- Token de acesso pessoal do GitHub

## Passo a Passo

### 1. Obter Token do GitHub

1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token" → "Generate new token (classic)"
3. Dê um nome descritivo (ex: "Lab05 GraphQL vs REST")
4. Selecione as permissões:
   - `public_repo` (para acessar repositórios públicos)
5. Clique em "Generate token"
6. **Copie o token imediatamente** (não será exibido novamente)

### 2. Configurar o Projeto

```bash
# 1. Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou no Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar token
# Criar arquivo .env na raiz do projeto
echo "GITHUB_TOKEN=seu_token_aqui" > .env

# Ou editar manualmente criando o arquivo .env com:
# GITHUB_TOKEN=ghp_seu_token_aqui
```

### 3. Testar Configuração

```bash
# Opção 1: Usar o script de teste (recomendado)
cd /home/kim/Repositories/graphql-vs-rest
source venv/bin/activate  # Ativar venv da raiz do projeto
cd scripts
python test_config.py

# Opção 2: Comando direto (sem ! para evitar problemas com bash)
cd /home/kim/Repositories/graphql-vs-rest
source venv/bin/activate
cd scripts
python -c "import config; token_ok = config.GITHUB_TOKEN != 'seu_token_aqui'; print('Token configurado' if token_ok else 'Token nao configurado')"
```

### 4. Executar Teste Piloto

Antes de executar o experimento completo, faça um teste piloto:

1. Edite `scripts/config.py` e altere temporariamente:
   ```python
   REPETITIONS = 5  # Em vez de 30
   ```

2. Execute o experimento:
   ```bash
   cd scripts
   python experiment.py
   ```

3. Verifique os resultados em `results/measurements.csv`

4. Se tudo estiver funcionando, altere `REPETITIONS` de volta para 30

### 5. Executar Experimento Completo

```bash
cd scripts
python experiment.py
```

O experimento levará aproximadamente:
- 180 execuções × 1.5 segundos de intervalo = ~270 segundos (4.5 minutos)
- Mais tempo de processamento e warm-up = ~5-10 minutos no total

## Estrutura de Arquivos

Após a execução, você terá:

```
graphql-vs-rest/
├── results/
│   └── measurements.csv    # Dados brutos das medições
├── scripts/
│   ├── config.py
│   ├── rest_client.py
│   ├── graphql_client.py
│   └── experiment.py
└── .env                     # Seu token (não commitar!)
```

## Solução de Problemas

### Erro: "Token do GitHub não configurado"
- Verifique se o arquivo `.env` existe na raiz do projeto
- Verifique se contém `GITHUB_TOKEN=seu_token_aqui`
- Certifique-se de que o token está correto e válido

### Erro: "Rate limit exceeded"
- O GitHub limita requisições por hora
- Aguarde 1 hora ou use um token com mais permissões
- Verifique seus limites em: https://api.github.com/rate_limit

### Erro: "Connection timeout"
- Verifique sua conexão com a internet
- Tente novamente após alguns minutos
- O script já tem retry automático configurado

