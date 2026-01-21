#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Automatizado de Análise de Oportunidades Imobiliárias
Londrina/PR - Zona Sul

Script principal que integra scraping, filtragem e análise de dados REAIS.

Autor: Sistema de Análise Imobiliária
Data: 2026-01-21
"""

import json
import sys
from collections import defaultdict
from typing import List, Dict


def analisar_oportunidades(arquivo_dados: str = 'dados_imoveis_londrina.json') -> List[Dict]:
    """
    Analisa oportunidades de compra (preços abaixo do mercado).
    
    Args:
        arquivo_dados: Caminho do arquivo JSON com dados filtrados
    
    Returns:
        Lista de oportunidades identificadas
    """
    print("\n" + "="*80)
    print("ANÁLISE DE OPORTUNIDADES DE COMPRA")
    print("="*80)
    
    try:
        with open(arquivo_dados, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {arquivo_dados}")
        return []
    
    # Agrupar por bairro e calcular preço médio/m²
    vendas_por_bairro = defaultdict(list)
    
    for imovel in dados:
        if (imovel.get('tipo_anuncio') == 'venda' and 
            imovel.get('preco_venda') and 
            imovel.get('metragem') and 
            imovel.get('metragem') > 0):
            
            bairro = imovel.get('bairro', 'Não informado')
            preco_m2 = imovel['preco_venda'] / imovel['metragem']
            vendas_por_bairro[bairro].append({
                'imovel': imovel,
                'preco_m2': preco_m2
            })
    
    print(f"\n📊 Bairros analisados: {len(vendas_por_bairro)}")
    
    # Calcular médias e identificar oportunidades
    oportunidades = []
    
    for bairro, vendas in vendas_por_bairro.items():
        if len(vendas) < 2:
            continue
        
        preco_medio_m2 = sum(v['preco_m2'] for v in vendas) / len(vendas)
        
        print(f"\n🏘️  {bairro}:")
        print(f"   • Imóveis à venda: {len(vendas)}")
        print(f"   • Preço médio: R$ {preco_medio_m2:,.2f}/m²")
        
        oportunidades_bairro = 0
        
        for venda in vendas:
            imovel = venda['imovel']
            preco_m2 = venda['preco_m2']
            percentual_diferenca = ((preco_medio_m2 - preco_m2) / preco_medio_m2) * 100
            
            if percentual_diferenca >= 10:
                oportunidades.append({
                    'bairro': bairro,
                    'nome_empreendimento': imovel.get('nome_empreendimento', 'Não informado'),
                    'metragem': imovel['metragem'],
                    'preco_venda': imovel['preco_venda'],
                    'preco_m2': round(preco_m2, 2),
                    'preco_medio_bairro': round(preco_medio_m2, 2),
                    'percentual_abaixo': round(percentual_diferenca, 2),
                    'classificacao': 'Oportunidade',
                    'link': imovel.get('link', ''),
                    'titulo': imovel.get('titulo', ''),
                    'plataforma': imovel.get('plataforma', '')
                })
                oportunidades_bairro += 1
        
        if oportunidades_bairro > 0:
            print(f"   • ✅ Oportunidades encontradas: {oportunidades_bairro}")
    
    # Ordenar por percentual abaixo do mercado
    oportunidades.sort(key=lambda x: x['percentual_abaixo'], reverse=True)
    
    print(f"\n💰 Total de oportunidades identificadas: {len(oportunidades)}")
    print("="*80 + "\n")
    
    return oportunidades


def calcular_yield(arquivo_dados: str = 'dados_imoveis_londrina.json') -> List[Dict]:
    """
    Calcula rentabilidade (yield) dos imóveis.
    
    Args:
        arquivo_dados: Caminho do arquivo JSON com dados filtrados
    
    Returns:
        Lista de imóveis com yield calculado
    """
    print("\n" + "="*80)
    print("CÁLCULO DE RENTABILIDADE (YIELD)")
    print("="*80)
    
    try:
        with open(arquivo_dados, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {arquivo_dados}")
        return []
    
    # Calcular aluguel médio por bairro
    alugueis_por_bairro = defaultdict(list)
    
    for imovel in dados:
        if imovel.get('tipo_anuncio') == 'aluguel' and imovel.get('preco_aluguel'):
            bairro = imovel.get('bairro', 'Não informado')
            alugueis_por_bairro[bairro].append(imovel['preco_aluguel'])
    
    aluguel_medio_bairro = {
        bairro: sum(alugueis) / len(alugueis)
        for bairro, alugueis in alugueis_por_bairro.items()
        if alugueis
    }
    
    print(f"\n📊 Bairros com dados de aluguel: {len(aluguel_medio_bairro)}")
    
    for bairro, aluguel_medio in sorted(aluguel_medio_bairro.items()):
        print(f"   • {bairro}: R$ {aluguel_medio:,.2f}/mês")
    
    # Calcular yield para imóveis à venda
    yields = []
    
    for imovel in dados:
        if imovel.get('tipo_anuncio') == 'venda' and imovel.get('preco_venda'):
            bairro = imovel.get('bairro', 'Não informado')
            
            if bairro not in aluguel_medio_bairro:
                continue
            
            aluguel_medio = aluguel_medio_bairro[bairro]
            yield_anual = ((aluguel_medio * 12) / imovel['preco_venda']) * 100
            
            # Classificação
            if yield_anual >= 8:
                classificacao = 'Excelente (≥8%)'
            elif yield_anual >= 6:
                classificacao = 'Alta rentabilidade (6-8%)'
            elif yield_anual >= 4:
                classificacao = 'Boa rentabilidade (4-6%)'
            else:
                classificacao = 'Baixa rentabilidade (<4%)'
            
            yields.append({
                'nome_empreendimento': imovel.get('nome_empreendimento', 'Não informado'),
                'bairro': bairro,
                'preco_venda': imovel['preco_venda'],
                'metragem': imovel.get('metragem'),
                'aluguel_medio': round(aluguel_medio, 2),
                'yield_anual': round(yield_anual, 2),
                'classificacao': classificacao,
                'link': imovel.get('link', ''),
                'titulo': imovel.get('titulo', ''),
                'plataforma': imovel.get('plataforma', '')
            })
    
    # Ordenar por yield
    yields.sort(key=lambda x: x['yield_anual'], reverse=True)
    
    print(f"\n📈 Total de imóveis com yield calculado: {len(yields)}")
    print("="*80 + "\n")
    
    return yields


def gerar_relatorio(oportunidades: List[Dict], yields: List[Dict]):
    """
    Gera relatórios consolidados em JSON e Markdown.
    
    Args:
        oportunidades: Lista de oportunidades identificadas
        yields: Lista de imóveis com yield calculado
    """
    print("\n" + "="*80)
    print("GERANDO RELATÓRIOS")
    print("="*80)
    
    # Gerar JSON
    relatorio = {
        'oportunidades': oportunidades[:10] if len(oportunidades) > 10 else oportunidades,
        'ranking_yield': yields[:10] if len(yields) > 10 else yields,
        'estatisticas': {
            'total_oportunidades': len(oportunidades),
            'total_yields': len(yields)
        }
    }
    
    with open('relatorio_final.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Relatório JSON salvo: relatorio_final.json")
    
    # Gerar Markdown
    with open('relatorio_final.md', 'w', encoding='utf-8') as f:
        f.write('# 📊 Relatório de Oportunidades Imobiliárias - Zona Sul de Londrina/PR\n\n')
        f.write('> Dados extraídos via web scraping de **OLX** e **ZAP Imóveis**\n\n')
        f.write('---\n\n')
        
        # Oportunidades
        f.write('## 💰 Top 10 Oportunidades (Abaixo do Mercado)\n\n')
        
        if oportunidades:
            for i, op in enumerate(oportunidades[:10], 1):
                f.write(f"### {i}. **{op['nome_empreendimento']}** - {op['bairro']}\n\n")
                f.write(f"- **Plataforma:** {op.get('plataforma', 'N/A')}\n")
                f.write(f"- **Preço:** R$ {op['preco_venda']:,.2f}\n")
                f.write(f"- **Metragem:** {op['metragem']} m²\n")
                f.write(f"- **Preço/m²:** R$ {op['preco_m2']:,.2f}\n")
                f.write(f"- **Preço médio do bairro:** R$ {op['preco_medio_bairro']:,.2f}/m²\n")
                f.write(f"- **🎯 Abaixo do mercado:** {op['percentual_abaixo']:.2f}%\n")
                f.write(f"- **Link:** [{op.get('titulo', 'Ver anúncio')[:50]}...]({op['link']})\n\n")
        else:
            f.write('*Nenhuma oportunidade identificada com os critérios atuais.*\n\n')
        
        f.write('---\n\n')
        
        # Rentabilidade
        f.write('## 📈 Top 10 Rentabilidade (Maior Yield)\n\n')
        
        if yields:
            for i, y in enumerate(yields[:10], 1):
                f.write(f"### {i}. **{y['nome_empreendimento']}** - {y['bairro']}\n\n")
                f.write(f"- **Plataforma:** {y.get('plataforma', 'N/A')}\n")
                f.write(f"- **Preço:** R$ {y['preco_venda']:,.2f}\n")
                if y.get('metragem'):
                    f.write(f"- **Metragem:** {y['metragem']} m²\n")
                f.write(f"- **Aluguel médio do bairro:** R$ {y['aluguel_medio']:,.2f}/mês\n")
                f.write(f"- **🏆 Yield anual:** {y['yield_anual']:.2f}%\n")
                f.write(f"- **Classificação:** {y['classificacao']}\n")
                f.write(f"- **Link:** [{y.get('titulo', 'Ver anúncio')[:50]}...]({y['link']})\n\n")
        else:
            f.write('*Não foi possível calcular yield (faltam dados de aluguel).*\n\n')
        
        f.write('---\n\n')
        f.write('## 📝 Notas\n\n')
        f.write('- **Yield calculado:** Rentabilidade bruta anual, sem considerar impostos, taxas e despesas.\n')
        f.write('- **Oportunidades:** Imóveis com preço ≥10% abaixo da média do bairro.\n')
        f.write('- **Dados:** Extraídos via web scraping em tempo real.\n\n')
        f.write('---\n\n')
        f.write('*Relatório gerado automaticamente pelo Sistema de Análise Imobiliária*\n')
    
    print(f"💾 Relatório Markdown salvo: relatorio_final.md")
    print("\n✅ Relatórios gerados com sucesso!")
    print("="*80 + "\n")


def main():
    """
    Função principal do sistema integrado.
    Executa scraping, filtragem e análise.
    """
    print("\n" + "="*80)
    print("SISTEMA AUTOMATIZADO DE ANÁLISE DE OPORTUNIDADES IMOBILIÁRIAS")
    print("Londrina/PR - Zona Sul")
    print("="*80)
    print("\nEste sistema realiza:")
    print("1. ✅ Web scraping REAL de OLX e ZAP Imóveis")
    print("2. ✅ Filtragem de dados (cessão de direitos, preço, tipo)")
    print("3. ✅ Análise de oportunidades de compra")
    print("4. ✅ Cálculo de rentabilidade (yield)")
    print("5. ✅ Geração de relatórios consolidados")
    print("\n" + "="*80 + "\n")
    
    # Verificar se deve executar scraping
    import os
    executar_scraping = True
    
    if os.path.exists('dados_imoveis_bruto.json'):
        resposta = input("📁 Arquivo 'dados_imoveis_bruto.json' já existe. Deseja executar novo scraping? (s/N): ")
        executar_scraping = resposta.lower() in ['s', 'sim', 'y', 'yes']
    
    # Etapa 1: Scraping
    if executar_scraping:
        print("\n🚀 ETAPA 1: Web Scraping")
        print("-" * 80)
        
        try:
            from scraper_imoveis import ScraperImoveis
            
            scraper = ScraperImoveis()
            todos_anuncios = scraper.executar_scraping()
            
            if todos_anuncios:
                with open('dados_imoveis_bruto.json', 'w', encoding='utf-8') as f:
                    json.dump(todos_anuncios, f, ensure_ascii=False, indent=2)
                print(f"✅ Dados brutos salvos: dados_imoveis_bruto.json ({len(todos_anuncios)} anúncios)")
            else:
                print("⚠️  AVISO: Nenhum anúncio foi extraído via scraping.")
                print("⚠️  Verifique a conexão com internet e disponibilidade dos sites.")
                print("⚠️  O sistema continuará com dados existentes (se houver).")
        
        except ImportError:
            print("❌ Erro: Módulo 'scraper_imoveis' não encontrado.")
            print("ℹ️  Continuando com dados existentes...")
        except Exception as e:
            print(f"❌ Erro durante scraping: {e}")
            print("ℹ️  Continuando com dados existentes...")
    else:
        print("\n⏭️  ETAPA 1: Scraping pulado (usando dados existentes)")
    
    # Etapa 2: Filtragem
    print("\n🔍 ETAPA 2: Filtragem de Dados")
    print("-" * 80)
    
    try:
        from filtrador_imoveis import FiltradorImoveis
        
        filtrador = FiltradorImoveis()
        dados_filtrados, cessao_direitos = filtrador.filtrar_dados('dados_imoveis_bruto.json')
        
        if dados_filtrados:
            filtrador.salvar_dados_filtrados(dados_filtrados, cessao_direitos)
        else:
            print("⚠️  Nenhum dado válido após filtragem.")
            return
    
    except FileNotFoundError:
        print("❌ Arquivo 'dados_imoveis_bruto.json' não encontrado.")
        print("ℹ️  Execute o scraping primeiro ou forneça um arquivo de dados.")
        return
    except Exception as e:
        print(f"❌ Erro durante filtragem: {e}")
        return
    
    # Etapa 3: Análise de Oportunidades
    print("\n💰 ETAPA 3: Análise de Oportunidades")
    print("-" * 80)
    
    try:
        oportunidades = analisar_oportunidades()
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        oportunidades = []
    
    # Etapa 4: Cálculo de Yield
    print("\n📈 ETAPA 4: Cálculo de Rentabilidade")
    print("-" * 80)
    
    try:
        yields = calcular_yield()
    except Exception as e:
        print(f"❌ Erro durante cálculo de yield: {e}")
        yields = []
    
    # Etapa 5: Geração de Relatórios
    print("\n📝 ETAPA 5: Geração de Relatórios")
    print("-" * 80)
    
    try:
        gerar_relatorio(oportunidades, yields)
    except Exception as e:
        print(f"❌ Erro ao gerar relatórios: {e}")
    
    # Resumo final
    print("\n" + "="*80)
    print("✅ PROCESSO CONCLUÍDO")
    print("="*80)
    print("\n📊 Resumo:")
    print(f"   • Oportunidades identificadas: {len(oportunidades)}")
    print(f"   • Imóveis com yield calculado: {len(yields)}")
    print("\n📁 Arquivos gerados:")
    print("   • dados_imoveis_bruto.json - Dados extraídos via scraping")
    print("   • dados_imoveis_londrina.json - Dados filtrados")
    print("   • cessao_direitos.json - Cessão de direitos separados")
    print("   • relatorio_final.json - Relatório em formato JSON")
    print("   • relatorio_final.md - Relatório em formato Markdown")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Processo interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
