import time
import random
import pandas as pd
import os
import sys
from datetime import datetime

# Adicionar o diretório scripts ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    for i in range(config.WARMUP_REQUESTS):
        print(f"  Warm-up {i+1}/{config.WARMUP_REQUESTS}...")
        rest_client.execute_query(QUERIES['simple_rest'])
        time.sleep(0.5)
        graphql_client.execute_query(QUERIES['simple_graphql'])
        time.sleep(0.5)
    print("Warm-up concluído.\n")

def run_experiment():
    """Executa o experimento completo"""
    # Verificar se o token está configurado
    if config.GITHUB_TOKEN == "seu_token_aqui" or not config.GITHUB_TOKEN:
        print("ERRO: Token do GitHub não configurado!")
        print("Configure a variável GITHUB_TOKEN no arquivo .env ou em config.py")
        print("Obtenha um token em: https://github.com/settings/tokens")
        return
    
    # Criar diretório results se não existir
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Inicializar clientes
    print("Inicializando clientes...")
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
    successful = 0
    failed = 0
    
    print(f"Iniciando experimento com {total_executions} execuções...\n")
    
    for idx, execution in enumerate(executions, 1):
        treatment_id = execution['treatment_id']
        treatment = execution['treatment']
        repetition = execution['repetition']
        
        print(f"Execução {idx}/{total_executions}: {treatment_id} (Repetição {repetition + 1})", end=" - ")
        
        # Determinar qual consulta executar
        complexity = treatment['complexity']
        api_type = treatment['api']
        
        try:
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
                    'size': treatment['size'],
                    'repetition': repetition + 1,
                    'response_time_ms': round(result['response_time'], 2),
                    'response_size_bytes': result['response_size'],
                    'success': True
                })
                successful += 1
                print(f"✓ {result['response_time']:.2f}ms, {result['response_size']} bytes")
            else:
                results.append({
                    'timestamp': datetime.now().isoformat(),
                    'treatment_id': treatment_id,
                    'api_type': api_type,
                    'complexity': complexity,
                    'size': treatment['size'],
                    'repetition': repetition + 1,
                    'response_time_ms': result.get('response_time', None),
                    'response_size_bytes': None,
                    'success': False,
                    'error': result.get('error', '')
                })
                failed += 1
                print(f"✗ Erro: {result.get('error', 'Erro desconhecido')[:50]}")
        
        except Exception as e:
            results.append({
                'timestamp': datetime.now().isoformat(),
                'treatment_id': treatment_id,
                'api_type': api_type,
                'complexity': complexity,
                'size': treatment['size'],
                'repetition': repetition + 1,
                'response_time_ms': None,
                'response_size_bytes': None,
                'success': False,
                'error': str(e)
            })
            failed += 1
            print(f"✗ Exceção: {str(e)[:50]}")
        
        # Intervalo entre requisições
        if idx < total_executions:
            time.sleep(config.REQUEST_INTERVAL)
    
    # Salvar resultados
    df = pd.DataFrame(results)
    output_file = os.path.join(results_dir, 'measurements.csv')
    df.to_csv(output_file, index=False)
    
    print(f"\n{'='*60}")
    print(f"Experimento concluído!")
    print(f"{'='*60}")
    print(f"Resultados salvos em: {output_file}")
    print(f"Total de medições: {len(results)}")
    print(f"Medições bem-sucedidas: {successful}")
    print(f"Medições falhadas: {failed}")
    print(f"Taxa de sucesso: {(successful/len(results)*100):.2f}%")
    
    # Estatísticas por tratamento
    if successful > 0:
        print(f"\nEstatísticas por tratamento (apenas sucessos):")
        print("-" * 60)
        for treatment_id in config.TREATMENTS.keys():
            treatment_data = df[(df['treatment_id'] == treatment_id) & (df['success'] == True)]
            if len(treatment_data) > 0:
                print(f"{treatment_id}:")
                print(f"  Média tempo: {treatment_data['response_time_ms'].mean():.2f} ms")
                print(f"  Média tamanho: {treatment_data['response_size_bytes'].mean():.0f} bytes")
                print(f"  Sucessos: {len(treatment_data)}/{config.REPETITIONS}")

if __name__ == '__main__':
    run_experiment()

