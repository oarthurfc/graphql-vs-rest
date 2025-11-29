# Lab05S01 - Desenho e Preparação do Experimento
## GraphQL vs REST: Experimento Controlado

---

## 1. DESENHO DO EXPERIMENTO

### A. Hipóteses Nula e Alternativa

#### Para RQ1: Tempo de Resposta

**H0₁ (Hipótese Nula):** Não há diferença estatisticamente significativa entre o tempo de resposta de consultas GraphQL e REST.

**H1₁ (Hipótese Alternativa):** Consultas GraphQL apresentam tempo de resposta estatisticamente menor que consultas REST.

#### Para RQ2: Tamanho da Resposta

**H0₂ (Hipótese Nula):** Não há diferença estatisticamente significativa entre o tamanho das respostas de consultas GraphQL e REST.

**H1₂ (Hipótese Alternativa):** Respostas de consultas GraphQL apresentam tamanho estatisticamente menor que respostas REST.

---

### B. Variáveis Dependentes

As variáveis dependentes são aquelas que serão medidas durante o experimento:

1. **Tempo de Resposta (ms):** Tempo decorrido entre o envio da requisição e o recebimento completo da resposta
   - Medido em milissegundos
   - Precisão de até 2 casas decimais

2. **Tamanho da Resposta (bytes):** Tamanho total do payload da resposta HTTP
   - Medido em bytes
   - Inclui cabeçalhos HTTP e corpo da resposta

---

### C. Variáveis Independentes

As variáveis independentes são aquelas que serão controladas/manipuladas:

1. **Tipo de API:** GraphQL ou REST (Fator Principal)
   - Níveis: GraphQL, REST

2. **Tipo de Consulta:** Complexidade e natureza da operação
   - Níveis: Simples (poucos campos), Média (múltiplos campos), Complexa (campos aninhados/relacionamentos)

3. **Quantidade de Dados Retornados:**
   - Níveis: Pequena (1-10 registros), Média (11-50 registros), Grande (51-100 registros)

---

### D. Tratamentos

Os tratamentos representam as combinações das variáveis independentes que serão aplicadas:

**Tratamento 1 (T1):** API REST com consulta simples e pequena quantidade de dados
**Tratamento 2 (T2):** API GraphQL com consulta simples e pequena quantidade de dados
**Tratamento 3 (T3):** API REST com consulta média e média quantidade de dados
**Tratamento 4 (T4):** API GraphQL com consulta média e média quantidade de dados
**Tratamento 5 (T5):** API REST com consulta complexa e grande quantidade de dados
**Tratamento 6 (T6):** API GraphQL com consulta complexa e grande quantidade de dados

---

### E. Objetos Experimentais

Os objetos experimentais são as APIs e consultas que serão utilizadas:

**APIs Públicas Selecionadas:**

1. **GitHub API** (REST: v3, GraphQL: v4)
   - Endpoint REST: `https://api.github.com/`
   - Endpoint GraphQL: `https://api.github.com/graphql`
   - Domínio: Repositórios, usuários, issues

**Consultas Planejadas:**

**Consulta Simples:**
- REST: Buscar informações básicas de um único recurso (ex: um usuário)
- GraphQL: Buscar os mesmos campos específicos do recurso

**Consulta Média:**
- REST: Buscar lista de recursos com múltiplos campos (ex: 20 repositórios)
- GraphQL: Buscar a mesma lista selecionando apenas campos necessários

**Consulta Complexa:**
- REST: Buscar recurso com relacionamentos (múltiplas requisições ou over-fetching)
- GraphQL: Buscar recurso com relacionamentos aninhados em única query

---

### F. Tipo de Projeto Experimental

**Projeto Experimental:** Fatorial Completo 2×3

- **Fator 1:** Tipo de API (2 níveis: REST, GraphQL)
- **Fator 2:** Complexidade da Consulta (3 níveis: Simples, Média, Complexa)

**Justificativa:** Este design permite avaliar tanto o efeito principal de cada fator quanto possíveis interações entre eles.

**Abordagem:** Within-subjects (medidas repetidas)
- Cada combinação de fatores será testada múltiplas vezes
- Randomização da ordem de execução para evitar efeitos de ordem

---

### G. Quantidade de Medições

Para garantir significância estatística e confiabilidade:

**Repetições por Tratamento:** 30 execuções
- Total de medições: 6 tratamentos × 30 repetições = **180 medições**

**Aquecimento:** 5 requisições de aquecimento antes das medições (warm-up)

**Intervalo entre Requisições:** 1-2 segundos para evitar rate limiting

**Distribuição Temporal:**
- Execução distribuída ao longo de diferentes horários do dia
- Evitar horários de pico para minimizar variações de rede

---

### H. Ameaças à Validade

#### Validade Interna

1. **Latência de Rede**
   - *Ameaça:* Variações na latência de rede podem afetar o tempo de resposta
   - *Mitigação:* Executar testes em ambiente controlado com conexão estável; múltiplas medições; análise estatística com outliers

2. **Cache**
   - *Ameaça:* Respostas em cache podem distorcer resultados
   - *Mitigação:* Incluir headers para evitar cache; variar parâmetros das consultas

3. **Rate Limiting**
   - *Ameaça:* APIs podem limitar taxa de requisições
   - *Mitigação:* Intervalos entre requisições; usar tokens de autenticação; monitorar status codes

4. **Estado do Servidor**
   - *Ameaça:* Carga do servidor pode variar
   - *Mitigação:* Distribuir medições ao longo do tempo; randomizar ordem de execução

#### Validade Externa

1. **APIs Específicas**
   - *Ameaça:* Resultados podem ser específicos das APIs escolhidas
   - *Mitigação:* Utilizar múltiplas APIs de diferentes domínios

2. **Implementação das APIs**
   - *Ameaça:* Qualidade da implementação pode variar
   - *Mitigação:* Escolher APIs públicas bem estabelecidas e mantidas

3. **Tipos de Consulta**
   - *Ameaça:* Consultas podem não representar casos reais
   - *Mitigação:* Basear consultas em padrões de uso documentados

#### Validade de Construção

1. **Medição de Tempo**
   - *Ameaça:* Tempo de processamento local pode ser incluído
   - *Mitigação:* Medir apenas tempo de rede (início do request até fim do response)

2. **Medição de Tamanho**
   - *Ameaça:* Diferentes formatos de compressão
   - *Mitigação:* Medir tamanho bruto (sem compressão) e com compressão separadamente

#### Validade de Conclusão

1. **Tamanho da Amostra**
   - *Ameaça:* Amostra insuficiente pode levar a conclusões incorretas
   - *Mitigação:* 30 repetições por tratamento; análise de poder estatístico

2. **Violação de Premissas Estatísticas**
   - *Ameaça:* Testes paramétricos podem ser inadequados
   - *Mitigação:* Verificar normalidade e homogeneidade; usar testes não-paramétricos se necessário

---

## 2. PREPARAÇÃO DO EXPERIMENTO

### A. Ambiente Experimental

**Hardware:**
- Processador: [Especificar]
- Memória RAM: [Especificar]
- Conexão: [Especificar tipo e velocidade]

**Software:**
- Sistema Operacional: macOS
- Linguagem: Python 3.9+
- Bibliotecas principais:
  - `requests` - Requisições HTTP para REST
  - `gql` - Cliente GraphQL
  - `time` - Medição de tempo
  - `pandas` - Manipulação de dados
  - `numpy` - Análise numérica
  - `scipy` - Análise estatística

### B. Estrutura de Diretórios

```
graphql-vs-rest/
├── data/
│   ├── raw/                 # Dados brutos das medições
│   ├── processed/           # Dados processados
│   └── queries/             # Consultas REST e GraphQL
├── scripts/
│   ├── rest_client.py      # Cliente para APIs REST
│   ├── graphql_client.py   # Cliente para APIs GraphQL
│   ├── experiment.py       # Script principal do experimento
│   └── config.py           # Configurações
├── results/
│   ├── measurements.csv    # Resultados das medições
│   └── statistics.csv      # Análises estatísticas
├── docs/
│   └── Lab05S01_Desenho_e_Preparacao.md
└── requirements.txt        # Dependências Python
```

### C. Consultas Definidas

#### GitHub API

**Consulta Simples - Informações de Usuário**

REST:
```http
GET https://api.github.com/users/torvalds
```

GraphQL:
```graphql
query {
  user(login: "torvalds") {
    login
    name
    bio
    company
    location
  }
}
```

**Consulta Média - Lista de Repositórios**

REST:
```http
GET https://api.github.com/users/torvalds/repos?per_page=20
```

GraphQL:
```graphql
query {
  user(login: "torvalds") {
    repositories(first: 20) {
      nodes {
        name
        description
        stargazerCount
        forkCount
      }
    }
  }
}
```

**Consulta Complexa - Repositório com Issues e Commits**

REST (múltiplas requisições):
```http
GET https://api.github.com/repos/torvalds/linux
GET https://api.github.com/repos/torvalds/linux/issues?per_page=10
GET https://api.github.com/repos/torvalds/linux/commits?per_page=10
```

GraphQL (única requisição):
```graphql
query {
  repository(owner: "torvalds", name: "linux") {
    name
    description
    stargazerCount
    issues(first: 10) {
      nodes {
        title
        state
        createdAt
      }
    }
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 10) {
            nodes {
              message
              committedDate
              author {
                name
              }
            }
          }
        }
      }
    }
  }
}
```

### D. Scripts de Implementação

#### requirements.txt
```txt
requests>=2.31.0
gql>=3.4.1
requests-toolbelt>=1.0.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0
matplotlib>=3.7.0
seaborn>=0.12.0
python-dotenv>=1.0.0
```

#### config.py
```python
# Configurações do Experimento

# APIs
GITHUB_TOKEN = "seu_token_aqui"  # Obter em https://github.com/settings/tokens
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
    'Cache-Control': 'no-cache'
}
```

#### rest_client.py
```python
import requests
import time
import sys

class RESTClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
    
    def execute_query(self, endpoint, method='GET', params=None):
        """
        Executa uma consulta REST e retorna métricas
        """
        url = f"{self.base_url}/{endpoint}"
        
        start_time = time.perf_counter()
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=params)
            
            end_time = time.perf_counter()
            
            response.raise_for_status()
            
            # Métricas
            response_time = (end_time - start_time) * 1000  # converter para ms
            response_size = len(response.content)
            
            return {
                'success': True,
                'response_time': response_time,
                'response_size': response_size,
                'status_code': response.status_code,
                'data': response.json()
            }
        
        except Exception as e:
            end_time = time.perf_counter()
            return {
                'success': False,
                'response_time': (end_time - start_time) * 1000,
                'error': str(e)
            }
    
    def execute_multiple_queries(self, endpoints):
        """
        Executa múltiplas consultas REST (para consultas complexas)
        """
        total_time = 0
        total_size = 0
        results = []
        
        start_time = time.perf_counter()
        
        for endpoint in endpoints:
            result = self.execute_query(endpoint)
            if result['success']:
                total_size += result['response_size']
                results.append(result['data'])
            else:
                return result
        
        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000
        
        return {
            'success': True,
            'response_time': total_time,
            'response_size': total_size,
            'data': results
        }
```

#### graphql_client.py
```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import time

class GraphQLClient:
    def __init__(self, endpoint, headers):
        transport = RequestsHTTPTransport(
            url=endpoint,
            headers=headers,
            verify=True,
            retries=3,
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
    
    def execute_query(self, query_string):
        """
        Executa uma consulta GraphQL e retorna métricas
        """
        query = gql(query_string)
        
        start_time = time.perf_counter()
        
        try:
            result = self.client.execute(query)
            end_time = time.perf_counter()
            
            # Calcular tamanho da resposta
            import json
            response_size = len(json.dumps(result).encode('utf-8'))
            
            response_time = (end_time - start_time) * 1000  # converter para ms
            
            return {
                'success': True,
                'response_time': response_time,
                'response_size': response_size,
                'data': result
            }
        
        except Exception as e:
            end_time = time.perf_counter()
            return {
                'success': False,
                'response_time': (end_time - start_time) * 1000,
                'error': str(e)
            }
```

#### experiment.py
```python
import time
import random
import pandas as pd
from datetime import datetime
import config
from rest_client import RESTClient
from graphql_client import GraphQLClient

# Definição das consultas
QUERIES = {
    'simple_rest': 'users/torvalds',
    'simple_graphql': '''
        query {
          user(login: "torvalds") {
            login
            name
            bio
            company
            location
          }
        }
    ''',
    'medium_rest': 'users/torvalds/repos?per_page=20',
    'medium_graphql': '''
        query {
          user(login: "torvalds") {
            repositories(first: 20) {
              nodes {
                name
                description
                stargazerCount
                forkCount
              }
            }
          }
        }
    ''',
    'complex_rest': [
        'repos/torvalds/linux',
        'repos/torvalds/linux/issues?per_page=10',
        'repos/torvalds/linux/commits?per_page=10'
    ],
    'complex_graphql': '''
        query {
          repository(owner: "torvalds", name: "linux") {
            name
            description
            stargazerCount
            issues(first: 10) {
              nodes {
                title
                state
                createdAt
              }
            }
            defaultBranchRef {
              target {
                ... on Commit {
                  history(first: 10) {
                    nodes {
                      message
                      committedDate
                      author {
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
    '''
}

def warm_up(rest_client, graphql_client):
    """Executa requisições de aquecimento"""
    print("Executando warm-up...")
    for _ in range(config.WARMUP_REQUESTS):
        rest_client.execute_query(QUERIES['simple_rest'])
        time.sleep(0.5)
        graphql_client.execute_query(QUERIES['simple_graphql'])
        time.sleep(0.5)
    print("Warm-up concluído.\n")

def run_experiment():
    """Executa o experimento completo"""
    # Inicializar clientes
    rest_client = RESTClient(config.GITHUB_REST_URL, config.HEADERS_REST)
    graphql_client = GraphQLClient(config.GITHUB_GRAPHQL_URL, config.HEADERS_GRAPHQL)
    
    # Warm-up
    warm_up(rest_client, graphql_client)
    
    # Lista para armazenar resultados
    results = []
    
    # Criar lista de execuções e randomizar
    executions = []
    for treatment_id, treatment in config.TREATMENTS.items():
        for repetition in range(config.REPETITIONS):
            executions.append({
                'treatment_id': treatment_id,
                'treatment': treatment,
                'repetition': repetition
            })
    
    random.shuffle(executions)
    
    # Executar experimento
    total_executions = len(executions)
    for idx, execution in enumerate(executions, 1):
        treatment_id = execution['treatment_id']
        treatment = execution['treatment']
        repetition = execution['repetition']
        
        print(f"Execução {idx}/{total_executions}: {treatment_id} (Repetição {repetition + 1})")
        
        # Determinar qual consulta executar
        complexity = treatment['complexity']
        api_type = treatment['api']
        
        if api_type == 'REST':
            if complexity == 'complex':
                result = rest_client.execute_multiple_queries(QUERIES[f'{complexity}_rest'])
            else:
                result = rest_client.execute_query(QUERIES[f'{complexity}_rest'])
        else:  # GraphQL
            result = graphql_client.execute_query(QUERIES[f'{complexity}_graphql'])
        
        # Armazenar resultado
        if result['success']:
            results.append({
                'timestamp': datetime.now().isoformat(),
                'treatment_id': treatment_id,
                'api_type': api_type,
                'complexity': complexity,
                'repetition': repetition,
                'response_time_ms': result['response_time'],
                'response_size_bytes': result['response_size'],
                'success': True
            })
        else:
            results.append({
                'timestamp': datetime.now().isoformat(),
                'treatment_id': treatment_id,
                'api_type': api_type,
                'complexity': complexity,
                'repetition': repetition,
                'response_time_ms': result.get('response_time', None),
                'response_size_bytes': None,
                'success': False,
                'error': result.get('error', '')
            })
        
        # Intervalo entre requisições
        time.sleep(config.REQUEST_INTERVAL)
    
    # Salvar resultados
    df = pd.DataFrame(results)
    df.to_csv('results/measurements.csv', index=False)
    print(f"\nExperimento concluído! Resultados salvos em results/measurements.csv")
    print(f"Total de medições: {len(results)}")
    print(f"Medições bem-sucedidas: {df['success'].sum()}")
    print(f"Medições falhadas: {(~df['success']).sum()}")

if __name__ == '__main__':
    run_experiment()
```

### E. Checklist de Preparação

- [ ] Criar conta no GitHub e gerar token de acesso pessoal
- [ ] Criar estrutura de diretórios do projeto
- [ ] Instalar Python 3.9+ e dependências (`pip install -r requirements.txt`)
- [ ] Configurar token de API no arquivo `config.py`
- [ ] Testar conectividade com APIs REST e GraphQL
- [ ] Validar scripts individuais (`rest_client.py`, `graphql_client.py`)
- [ ] Executar teste piloto com 5 repetições
- [ ] Verificar formato e completude dos dados salvos
- [ ] Documentar configuração do ambiente (hardware, software, rede)
- [ ] Preparar ambiente estável para execução (fechar aplicações pesadas, conectar a rede estável)

### F. Cronograma de Execução

**Fase 1 - Preparação (1-2 dias):**
- Configuração do ambiente
- Implementação dos scripts
- Testes iniciais

**Fase 2 - Teste Piloto (1 dia):**
- Execução com 5 repetições
- Validação da coleta de dados
- Ajustes necessários

**Fase 3 - Execução Principal (2-3 dias):**
- Execução completa com 30 repetições
- Distribuída em diferentes horários
- Monitoramento contínuo

**Fase 4 - Validação (1 dia):**
- Verificação de dados faltantes
- Identificação de outliers
- Preparação para análise

---

## 3. MÉTRICAS DE AVALIAÇÃO

### Estatísticas Descritivas
Para cada tratamento, calcular:
- Média
- Mediana
- Desvio padrão
- Quartis (Q1, Q3)
- Mínimo e Máximo

### Testes Estatísticos Planejados

**Para RQ1 e RQ2:**

1. **Teste de Normalidade:** Shapiro-Wilk
2. **Teste de Homogeneidade de Variâncias:** Levene
3. **Teste de Hipótese:**
   - Se premissas atendidas: t-test pareado ou ANOVA
   - Se premissas violadas: Mann-Whitney U ou Kruskal-Wallis
4. **Tamanho de Efeito:** Cohen's d ou Cliff's Delta
5. **Nível de Significância:** α = 0.05

---

## 4. PRÓXIMOS PASSOS (Sprint 2)

1. Executar o experimento conforme planejado
2. Coletar e validar dados
3. Realizar análise estatística
4. Interpretar resultados
5. Elaborar relatório final

---

**Documento elaborado para Lab05S01**  
**Data:** Novembro 2025  
**Status:** Preparação Concluída ✓
