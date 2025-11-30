from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import time
import json

class GraphQLClient:
    def __init__(self, endpoint, headers):
        """
        Inicializa o cliente GraphQL
        
        Args:
            endpoint: URL do endpoint GraphQL
            headers: Headers HTTP para autenticação
        """
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
        
        Args:
            query_string: String contendo a query GraphQL
        
        Returns:
            dict: Dicionário com métricas e dados da resposta
        """
        query = gql(query_string)
        
        start_time = time.perf_counter()
        
        try:
            result = self.client.execute(query)
            end_time = time.perf_counter()
            
            # Calcular tamanho da resposta
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

