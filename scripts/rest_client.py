import requests
import time

class RESTClient:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
    
    def execute_query(self, endpoint, method='GET', params=None):
        """
        Executa uma consulta REST e retorna métricas
        
        Args:
            endpoint: Endpoint da API (ex: 'users/torvalds')
            method: Método HTTP ('GET' ou 'POST')
            params: Parâmetros da requisição
        
        Returns:
            dict: Dicionário com métricas e dados da resposta
        """
        # Remover barra inicial se existir
        endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        
        start_time = time.perf_counter()
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=params, timeout=30)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
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
        
        except requests.exceptions.RequestException as e:
            end_time = time.perf_counter()
            return {
                'success': False,
                'response_time': (end_time - start_time) * 1000,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
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
        
        Args:
            endpoints: Lista de endpoints a serem executados
        
        Returns:
            dict: Dicionário com métricas agregadas e dados das respostas
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

