# Status do Experimento - Lab05S02

## ✅ Verificação Completa

### 1. Dados Coletados - SUFICIENTES ✅

**Resumo dos Dados:**
- **Total de medições:** 180 (6 tratamentos × 30 repetições)
- **Taxa de sucesso:** 100% (180/180)
- **Distribuição:**
  - REST: 90 medições
  - GraphQL: 90 medições
  - Cada tratamento: 30 medições

**Dados necessários para RQ1 e RQ2:**
- ✅ `response_time_ms` - Para responder RQ1
- ✅ `response_size_bytes` - Para responder RQ2
- ✅ `api_type` - Para comparar REST vs GraphQL
- ✅ `treatment_id` - Para análise por tratamento
- ✅ `complexity` - Para análise por complexidade

**Conclusão:** Os dados são **SUFICIENTES** para responder às perguntas de pesquisa.

---

### 2. Tópicos A-G no README - TODOS DEFINIDOS ✅

| Tópico | Status | Localização no README |
|--------|--------|----------------------|
| **A. Hipóteses Nula e Alternativa** | ✅ Completo | Linhas 8-20 |
| **B. Variáveis Dependentes** | ✅ Completo | Linhas 24-36 |
| **C. Variáveis Independentes** | ✅ Completo | Linhas 40-51 |
| **D. Tratamentos** | ✅ Completo | Linhas 55-64 |
| **E. Objetos Experimentais** | ✅ Completo | Linhas 68-91 |
| **F. Tipo de Projeto Experimental** | ✅ Completo | Linhas 95-106 |
| **G. Quantidade de Medições** | ✅ Completo | Linhas 110-123 |
| **H. Ameaças à Validade** | ✅ Completo (extra) | Linhas 127-179 |

**Conclusão:** Todos os tópicos estão **COERENTEMENTE DEFINIDOS** no README.

---

### 3. Passos do Experimento - STATUS

#### ✅ Passo 2: Preparação do Experimento - COMPLETO

**O que foi feito:**
- ✅ Ambiente experimental documentado
- ✅ Estrutura de diretórios criada
- ✅ Scripts desenvolvidos (`rest_client.py`, `graphql_client.py`, `experiment.py`)
- ✅ Consultas definidas (simples, média, complexa)
- ✅ Bibliotecas escolhidas e instaladas
- ✅ Configurações definidas (`config.py`)
- ✅ Cenário experimental montado

**Localização no README:** Seção 2 (linhas 183-740)

---

#### ✅ Passo 3: Execução do Experimento - COMPLETO

**O que foi feito:**
- ✅ Experimento executado conforme planejado
- ✅ 180 medições realizadas (6 tratamentos × 30 repetições)
- ✅ Dados coletados e salvos em `results/measurements.csv`
- ✅ Taxa de sucesso: 100%
- ✅ Ordem randomizada (conforme planejado)

**Evidência:** Arquivo `results/measurements.csv` com 180 linhas de dados válidos

---

#### ✅ Passo 4: Análise de Resultados - COMPLETO

**O que foi feito:**

1. **Revisão dos valores obtidos:**
   - ✅ Validação básica: 180 medições, todas bem-sucedidas
   - ✅ Identificação de outliers: 2 outliers detectados em GraphQL (analisados)
   - ✅ Verificação de valores: Análise detalhada completa

2. **Análise estatística formal:**
   - ✅ **Estatísticas descritivas** (média, mediana, desvio padrão, quartis)
   - ✅ **Teste de normalidade** (Shapiro-Wilk)
   - ✅ **Teste de homogeneidade de variâncias** (Levene)
   - ✅ **Teste de hipótese** (Mann-Whitney U - não-paramétrico)
   - ✅ **Tamanho de efeito** (Cohen's d)
   - ✅ **Análise por complexidade** (simples, média, complexa)

**Arquivos Gerados:**
- ✅ `scripts/analysis.py` - Script de análise estatística
- ✅ `results/statistics.json` - Resultados completos em JSON
- ✅ `results/statistics_summary.csv` - Resumo estatístico
- ✅ `docs/ANALISE_RESULTADOS.md` - Relatório completo da análise

**Resultados Principais:**
- **RQ1:** Não há diferença estatisticamente significativa (p = 0.4596), mas GraphQL é ~25% mais rápido em média. Para consultas complexas, GraphQL é significativamente mais rápido (p < 0.0001).
- **RQ2:** GraphQL tem tamanho estatisticamente menor (p < 0.0001), com diferença de 86% em média e efeito grande (Cohen's d = -1.75).

---

## 📊 Resumo dos Resultados (Análise Estatística Completa)

### RQ1: Tempo de Resposta

| API | Média (ms) | Mediana (ms) | Desvio Padrão (ms) |
|-----|------------|--------------|---------------------|
| REST | 798.30 | 509.61 | 483.06 |
| GraphQL | 597.15 | 545.65 | 245.12 |

**Teste Estatístico:** Mann-Whitney U (unilateral)  
**p-value:** 0.4596  
**Conclusão:** Não há diferença estatisticamente significativa (não rejeitamos H₀)  
**Tamanho de Efeito:** Cohen's d = -0.53 (médio)  
**Observação:** Para consultas complexas, GraphQL é significativamente mais rápido (p < 0.0001)

### RQ2: Tamanho da Resposta

| API | Média (bytes) | Mediana (bytes) | Desvio Padrão (bytes) |
|-----|---------------|----------------|----------------------|
| REST | 31,953 | 46,555 | 21,860 |
| GraphQL | 4,467 | 3,203 | 4,179 |

**Teste Estatístico:** Mann-Whitney U (unilateral)  
**p-value:** < 0.0001  
**Conclusão:** GraphQL tem tamanho estatisticamente menor (rejeitamos H₀)  
**Tamanho de Efeito:** Cohen's d = -1.75 (grande)

---

## 🎯 Próximos Passos

### ✅ Passo 4: Análise de Resultados - CONCLUÍDO

**Arquivos Criados:**
- ✅ `scripts/analysis.py` - Script completo de análise estatística
- ✅ `results/statistics.json` - Resultados completos em JSON
- ✅ `results/statistics_summary.csv` - Resumo estatístico
- ✅ `docs/ANALISE_RESULTADOS.md` - Relatório completo com interpretação

**Análise Realizada:**
- ✅ Estatísticas descritivas por tratamento e por API
- ✅ Testes de normalidade (Shapiro-Wilk) - Dados não normais
- ✅ Testes de homogeneidade (Levene) - Variâncias não homogêneas
- ✅ Testes de hipótese (Mann-Whitney U - não-paramétrico)
- ✅ Cálculo de tamanho de efeito (Cohen's d)
- ✅ Análise por complexidade (simples, média, complexa)
- ✅ Validação de dados e identificação de outliers

**Respostas às Perguntas de Pesquisa:**
- **RQ1:** Não há evidência estatística de que GraphQL seja mais rápido que REST quando consideramos todas as consultas juntas. No entanto, para consultas complexas, GraphQL é significativamente mais rápido.
- **RQ2:** GraphQL tem tamanho estatisticamente menor que REST, com diferença de 86% em média e efeito grande e significativo.

---

## ✅ Checklist Final

- [x] Passo 1: Desenho do Experimento (A-G)
- [x] Passo 2: Preparação do Experimento
- [x] Passo 3: Execução do Experimento
- [x] Passo 4: Análise de Resultados ✅ **CONCLUÍDO**
- [ ] Passo 5: Relatório Final ⚠️ **PENDENTE**
- [ ] Passo 6: Dashboard de Visualização (Lab05S03)

---

**Status Atual:** Análise estatística completa realizada. Resultados documentados em `docs/ANALISE_RESULTADOS.md`. Próximo passo: Elaborar relatório final (Passo 5).

