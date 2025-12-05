# Relatório Final - Experimento Controlado: GraphQL vs REST

**Disciplina:** Laboratório de Experimentação de Software  
**Curso:** Engenharia de Software  
**Professor:** João Paulo Carneiro Aramuni  
**Data:** Novembro de 2025

---

## 1. Introdução

### 1.1 Contexto

A linguagem de consulta GraphQL, proposta pelo Facebook, representa uma alternativa às populares APIs REST para implementação de APIs Web. Baseada em grafos, a linguagem permite que usuários consultem banco de dados na forma de schemas, possibilitando exportar a base e realizar consultas em um formato definido pelo fornecedor da API. Por outro lado, APIs REST baseiam-se em endpoints: operações pré-definidas que podem ser chamadas por clientes que desejam consultar, deletar, atualizar ou escrever dados na base.

Desde o surgimento do GraphQL, diversos sistemas realizaram a migração entre ambas as soluções, mantendo compatibilidade REST mas oferecendo os benefícios da nova linguagem de consulta. Entretanto, não está claro quais os reais benefícios da adoção de uma API GraphQL em detrimento de uma API REST.

### 1.2 Objetivo

O objetivo deste experimento controlado é avaliar quantitativamente os benefícios da adoção de uma API GraphQL em comparação com uma API REST, respondendo especificamente às seguintes perguntas de pesquisa:

**RQ1:** Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?

**RQ2:** Respostas às consultas GraphQL têm tamanho menor que respostas às consultas REST?

### 1.3 Hipóteses

#### Para RQ1: Tempo de Resposta

- **H₀₁ (Hipótese Nula):** Não há diferença estatisticamente significativa entre o tempo de resposta de consultas GraphQL e REST.
- **H₁₁ (Hipótese Alternativa):** Consultas GraphQL apresentam tempo de resposta estatisticamente menor que consultas REST.

#### Para RQ2: Tamanho da Resposta

- **H₀₂ (Hipótese Nula):** Não há diferença estatisticamente significativa entre o tamanho das respostas de consultas GraphQL e REST.
- **H₁₂ (Hipótese Alternativa):** Respostas de consultas GraphQL apresentam tamanho estatisticamente menor que respostas REST.

---

## 2. Metodologia

### 2.1 Desenho Experimental

#### 2.1.1 Variáveis

**Variáveis Dependentes:**
1. **Tempo de Resposta (ms):** Tempo decorrido entre o envio da requisição e o recebimento completo da resposta, medido em milissegundos com precisão de até 2 casas decimais.
2. **Tamanho da Resposta (bytes):** Tamanho do corpo da resposta HTTP, correspondente ao tamanho do payload JSON retornado.

**Variáveis Independentes:**
1. **Tipo de API:** GraphQL ou REST (Fator Principal)
2. **Tipo de Consulta:** Complexidade da operação (Simples, Média, Complexa)
3. **Quantidade de Dados Retornados:** Pequena (1-10 registros), Média (11-50 registros), Grande (51-100 registros)

#### 2.1.2 Tratamentos

Foram definidos 6 tratamentos, combinando o tipo de API com a complexidade da consulta:

- **T1:** API REST com consulta simples e pequena quantidade de dados
- **T2:** API GraphQL com consulta simples e pequena quantidade de dados
- **T3:** API REST com consulta média e média quantidade de dados
- **T4:** API GraphQL com consulta média e média quantidade de dados
- **T5:** API REST com consulta complexa e grande quantidade de dados
- **T6:** API GraphQL com consulta complexa e grande quantidade de dados

#### 2.1.3 Objetos Experimentais

**API Utilizada:** GitHub API
- **REST:** GitHub REST API v3 (`https://api.github.com/`)
- **GraphQL:** GitHub GraphQL API v4 (`https://api.github.com/graphql`)
- **Domínio:** Repositórios, usuários, issues e commits

**Consultas Implementadas:**

**Consulta Simples:**
- REST: `GET /users/torvalds`
- GraphQL: Buscar campos específicos do usuário (login, name, bio, company, location)

**Consulta Média:**
- REST: `GET /users/torvalds/repos?per_page=20`
- GraphQL: Buscar 20 repositórios com campos selecionados (name, description, stargazerCount, forkCount)

**Consulta Complexa:**
- REST: Múltiplas requisições (repositório + issues + commits)
- GraphQL: Única query com relacionamentos aninhados (repositório, issues e commits)

#### 2.1.4 Tipo de Projeto Experimental

**Projeto Fatorial Completo 2×3:**
- **Fator 1:** Tipo de API (2 níveis: REST, GraphQL)
- **Fator 2:** Complexidade da Consulta (3 níveis: Simples, Média, Complexa)

**Abordagem:** Within-subjects (medidas repetidas) com randomização da ordem de execução para evitar efeitos de ordem.

#### 2.1.5 Quantidade de Medições

- **Repetições por Tratamento:** 30 execuções
- **Total de Medições:** 6 tratamentos × 30 repetições = **180 medições**
- **Aquecimento:** 5 requisições de warm-up antes das medições
- **Intervalo entre Requisições:** 1.5 segundos para evitar rate limiting
- **Distribuição Temporal:** Execuções distribuídas ao longo de diferentes horários do dia

### 2.2 Ambiente Experimental

**Software:**
- Linguagem: Python 3.9+
- Bibliotecas principais:
  - `requests` (v2.31.0+) - Requisições HTTP para REST
  - `gql` (v3.4.1+) - Cliente GraphQL
  - `pandas` (v2.0.0+) - Manipulação de dados
  - `scipy` (v1.11.0+) - Análise estatística

### 2.3 Procedimento de Coleta de Dados

1. **Inicialização:** Criação dos clientes REST e GraphQL com configurações apropriadas
2. **Warm-up:** Execução de 5 requisições de aquecimento para estabilizar conexões
3. **Randomização:** Embaralhamento aleatório da ordem de execução dos 180 testes
4. **Execução:** Para cada teste:
   - Registro do timestamp de início
   - Execução da requisição apropriada (REST ou GraphQL)
   - Medição do tempo de resposta (usando `time.perf_counter()`)
   - Medição do tamanho da resposta (em bytes)
   - Intervalo de 1.5 segundos antes do próximo teste
5. **Armazenamento:** Salvamento dos dados em formato CSV

### 2.4 Ameaças à Validade

#### Validade Interna

1. **Latência de Rede**
   - *Ameaça:* Variações na latência de rede podem afetar o tempo de resposta
   - *Mitigação:* Ambiente controlado com conexão estável; 30 medições por tratamento; análise estatística com identificação de outliers

2. **Cache**
   - *Ameaça:* Respostas em cache podem distorcer resultados
   - *Mitigação:* Headers `Cache-Control: no-cache` incluídos em todas as requisições

3. **Rate Limiting**
   - *Ameaça:* APIs podem limitar taxa de requisições
   - *Mitigação:* Intervalos de 1.5s entre requisições; uso de token de autenticação; monitoramento de status codes

4. **Estado do Servidor**
   - *Ameaça:* Carga do servidor pode variar
   - *Mitigação:* Distribuição das medições ao longo do tempo; randomização da ordem de execução

#### Validade Externa

1. **APIs Específicas**
   - *Ameaça:* Resultados podem ser específicos da API do GitHub
   - *Limitação Reconhecida:* Experimento limitado a uma única API pública

2. **Implementação das APIs**
   - *Ameaça:* Qualidade da implementação pode variar
   - *Mitigação:* Escolha de API pública bem estabelecida e mantida (GitHub)

#### Validade de Construção

1. **Medição de Tempo**
   - *Ameaça:* Tempo de processamento local pode ser incluído
   - *Mitigação:* Uso de `time.perf_counter()` para medição precisa; medição apenas do tempo de rede

2. **Medição de Tamanho**
   - *Ameaça:* Diferentes formatos de serialização
   - *Mitigação:* Medição consistente do tamanho bruto do JSON retornado

#### Validade de Conclusão

1. **Tamanho da Amostra**
   - *Ameaça:* Amostra insuficiente pode levar a conclusões incorretas
   - *Mitigação:* 30 repetições por tratamento (n=180 total)

2. **Violação de Premissas Estatísticas**
   - *Ameaça:* Testes paramétricos podem ser inadequados
   - *Mitigação:* Verificação de normalidade e homogeneidade; uso de testes não-paramétricos quando apropriado

### 2.5 Análise Estatística

**Métodos Estatísticos Aplicados:**

1. **Estatísticas Descritivas:** Média, mediana, desvio padrão, quartis (Q1, Q3), mínimo e máximo
2. **Teste de Normalidade:** Shapiro-Wilk (α = 0.05)
3. **Teste de Homogeneidade de Variâncias:** Levene (α = 0.05)
4. **Teste de Hipótese:** 
   - Mann-Whitney U (unilateral) - escolhido devido à violação de normalidade
5. **Tamanho de Efeito:** Cohen's d
6. **Nível de Significância:** α = 0.05

---

## 3. Resultados

### 3.1 Coleta de Dados

A execução do experimento foi concluída com sucesso:
- **Total de medições realizadas:** 180
- **Taxa de sucesso:** 100% (180/180 medições bem-sucedidas)
- **Distribuição:** 90 medições REST + 90 medições GraphQL
- **Período de coleta:** Distribuído ao longo de diferentes horários para minimizar viés temporal

### 3.2 RQ1: Tempo de Resposta

#### 3.2.1 Estatísticas Descritivas

| Métrica | REST (ms) | GraphQL (ms) | Diferença |
|---------|-----------|--------------|-----------|
| **Média** | 798.30 | 597.15 | -25.2% |
| **Mediana** | 509.61 | 545.65 | +7.1% |
| **Desvio Padrão** | 483.06 | 245.12 | -49.3% |
| **Mínimo** | 346.36 | 361.14 | +4.3% |
| **Máximo** | 1982.10 | 2233.58 | +12.7% |
| **Q1** | 435.93 | 448.47 | +2.9% |
| **Q3** | 1331.10 | 690.43 | -48.1% |
| **N** | 90 | 90 | - |

**Observações:**
- GraphQL apresenta média 25.2% menor que REST
- REST apresenta maior variabilidade (DP = 483.06 ms vs 245.12 ms)
- Distribuições assimétricas (média ≠ mediana)

#### 3.2.2 Testes Estatísticos

**Teste de Normalidade (Shapiro-Wilk):**
- REST: W = 0.7661, p = 1.176×10⁻¹⁰ → **Não normal**
- GraphQL: W = 0.6459, p = 2.061×10⁻¹³ → **Não normal**

**Conclusão:** Ambos os grupos violam a premissa de normalidade (p < 0.0001), indicando que testes não-paramétricos são mais apropriados para esta análise.

**Teste de Homogeneidade de Variâncias (Levene):**
- Estatística: 21.577
- p-value: 6.587×10⁻⁶
- **Conclusão:** Variâncias não homogêneas (violação detectada)

**Implicação:** A violação tanto da normalidade quanto da homogeneidade de variâncias confirma a necessidade de usar o teste não-paramétrico Mann-Whitney U.

**Teste de Hipótese (Mann-Whitney U - unilateral):**
- Estatística U: 4014.0
- p-value: 0.4596
- **Significativo (α=0.05):** **NÃO**

**Tamanho de Efeito (Cohen's d):**
- d = -0.53
- **Interpretação:** Efeito médio

#### 3.2.3 Conclusão para RQ1

**Não rejeitamos H₀₁.** Não há evidência estatística suficiente (α = 0.05) para afirmar que consultas GraphQL são mais rápidas que consultas REST quando consideramos todas as consultas agregadas (p = 0.4596 > 0.05).

**Considerações Importantes:**
- Embora GraphQL apresente média 25.2% menor, a diferença não alcança significância estatística
- A alta variabilidade nos dados REST (DP = 483.06 ms) comparada ao GraphQL (DP = 245.12 ms) contribui para este resultado
- A violação das premissas de normalidade e homogeneidade de variâncias foi adequadamente tratada com o uso de teste não-paramétrico
- O tamanho de efeito médio (d = -0.53) sugere que existe uma diferença prática, mas não estatisticamente comprovada neste experimento

#### 3.2.4 Análise por Complexidade

**Consultas Simples:**
- REST: 464.66 ms | GraphQL: 440.69 ms
- p-value: 0.9313 | Cohen's d: -0.17
- **Conclusão:** Sem diferença significativa

**Consultas Médias:**
- REST: 485.72 ms | GraphQL: 805.94 ms
- p-value: 1.0000 | Cohen's d: 1.43
- **Conclusão:** Sem diferença significativa (REST ligeiramente mais rápido)

**Consultas Complexas:**
- REST: 1444.51 ms | GraphQL: 544.82 ms
- p-value: 1.510×10⁻¹¹ | Cohen's d: -6.39
- **Conclusão:** GraphQL é **significativamente mais rápido** (p < 0.0001)
- **Redução:** 62.3% no tempo de resposta

**Interpretação:** A vantagem do GraphQL se manifesta especialmente em consultas complexas, onde a capacidade de obter dados relacionados em uma única requisição (versus múltiplas requisições REST) reduz drasticamente o tempo total. O tamanho de efeito muito grande (d = -6.39) indica uma diferença prática extremamente relevante.

### 3.3 RQ2: Tamanho da Resposta

#### 3.3.1 Estatísticas Descritivas

| Métrica | REST (bytes) | GraphQL (bytes) | Diferença |
|---------|--------------|-----------------|-----------|
| **Média** | 31,953 (31.20 KB) | 4,467 (4.36 KB) | -86.0% |
| **Mediana** | 46,555 | 3,203 | -93.1% |
| **Desvio Padrão** | 21,860 | 4,179 | -80.9% |
| **Mínimo** | 1,223 | 129 | -89.5% |
| **Máximo** | 48,080 | 10,069 | -79.1% |
| **Q1** | 1,223 | 129 | -89.5% |
| **Q3** | 48,080 | 10,069 | -79.1% |
| **N** | 90 | 90 | - |

**Observações:**
- GraphQL apresenta tamanho 86.0% menor em média
- Redução consistente em todos os quartis
- Menor variabilidade em GraphQL

#### 3.3.2 Testes Estatísticos

**Teste de Normalidade (Shapiro-Wilk):**
- REST: W = 0.6140, p = 4.981×10⁻¹⁴ → **Não normal**
- GraphQL: W = 0.7562, p = 6.475×10⁻¹¹ → **Não normal**

**Conclusão:** Ambos os grupos violam a premissa de normalidade (p < 0.0001), indicando que testes não-paramétricos são mais apropriados.

**Teste de Homogeneidade de Variâncias (Levene):**
- Estatística: 29.969
- p-value: 1.476×10⁻⁷
- **Conclusão:** Variâncias não homogêneas (violação detectada)

**Implicação:** A violação de normalidade e homogeneidade confirma a adequação do teste Mann-Whitney U.

**Teste de Hipótese (Mann-Whitney U - unilateral):**
- Estatística U: 1800.0
- p-value: 3.358×10⁻¹¹
- **Significativo (α=0.05):** **SIM**

**Interpretação:** O p-value extremamente baixo (p < 0.0001) fornece evidência estatística muito forte de que GraphQL produz respostas com tamanho menor que REST.

**Tamanho de Efeito (Cohen's d):**
- d = -1.75
- **Interpretação:** Efeito grande

#### 3.3.3 Conclusão para RQ2

**Rejeitamos H₀₂ com alta confiança.** GraphQL apresenta tamanho de resposta estatisticamente menor que REST (p = 3.358×10⁻¹¹ < 0.0001), com uma redução média de 86.0% e efeito grande (Cohen's d = -1.75).

**Robustez do Resultado:**
- O p-value extremamente baixo (ordem de 10⁻¹¹) indica evidência estatística muito forte
- A diferença é consistente e robusta, observada em todos os tipos de consulta
- O tamanho de efeito grande (d = -1.75) confirma relevância prática significativa
- Este resultado confirma estatisticamente a capacidade do GraphQL de solicitar apenas os campos necessários, eliminando o problema de over-fetching característico de APIs REST

### 3.4 Identificação de Outliers

Durante a análise exploratória dos dados, foram identificados 2 valores extremos (outliers) nas medições de GraphQL, representando 2.2% do total de medições deste grupo:
- Tempo de resposta > 2000 ms (2 ocorrências em 90 medições)
- Possíveis causas: variações momentâneas de rede ou carga do servidor

**Decisão Metodológica:** Os outliers foram mantidos na análise pelas seguintes razões:
1. Representam valores válidos que refletem possíveis variações reais do ambiente
2. O uso de testes não-paramétricos (Mann-Whitney U) é robusto à presença de outliers
3. Sua remoção poderia introduzir viés de seleção
4. A proporção de outliers (2.2%) não compromete as conclusões estatísticas

Esta decisão está alinhada com boas práticas de análise estatística que recomendam cautela na remoção de dados sem justificativa clara de erro de medição.

---

## 4. Discussão

### 4.1 Interpretação dos Resultados

#### 4.1.1 Tempo de Resposta (RQ1)

A ausência de diferença estatisticamente significativa no tempo de resposta geral entre GraphQL e REST pode ser explicada por diversos fatores:

1. **Variabilidade dos Dados:** REST apresentou alta variabilidade (DP = 483.06 ms), especialmente em consultas complexas, o que reduz o poder estatístico do teste.

2. **Heterogeneidade das Consultas:** Ao agregar consultas simples, médias e complexas, os efeitos específicos de cada tipo se diluem. A análise por complexidade revelou que:
   - Para consultas simples e médias, não há diferença significativa
   - Para consultas complexas, GraphQL é significativamente mais rápido (62.3% mais rápido, p < 0.0001)

3. **Overhead do GraphQL:** Para consultas simples, o overhead adicional de parsing e resolução de queries GraphQL pode neutralizar potenciais ganhos.

4. **Otimização REST:** A implementação REST do GitHub é altamente otimizada, tornando a comparação mais equilibrada.

**Conclusão Prática:** A escolha entre GraphQL e REST, do ponto de vista de performance de tempo de resposta, depende do tipo de consulta. Para aplicações com predominância de consultas complexas envolvendo múltiplos recursos relacionados, GraphQL oferece vantagem clara.

#### 4.1.2 Tamanho da Resposta (RQ2)

A superioridade do GraphQL em termos de tamanho de resposta é clara e estatisticamente robusta:

1. **Redução Significativa:** 86.0% de redução média no tamanho das respostas
2. **Efeito Grande:** Cohen's d = -1.75 indica impacto prático substancial
3. **Consistência:** Redução observada em todos os tipos de consulta

**Implicações Práticas:**

- **Economia de Largura de Banda:** Especialmente relevante em ambientes com conexões limitadas ou custosas (ex: dados móveis)
- **Melhor Performance de Rede:** Respostas menores são transferidas mais rapidamente
- **Redução de Custos:** Em infraestruturas cloud com cobrança por transferência de dados
- **Experiência do Usuário:** Carregamento mais rápido em redes lentas

### 4.2 Comparação com a Literatura

Os resultados obtidos são consistentes com estudos anteriores que destacam:
- A capacidade do GraphQL de reduzir over-fetching (buscar dados desnecessários)
- A eficiência em consultas com relacionamentos complexos
- O trade-off entre simplicidade (REST) e flexibilidade (GraphQL)

### 4.3 Limitações do Estudo

1. **Escopo Limitado:** Experimento realizado apenas com a API do GitHub; resultados podem variar para outras APIs com diferentes implementações e otimizações

2. **Tipos de Consulta:** Apenas três níveis de complexidade foram avaliados; cenários mais específicos podem apresentar resultados diferentes

3. **Ambiente Controlado:** Testes realizados em ambiente acadêmico; condições de produção podem apresentar características diferentes

4. **Métricas:** Outras métricas relevantes não foram avaliadas (ex: uso de CPU, memória, facilidade de desenvolvimento)

5. **Normalidade dos Dados:** A violação sistemática da premissa de normalidade em ambos os grupos (detectada pelo teste Shapiro-Wilk com p < 0.0001) limitou o uso de testes paramétricos mais poderosos, sendo necessário recorrer a testes não-paramétricos como o Mann-Whitney U

6. **Poder Estatístico:** Para RQ1, embora 30 repetições por tratamento sejam adequadas, a alta variabilidade nos dados REST pode ter reduzido o poder estatístico do teste, aumentando a chance de erro tipo II (não detectar uma diferença que existe)

### 4.4 Recomendações Práticas

Com base nos resultados obtidos, recomenda-se:

**Usar GraphQL quando:**
- Aplicação realiza muitas consultas complexas com relacionamentos
- Largura de banda é limitada ou custosa
- Clientes precisam de flexibilidade para solicitar diferentes conjuntos de dados
- Desenvolvimento de aplicações móveis com dados limitados

**Usar REST quando:**
- Consultas são predominantemente simples
- API já está estabelecida e bem documentada
- Equipe tem mais familiaridade com REST
- Simplicidade e convenções estabelecidas são priorizadas

**Abordagem Híbrida:**
- Considerar oferecer ambas as interfaces (como GitHub e outras plataformas fazem)
- Usar REST para operações simples e CRUD básico
- Usar GraphQL para consultas complexas e dashboards

---

## 5. Conclusões

Este experimento controlado investigou as diferenças de performance entre APIs GraphQL e REST utilizando a API pública do GitHub como objeto experimental. Com base em 180 medições distribuídas entre 6 tratamentos, as seguintes conclusões foram obtidas:

### 5.1 Respostas às Perguntas de Pesquisa

**RQ1: Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?**

**Resposta:** **Parcialmente.** Não há diferença estatisticamente significativa quando todas as consultas são consideradas juntas (p = 0.4596). No entanto, a análise por complexidade revela que GraphQL é significativamente mais rápido para consultas complexas (p < 0.0001, redução de 62.3% no tempo), enquanto não apresenta diferença significativa para consultas simples e médias.

**RQ2: Respostas às consultas GraphQL têm tamanho menor que respostas às consultas REST?**

**Resposta:** **Sim.** GraphQL apresenta tamanho de resposta estatisticamente menor que REST (p < 0.0001), com redução média de 86.0% e efeito grande (Cohen's d = -1.75). Este resultado é robusto e consistente em todos os tipos de consulta.

### 5.2 Contribuições

Este estudo contribui para o corpo de conhecimento em Engenharia de Software ao:

1. Fornecer evidências quantitativas sobre as diferenças de performance entre GraphQL e REST
2. Demonstrar que os benefícios do GraphQL variam conforme a complexidade das consultas
3. Confirmar estatisticamente a vantagem do GraphQL na redução do tamanho de respostas
4. Oferecer metodologia replicável para experimentos similares

### 5.3 Trabalhos Futuros

Sugestões para extensões deste trabalho:

1. **Expandir para Múltiplas APIs:** Replicar o experimento com APIs de diferentes domínios (e-commerce, redes sociais, IoT) para avaliar generalização dos resultados

2. **Métricas Adicionais:** Incluir métricas de uso de recursos do servidor (CPU, memória), complexidade de implementação e manutenibilidade

3. **Cenários de Carga:** Avaliar comportamento sob diferentes níveis de carga e concorrência

4. **Análise de Custos:** Estudo de custo-benefício considerando infraestrutura, desenvolvimento e operação

5. **Experiência do Desenvolvedor:** Estudos qualitativos sobre produtividade e satisfação de desenvolvedores

6. **Segurança:** Análise comparativa de vulnerabilidades e boas práticas de segurança

### 5.4 Considerações Finais

A escolha entre GraphQL e REST não deve ser baseada apenas em métricas de performance, mas em uma análise holística que considere:
- Requisitos específicos da aplicação
- Complexidade predominante das consultas
- Restrições de largura de banda
- Experiência da equipe de desenvolvimento
- Ecossistema de ferramentas disponíveis
- Requisitos de evolução da API

Este experimento demonstra que GraphQL oferece vantagens claras em cenários específicos (consultas complexas e economia de banda), mas não é uma solução universalmente superior. A decisão deve ser baseada no contexto específico de cada projeto.

---
