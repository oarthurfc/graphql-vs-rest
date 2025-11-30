#!/usr/bin/env python3
"""
Análise Estatística do Experimento GraphQL vs REST

Este script realiza a análise estatística completa dos dados coletados,
incluindo testes de normalidade, homogeneidade de variâncias, testes de
hipótese e cálculo de tamanho de efeito.
"""

import pandas as pd
import numpy as np
import os
import sys
from scipy import stats
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu, f_oneway, kruskal
import json
from datetime import datetime

# Adicionar o diretório scripts ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_data():
    """Carrega os dados do experimento"""
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    data_file = os.path.join(results_dir, 'measurements.csv')
    
    if not os.path.exists(data_file):
        print(f"ERRO: Arquivo {data_file} não encontrado!")
        sys.exit(1)
    
    df = pd.read_csv(data_file)
    print(f"✓ Dados carregados: {len(df)} medições")
    return df

def descriptive_statistics(df, variable, group_by='api_type'):
    """Calcula estatísticas descritivas"""
    stats_dict = {}
    
    for group in df[group_by].unique():
        data = df[df[group_by] == group][variable].dropna()
        stats_dict[group] = {
            'n': len(data),
            'mean': data.mean(),
            'median': data.median(),
            'std': data.std(),
            'min': data.min(),
            'max': data.max(),
            'q1': data.quantile(0.25),
            'q3': data.quantile(0.75),
            'iqr': data.quantile(0.75) - data.quantile(0.25)
        }
    
    return stats_dict

def test_normality(data, alpha=0.05):
    """Teste de normalidade Shapiro-Wilk"""
    if len(data) < 3:
        return {'statistic': None, 'pvalue': None, 'normal': None, 'note': 'Amostra muito pequena'}
    
    # Limitar a 5000 amostras (limite do Shapiro-Wilk)
    if len(data) > 5000:
        data_sample = data.sample(5000, random_state=42)
    else:
        data_sample = data
    
    stat, pvalue = shapiro(data_sample)
    is_normal = pvalue > alpha
    
    return {
        'statistic': stat,
        'pvalue': pvalue,
        'normal': is_normal,
        'alpha': alpha
    }

def test_homogeneity(df, variable, group_by='api_type', alpha=0.05):
    """Teste de homogeneidade de variâncias (Levene)"""
    groups = [df[df[group_by] == group][variable].dropna() for group in df[group_by].unique()]
    
    if len(groups) < 2:
        return {'statistic': None, 'pvalue': None, 'homogeneous': None}
    
    stat, pvalue = levene(*groups)
    is_homogeneous = pvalue > alpha
    
    return {
        'statistic': stat,
        'pvalue': pvalue,
        'homogeneous': is_homogeneous,
        'alpha': alpha
    }

def cohens_d(group1, group2):
    """Calcula o tamanho de efeito Cohen's d"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    
    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return 0
    
    d = (group1.mean() - group2.mean()) / pooled_std
    
    # Interpretação
    if abs(d) < 0.2:
        interpretation = 'negligível'
    elif abs(d) < 0.5:
        interpretation = 'pequeno'
    elif abs(d) < 0.8:
        interpretation = 'médio'
    else:
        interpretation = 'grande'
    
    return {
        'd': d,
        'interpretation': interpretation,
        'magnitude': abs(d)
    }

def analyze_rq1(df):
    """Análise para RQ1: Tempo de Resposta"""
    print("\n" + "="*70)
    print("RQ1: Respostas às consultas GraphQL são mais rápidas que REST?")
    print("="*70)
    
    rest_time = df[df['api_type'] == 'REST']['response_time_ms'].dropna()
    graphql_time = df[df['api_type'] == 'GraphQL']['response_time_ms'].dropna()
    
    # Estatísticas descritivas
    print("\n📊 ESTATÍSTICAS DESCRITIVAS - Tempo de Resposta (ms)")
    print("-"*70)
    desc_stats = descriptive_statistics(df, 'response_time_ms', 'api_type')
    
    for api, stats in desc_stats.items():
        print(f"\n{api}:")
        print(f"  N: {stats['n']}")
        print(f"  Média: {stats['mean']:.2f} ms")
        print(f"  Mediana: {stats['median']:.2f} ms")
        print(f"  Desvio Padrão: {stats['std']:.2f} ms")
        print(f"  Mínimo: {stats['min']:.2f} ms")
        print(f"  Máximo: {stats['max']:.2f} ms")
        print(f"  Q1: {stats['q1']:.2f} ms")
        print(f"  Q3: {stats['q3']:.2f} ms")
        print(f"  IQR: {stats['iqr']:.2f} ms")
    
    # Diferença percentual
    diff_pct = ((rest_time.mean() - graphql_time.mean()) / rest_time.mean()) * 100
    print(f"\n📈 Diferença: GraphQL é {diff_pct:.1f}% mais rápido (média)")
    
    # Teste de normalidade
    print("\n🔍 TESTE DE NORMALIDADE (Shapiro-Wilk)")
    print("-"*70)
    rest_norm = test_normality(rest_time)
    graphql_norm = test_normality(graphql_time)
    
    print(f"\nREST:")
    print(f"  Estatística: {rest_norm['statistic']:.4f}" if rest_norm['statistic'] else "  N/A")
    print(f"  p-value: {rest_norm['pvalue']:.4f}" if rest_norm['pvalue'] else "  N/A")
    print(f"  Normal: {'Sim' if rest_norm['normal'] else 'Não' if rest_norm['normal'] is not None else 'N/A'}")
    
    print(f"\nGraphQL:")
    print(f"  Estatística: {graphql_norm['statistic']:.4f}" if graphql_norm['statistic'] else "  N/A")
    print(f"  p-value: {graphql_norm['pvalue']:.4f}" if graphql_norm['pvalue'] else "  N/A")
    print(f"  Normal: {'Sim' if graphql_norm['normal'] else 'Não' if graphql_norm['normal'] is not None else 'N/A'}")
    
    both_normal = rest_norm['normal'] and graphql_norm['normal']
    
    # Teste de homogeneidade de variâncias
    print("\n🔍 TESTE DE HOMOGENEIDADE DE VARIÂNCIAS (Levene)")
    print("-"*70)
    levene_result = test_homogeneity(df, 'response_time_ms', 'api_type')
    print(f"  Estatística: {levene_result['statistic']:.4f}" if levene_result['statistic'] else "  N/A")
    print(f"  p-value: {levene_result['pvalue']:.4f}" if levene_result['pvalue'] else "  N/A")
    print(f"  Variâncias homogêneas: {'Sim' if levene_result['homogeneous'] else 'Não' if levene_result['homogeneous'] is not None else 'N/A'}")
    
    # Teste de hipótese
    print("\n📊 TESTE DE HIPÓTESE")
    print("-"*70)
    print("H0: Não há diferença entre os tempos de resposta")
    print("H1: GraphQL é mais rápido que REST")
    
    if both_normal and levene_result['homogeneous']:
        # t-test
        stat, pvalue = ttest_ind(graphql_time, rest_time, alternative='less')
        test_name = "t-test (unilateral)"
        print(f"\n{test_name}:")
        print(f"  Estatística: {stat:.4f}")
        print(f"  p-value: {pvalue:.4f}")
        print(f"  Significativo (α=0.05): {'Sim' if pvalue < 0.05 else 'Não'}")
    else:
        # Mann-Whitney U (não-paramétrico)
        stat, pvalue = mannwhitneyu(graphql_time, rest_time, alternative='less')
        test_name = "Mann-Whitney U (unilateral)"
        print(f"\n{test_name}:")
        print(f"  Estatística: {stat:.4f}")
        print(f"  p-value: {pvalue:.4f}")
        print(f"  Significativo (α=0.05): {'Sim' if pvalue < 0.05 else 'Não'}")
    
    # Tamanho de efeito
    print("\n📏 TAMANHO DE EFEITO (Cohen's d)")
    print("-"*70)
    effect_size = cohens_d(graphql_time, rest_time)
    print(f"  Cohen's d: {effect_size['d']:.4f}")
    print(f"  Interpretação: {effect_size['interpretation']}")
    print(f"  Magnitude: {effect_size['magnitude']:.4f}")
    
    # Conclusão
    print("\n✅ CONCLUSÃO RQ1")
    print("-"*70)
    significant = pvalue < 0.05
    if significant:
        print(f"Rejeitamos H0. GraphQL é estatisticamente mais rápido que REST")
        print(f"(p = {pvalue:.4f}, d = {effect_size['d']:.4f})")
    else:
        print(f"Não rejeitamos H0. Não há evidência estatística de que GraphQL seja mais rápido")
        print(f"(p = {pvalue:.4f}, d = {effect_size['d']:.4f})")
    
    return {
        'descriptive': desc_stats,
        'normality': {'REST': rest_norm, 'GraphQL': graphql_norm},
        'homogeneity': levene_result,
        'test': {'name': test_name, 'statistic': stat, 'pvalue': pvalue, 'significant': significant},
        'effect_size': effect_size,
        'conclusion': 'GraphQL é mais rápido' if significant else 'Sem diferença significativa'
    }

def analyze_rq2(df):
    """Análise para RQ2: Tamanho da Resposta"""
    print("\n" + "="*70)
    print("RQ2: Respostas às consultas GraphQL têm tamanho menor que REST?")
    print("="*70)
    
    rest_size = df[df['api_type'] == 'REST']['response_size_bytes'].dropna()
    graphql_size = df[df['api_type'] == 'GraphQL']['response_size_bytes'].dropna()
    
    # Estatísticas descritivas
    print("\n📊 ESTATÍSTICAS DESCRITIVAS - Tamanho da Resposta (bytes)")
    print("-"*70)
    desc_stats = descriptive_statistics(df, 'response_size_bytes', 'api_type')
    
    for api, stats in desc_stats.items():
        print(f"\n{api}:")
        print(f"  N: {stats['n']}")
        print(f"  Média: {stats['mean']:.0f} bytes ({stats['mean']/1024:.2f} KB)")
        print(f"  Mediana: {stats['median']:.0f} bytes ({stats['median']/1024:.2f} KB)")
        print(f"  Desvio Padrão: {stats['std']:.0f} bytes")
        print(f"  Mínimo: {stats['min']:.0f} bytes")
        print(f"  Máximo: {stats['max']:.0f} bytes")
        print(f"  Q1: {stats['q1']:.0f} bytes")
        print(f"  Q3: {stats['q3']:.0f} bytes")
        print(f"  IQR: {stats['iqr']:.0f} bytes")
    
    # Diferença percentual
    diff_pct = ((rest_size.mean() - graphql_size.mean()) / rest_size.mean()) * 100
    print(f"\n📈 Diferença: GraphQL é {diff_pct:.1f}% menor (média)")
    
    # Teste de normalidade
    print("\n🔍 TESTE DE NORMALIDADE (Shapiro-Wilk)")
    print("-"*70)
    rest_norm = test_normality(rest_size)
    graphql_norm = test_normality(graphql_size)
    
    print(f"\nREST:")
    print(f"  Estatística: {rest_norm['statistic']:.4f}" if rest_norm['statistic'] else "  N/A")
    print(f"  p-value: {rest_norm['pvalue']:.4f}" if rest_norm['pvalue'] else "  N/A")
    print(f"  Normal: {'Sim' if rest_norm['normal'] else 'Não' if rest_norm['normal'] is not None else 'N/A'}")
    
    print(f"\nGraphQL:")
    print(f"  Estatística: {graphql_norm['statistic']:.4f}" if graphql_norm['statistic'] else "  N/A")
    print(f"  p-value: {graphql_norm['pvalue']:.4f}" if graphql_norm['pvalue'] else "  N/A")
    print(f"  Normal: {'Sim' if graphql_norm['normal'] else 'Não' if graphql_norm['normal'] is not None else 'N/A'}")
    
    both_normal = rest_norm['normal'] and graphql_norm['normal']
    
    # Teste de homogeneidade de variâncias
    print("\n🔍 TESTE DE HOMOGENEIDADE DE VARIÂNCIAS (Levene)")
    print("-"*70)
    levene_result = test_homogeneity(df, 'response_size_bytes', 'api_type')
    print(f"  Estatística: {levene_result['statistic']:.4f}" if levene_result['statistic'] else "  N/A")
    print(f"  p-value: {levene_result['pvalue']:.4f}" if levene_result['pvalue'] else "  N/A")
    print(f"  Variâncias homogêneas: {'Sim' if levene_result['homogeneous'] else 'Não' if levene_result['homogeneous'] is not None else 'N/A'}")
    
    # Teste de hipótese
    print("\n📊 TESTE DE HIPÓTESE")
    print("-"*70)
    print("H0: Não há diferença entre os tamanhos das respostas")
    print("H1: GraphQL tem tamanho menor que REST")
    
    if both_normal and levene_result['homogeneous']:
        # t-test
        stat, pvalue = ttest_ind(graphql_size, rest_size, alternative='less')
        test_name = "t-test (unilateral)"
        print(f"\n{test_name}:")
        print(f"  Estatística: {stat:.4f}")
        print(f"  p-value: {pvalue:.4f}")
        print(f"  Significativo (α=0.05): {'Sim' if pvalue < 0.05 else 'Não'}")
    else:
        # Mann-Whitney U (não-paramétrico)
        stat, pvalue = mannwhitneyu(graphql_size, rest_size, alternative='less')
        test_name = "Mann-Whitney U (unilateral)"
        print(f"\n{test_name}:")
        print(f"  Estatística: {stat:.4f}")
        print(f"  p-value: {pvalue:.4f}")
        print(f"  Significativo (α=0.05): {'Sim' if pvalue < 0.05 else 'Não'}")
    
    # Tamanho de efeito
    print("\n📏 TAMANHO DE EFEITO (Cohen's d)")
    print("-"*70)
    effect_size = cohens_d(graphql_size, rest_size)
    print(f"  Cohen's d: {effect_size['d']:.4f}")
    print(f"  Interpretação: {effect_size['interpretation']}")
    print(f"  Magnitude: {effect_size['magnitude']:.4f}")
    
    # Conclusão
    print("\n✅ CONCLUSÃO RQ2")
    print("-"*70)
    significant = pvalue < 0.05
    if significant:
        print(f"Rejeitamos H0. GraphQL tem tamanho estatisticamente menor que REST")
        print(f"(p = {pvalue:.4f}, d = {effect_size['d']:.4f})")
    else:
        print(f"Não rejeitamos H0. Não há evidência estatística de que GraphQL seja menor")
        print(f"(p = {pvalue:.4f}, d = {effect_size['d']:.4f})")
    
    return {
        'descriptive': desc_stats,
        'normality': {'REST': rest_norm, 'GraphQL': graphql_norm},
        'homogeneity': levene_result,
        'test': {'name': test_name, 'statistic': stat, 'pvalue': pvalue, 'significant': significant},
        'effect_size': effect_size,
        'conclusion': 'GraphQL é menor' if significant else 'Sem diferença significativa'
    }

def analyze_by_complexity(df):
    """Análise por complexidade da consulta"""
    print("\n" + "="*70)
    print("ANÁLISE POR COMPLEXIDADE DA CONSULTA")
    print("="*70)
    
    complexities = ['simple', 'medium', 'complex']
    results = {}
    
    for complexity in complexities:
        print(f"\n📊 Complexidade: {complexity.upper()}")
        print("-"*70)
        
        subset = df[df['complexity'] == complexity]
        rest_data = subset[subset['api_type'] == 'REST']['response_time_ms'].dropna()
        graphql_data = subset[subset['api_type'] == 'GraphQL']['response_time_ms'].dropna()
        
        if len(rest_data) > 0 and len(graphql_data) > 0:
            print(f"REST: Média = {rest_data.mean():.2f} ms, N = {len(rest_data)}")
            print(f"GraphQL: Média = {graphql_data.mean():.2f} ms, N = {len(graphql_data)}")
            
            # Teste de hipótese
            rest_norm = test_normality(rest_data)
            graphql_norm = test_normality(graphql_data)
            both_normal = rest_norm['normal'] and graphql_norm['normal']
            
            if both_normal:
                stat, pvalue = ttest_ind(graphql_data, rest_data, alternative='less')
                test_name = "t-test"
            else:
                stat, pvalue = mannwhitneyu(graphql_data, rest_data, alternative='less')
                test_name = "Mann-Whitney U"
            
            effect_size = cohens_d(graphql_data, rest_data)
            
            print(f"Teste: {test_name}, p = {pvalue:.4f}, d = {effect_size['d']:.4f}")
            print(f"Significativo: {'Sim' if pvalue < 0.05 else 'Não'}")
            
            results[complexity] = {
                'rest_mean': rest_data.mean(),
                'graphql_mean': graphql_data.mean(),
                'pvalue': pvalue,
                'effect_size': effect_size['d'],
                'significant': pvalue < 0.05
            }
    
    return results

def save_results(rq1_results, rq2_results, complexity_results):
    """Salva os resultados da análise"""
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Salvar em JSON
    output = {
        'timestamp': datetime.now().isoformat(),
        'rq1': rq1_results,
        'rq2': rq2_results,
        'complexity': complexity_results
    }
    
    json_file = os.path.join(results_dir, 'statistics.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\n✓ Resultados salvos em: {json_file}")
    
    # Salvar resumo em CSV
    summary_data = {
        'RQ': ['RQ1', 'RQ2'],
        'Hipótese': [
            'GraphQL é mais rápido que REST',
            'GraphQL tem tamanho menor que REST'
        ],
        'Teste_Estatístico': [
            rq1_results['test']['name'],
            rq2_results['test']['name']
        ],
        'p_value': [
            rq1_results['test']['pvalue'],
            rq2_results['test']['pvalue']
        ],
        'Significativo': [
            rq1_results['test']['significant'],
            rq2_results['test']['significant']
        ],
        'Cohens_d': [
            rq1_results['effect_size']['d'],
            rq2_results['effect_size']['d']
        ],
        'Interpretação_efeito': [
            rq1_results['effect_size']['interpretation'],
            rq2_results['effect_size']['interpretation']
        ],
        'Conclusão': [
            rq1_results['conclusion'],
            rq2_results['conclusion']
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    csv_file = os.path.join(results_dir, 'statistics_summary.csv')
    summary_df.to_csv(csv_file, index=False)
    print(f"✓ Resumo salvo em: {csv_file}")

def main():
    """Função principal"""
    print("="*70)
    print("ANÁLISE ESTATÍSTICA - EXPERIMENTO GraphQL vs REST")
    print("="*70)
    
    # Carregar dados
    df = load_data()
    
    # Verificar dados
    print(f"\n✓ Total de medições: {len(df)}")
    print(f"✓ Medições REST: {len(df[df['api_type'] == 'REST'])}")
    print(f"✓ Medições GraphQL: {len(df[df['api_type'] == 'GraphQL'])}")
    print(f"✓ Taxa de sucesso: {(df['success'].sum() / len(df) * 100):.1f}%")
    
    # Análise RQ1
    rq1_results = analyze_rq1(df)
    
    # Análise RQ2
    rq2_results = analyze_rq2(df)
    
    # Análise por complexidade
    complexity_results = analyze_by_complexity(df)
    
    # Salvar resultados
    save_results(rq1_results, rq2_results, complexity_results)
    
    # Resumo final
    print("\n" + "="*70)
    print("RESUMO FINAL")
    print("="*70)
    print(f"\nRQ1: {rq1_results['conclusion']}")
    print(f"  p-value: {rq1_results['test']['pvalue']:.4f}")
    print(f"  Cohen's d: {rq1_results['effect_size']['d']:.4f}")
    
    print(f"\nRQ2: {rq2_results['conclusion']}")
    print(f"  p-value: {rq2_results['test']['pvalue']:.4f}")
    print(f"  Cohen's d: {rq2_results['effect_size']['d']:.4f}")
    
    print("\n" + "="*70)
    print("Análise estatística concluída!")
    print("="*70)

if __name__ == '__main__':
    main()

