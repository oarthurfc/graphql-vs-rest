# Análise Estatística dos Resultados
## Experimento GraphQL vs REST

**Data da Análise:** 30 de Novembro de 2025  
**Total de Medições:** 180 (90 REST + 90 GraphQL)  
**Taxa de Sucesso:** 100%

---

## Resumo Executivo

### RQ1: Tempo de Resposta
**Resultado:** Não há diferença estatisticamente significativa (p = 0.4596)

- GraphQL é 25.2% mais rápido em média (597.15 ms vs 798.30 ms)
- **Mas:** A diferença não é estatisticamente significativa
- Tamanho de efeito: Médio (Cohen's d = -0.53)

### RQ2: Tamanho da Resposta
**Resultado:** GraphQL tem tamanho estatisticamente menor (p < 0.0001)

- GraphQL é 86.0% menor em média (4.47 KB vs 31.20 KB)
- **Diferença estatisticamente significativa**
- Tamanho de efeito: Grande (Cohen's d = -1.75)

---

## 1. RQ1: Tempo de Resposta

### Hipóteses
- **H₀:** Não há diferença estatisticamente significativa entre o tempo de resposta de consultas GraphQL e REST
- **H₁:** Consultas GraphQL apresentam tempo de resposta estatisticamente menor que consultas REST

### Estatísticas Descritivas

| API | N | Média (ms) | Mediana (ms) | DP (ms) | Mínimo (ms) | Máximo (ms) |
|-----|---|------------|--------------|---------|-------------|-------------|
| **REST** | 90 | 798.30 | 509.61 | 483.06 | 346.36 | 1982.10 |
| **GraphQL** | 90 | 597.15 | 545.65 | 245.12 | 361.14 | 2233.58 |

**Diferença percentual:** GraphQL é 25.2% mais rápido (média)

### Testes Estatísticos

#### Teste de Normalidade (Shapiro-Wilk)
- **REST:** p < 0.0001 → **Não normal**
- **GraphQL:** p < 0.0001 → **Não normal**

**Conclusão:** Dados não seguem distribuição normal → usar teste não-paramétrico

#### Teste de Homogeneidade de Variâncias (Levene)
- **Estatística:** 21.58
- **p-value:** < 0.0001
- **Conclusão:** Variâncias **não homogêneas**

#### Teste de Hipótese (Mann-Whitney U - unilateral)
- **Estatística:** 4014.0
- **p-value:** 0.4596
- **Significativo (α=0.05):** **NÃO**

**Conclusão:** Não rejeitamos H₀. Não há evidência estatística de que GraphQL seja mais rápido que REST.

#### Tamanho de Efeito (Cohen's d)
- **d = -0.53** (médio)
- **Interpretação:** Efeito médio, mas não estatisticamente significativo

---

## 2. RQ2: Tamanho da Resposta

### Hipóteses
- **H₀:** Não há diferença estatisticamente significativa entre o tamanho das respostas de consultas GraphQL e REST
- **H₁:** Respostas de consultas GraphQL apresentam tamanho estatisticamente menor que respostas REST

### Estatísticas Descritivas

| API | N | Média (bytes) | Média (KB) | Mediana (bytes) | DP (bytes) |
|-----|---|---------------|------------|-----------------|------------|
| **REST** | 90 | 31,953 | 31.20 | 46,555 | 21,860 |
| **GraphQL** | 90 | 4,467 | 4.36 | 3,203 | 4,179 |

**Diferença percentual:** GraphQL é 86.0% menor (média)

### Testes Estatísticos

#### Teste de Normalidade (Shapiro-Wilk)
- **REST:** p < 0.0001 → **Não normal**
- **GraphQL:** p < 0.0001 → **Não normal**

**Conclusão:** Dados não seguem distribuição normal → usar teste não-paramétrico

#### Teste de Homogeneidade de Variâncias (Levene)
- **Estatística:** 29.97
- **p-value:** < 0.0001
- **Conclusão:** Variâncias **não homogêneas**

#### Teste de Hipótese (Mann-Whitney U - unilateral)
- **Estatística:** 1800.0
- **p-value:** < 0.0001
- **Significativo (α=0.05):** **SIM**

**Conclusão:** Rejeitamos H₀. GraphQL tem tamanho estatisticamente menor que REST.

#### Tamanho de Efeito (Cohen's d)
- **d = -1.75** (grande)
- **Interpretação:** Efeito grande e estatisticamente significativo

---

## 3. Análise por Complexidade da Consulta

### Consultas Simples

| API | Média (ms) | N |
|-----|------------|---|
| REST | 464.66 | 30 |
| GraphQL | 440.69 | 30 |

- **Teste:** Mann-Whitney U
- **p-value:** 0.9313
- **Significativo:** **NÃO**
- **Cohen's d:** -0.17 (negligível)

**Conclusão:** Não há diferença significativa para consultas simples.

### Consultas Médias

| API | Média (ms) | N |
|-----|------------|---|
| REST | 485.72 | 30 |
| GraphQL | 805.94 | 30 |

- **Teste:** Mann-Whitney U
- **p-value:** 1.0000
- **Significativo:** **NÃO**
- **Cohen's d:** 1.43 (grande, mas não significativo)

**Conclusão:** Não há diferença significativa para consultas médias. REST parece mais rápido.

### Consultas Complexas

| API | Média (ms) | N |
|-----|------------|---|
| REST | 1444.51 | 30 |
| GraphQL | 544.82 | 30 |

- **Teste:** Mann-Whitney U
- **p-value:** < 0.0001
- **Significativo:** **SIM**
- **Cohen's d:** -6.39 (muito grande)

**Conclusão:** GraphQL é estatisticamente mais rápido para consultas complexas.

---

## 4. Interpretação dos Resultados

### RQ1: Tempo de Resposta

Embora GraphQL seja 25% mais rápido em média, a diferença **não é estatisticamente significativa** quando consideramos todas as consultas juntas. No entanto, quando analisamos por complexidade:

- **Consultas simples:** Sem diferença significativa
- **Consultas médias:** Sem diferença significativa (REST ligeiramente mais rápido)
- **Consultas complexas:** GraphQL é **significativamente mais rápido** (p < 0.0001)

A falta de significância na análise geral pode ser devido à alta variabilidade nos dados, especialmente nas consultas complexas REST, que têm tempos muito maiores.

### RQ2: Tamanho da Resposta

GraphQL apresenta tamanho **estatisticamente menor** que REST, com:
- Diferença de 86% em média
- Efeito grande (Cohen's d = -1.75)
- Significância estatística muito forte (p < 0.0001)

Este resultado é consistente e robusto, confirmando que GraphQL retorna respostas menores devido à capacidade de solicitar apenas os campos necessários.

---

## 5. Limitações e Considerações

1. **Normalidade:** Os dados não seguem distribuição normal, o que levou ao uso de testes não-paramétricos (Mann-Whitney U).

2. **Variabilidade:** REST apresenta maior variabilidade nos tempos de resposta, especialmente em consultas complexas.

3. **Outliers:** 2 outliers detectados em GraphQL, mas não afetaram significativamente os resultados.

4. **Contexto:** Os resultados são específicos para a API do GitHub e podem variar para outras APIs.

---

## 6. Conclusões Finais

### Resposta a RQ1
**Não há evidência estatística de que GraphQL seja mais rápido que REST quando consideramos todas as consultas juntas.** No entanto, para consultas complexas, GraphQL é significativamente mais rápido.

### Resposta a RQ2
**GraphQL tem tamanho estatisticamente menor que REST**, com diferença de 86% em média e efeito grande e significativo.

### Recomendações

1. **Para consultas simples e médias:** A escolha entre REST e GraphQL pode ser baseada em outros fatores (facilidade de uso, ferramentas disponíveis, etc.), pois não há diferença significativa de performance.

2. **Para consultas complexas:** GraphQL oferece vantagem clara em tempo de resposta, além de reduzir significativamente o tamanho das respostas.

3. **Economia de banda:** GraphQL é claramente superior em reduzir o tamanho das respostas, o que pode ser importante em ambientes com largura de banda limitada.

---

**Arquivos Gerados:**
- `results/statistics.json` - Resultados completos em JSON
- `results/statistics_summary.csv` - Resumo em CSV
- `docs/ANALISE_RESULTADOS.md` - Este documento

