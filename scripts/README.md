# Scripts do Experimento GraphQL vs REST

Este diretório contém todos os scripts necessários para executar o experimento controlado comparando APIs GraphQL e REST.

## 📁 Arquivos

- **`config.py`**: Configurações do experimento (token, repetições, tratamentos)
- **`rest_client.py`**: Cliente para fazer requisições REST à API do GitHub
- **`graphql_client.py`**: Cliente para fazer requisições GraphQL à API do GitHub
- **`experiment.py`**: Script principal que executa todo o experimento
- **`test_config.py`**: Script auxiliar para testar se o token está configurado

## 🚀 Como Executar

### Pré-requisitos

1. **Ambiente virtual ativado** (venv)
2. **Token do GitHub configurado** no arquivo `.env` na raiz do projeto
3. **Dependências instaladas** (`pip install -r requirements.txt`)

### Executar o Experimento

```bash
# 1. Ativar o ambiente virtual na pasta raiz de graphql-vs-rest(se ainda não estiver ativo)
source venv/bin/activate

# 2. Ir para a pasta scripts
cd scripts

# 3. Executar o experimento
python experiment.py
```

### Testar Configuração

Antes de executar o experimento completo, você pode testar se o token está configurado:

```bash
python test_config.py
```

## ⚙️ Configurações

As configurações principais estão em `config.py`:

- **`REPETITIONS`**: Número de repetições por tratamento (padrão: 30)
- **`WARMUP_REQUESTS`**: Número de requisições de aquecimento (padrão: 5)
- **`REQUEST_INTERVAL`**: Intervalo entre requisições em segundos (padrão: 1.5)

### Teste Piloto

Para fazer um teste rápido antes do experimento completo, edite `config.py`:

```python
REPETITIONS = 5  # Em vez de 30
```

Depois execute normalmente. Isso fará apenas 30 medições (6 tratamentos × 5 repetições) em vez de 180.

## 📊 Resultados

Após a execução, os resultados serão salvos em:

```
../results/measurements.csv
```

O arquivo CSV contém as seguintes colunas:
- `timestamp`: Data e hora da medição
- `treatment_id`: ID do tratamento (T1 a T6)
- `api_type`: Tipo de API (REST ou GraphQL)
- `complexity`: Complexidade da consulta (simple, medium, complex)
- `size`: Tamanho dos dados (small, medium, large)
- `repetition`: Número da repetição (1 a 30)
- `response_time_ms`: Tempo de resposta em milissegundos
- `response_size_bytes`: Tamanho da resposta em bytes
- `success`: Se a requisição foi bem-sucedida (True/False)
- `error`: Mensagem de erro (se houver)

## 🔍 Tratamentos

O experimento executa 6 tratamentos:

- **T1**: REST + Consulta Simples + Dados Pequenos
- **T2**: GraphQL + Consulta Simples + Dados Pequenos
- **T3**: REST + Consulta Média + Dados Médios
- **T4**: GraphQL + Consulta Média + Dados Médios
- **T5**: REST + Consulta Complexa + Dados Grandes
- **T6**: GraphQL + Consulta Complexa + Dados Grandes

Cada tratamento é executado 30 vezes (total: 180 medições).

## ⏱️ Tempo Estimado

- **Warm-up**: ~5 segundos (5 requisições)
- **Execução**: ~4.5 minutos (180 execuções × 1.5s intervalo)
- **Total**: ~5-10 minutos (incluindo processamento)

## 🐛 Solução de Problemas

### Erro: "Token do GitHub não configurado"

1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Verifique se contém: `GITHUB_TOKEN=seu_token_aqui`
3. Execute `python test_config.py` para verificar

### Erro: "ModuleNotFoundError"

Certifique-se de que:
1. O ambiente virtual está ativado (`source venv/bin/activate`)
2. As dependências estão instaladas (`pip install -r requirements.txt`)

### Erro: "Rate limit exceeded"

O GitHub limita requisições por hora. Aguarde 1 hora ou verifique seus limites em:
https://api.github.com/rate_limit

## 📝 Notas

- O script randomiza a ordem de execução dos tratamentos para evitar viés
- Requisições falhadas são registradas no CSV com `success=False`
- O script mostra estatísticas resumidas ao final da execução

