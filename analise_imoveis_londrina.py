#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mecanismo de Análise de Oportunidades Imobiliárias em Londrina/PR - Zona Sul

Este script analisa dados de preços de venda e aluguel de apartamentos em Londrina/PR
para identificar oportunidades de compra abaixo do valor de mercado e calcular a
rentabilidade anual projetada (yield).

Plataformas de busca simuladas:
- OLX: https://www.olx.com.br/
- ZAP Imóveis: https://www.zapimoveis.com.br/

Autor: Sistema de Análise Imobiliária
Data: 2026-01-19
"""

import json
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from statistics import mean
import os


@dataclass
class Imovel:
    """Representa um imóvel com suas características."""
    plataforma: str
    bairro: str
    nome_empreendimento: str
    metragem: float  # em m²
    preco_venda: float  # em R$
    aluguel_mensal: float = 0.0  # em R$
    endereco: str = ""
    
    @property
    def preco_por_m2(self) -> float:
        """Calcula o preço por metro quadrado."""
        return self.preco_venda / self.metragem if self.metragem > 0 else 0.0
    
    @property
    def yield_anual(self) -> float:
        """Calcula o yield anual bruto em porcentagem."""
        if self.preco_venda > 0 and self.aluguel_mensal > 0:
            return ((self.aluguel_mensal * 12) / self.preco_venda) * 100
        return 0.0


class AnalisadorImoveis:
    """Classe principal para análise de oportunidades imobiliárias."""
    
    def __init__(self):
        self.imoveis: List[Imovel] = []
        self.percentual_oportunidade = 10.0  # 10% abaixo do mercado
    
    def adicionar_imovel(self, imovel: Imovel):
        """Adiciona um imóvel à lista de análise."""
        self.imoveis.append(imovel)
    
    def carregar_dados_json(self, arquivo: str):
        """Carrega dados de imóveis de um arquivo JSON."""
        if not os.path.exists(arquivo):
            print(f"Arquivo {arquivo} não encontrado.")
            return
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        for item in dados:
            imovel = Imovel(**item)
            self.adicionar_imovel(imovel)
        
        print(f"✓ {len(dados)} imóveis carregados de {arquivo}")
    
    def obter_imoveis_por_bairro(self, bairro: str) -> List[Imovel]:
        """Retorna todos os imóveis de um bairro específico."""
        return [i for i in self.imoveis if i.bairro.lower() == bairro.lower()]
    
    def calcular_preco_medio_m2(self, bairro: str) -> float:
        """Calcula o preço médio por m² em um bairro."""
        imoveis_bairro = self.obter_imoveis_por_bairro(bairro)
        if not imoveis_bairro:
            return 0.0
        
        precos_m2 = [i.preco_por_m2 for i in imoveis_bairro]
        return mean(precos_m2)
    
    def identificar_oportunidades(self, bairro: str = None) -> List[Tuple[Imovel, float, float]]:
        """
        Identifica imóveis abaixo do preço médio do mercado.
        
        Retorna lista de tuplas: (imovel, preco_medio_bairro, percentual_abaixo)
        """
        oportunidades = []
        
        bairros = set(i.bairro for i in self.imoveis)
        if bairro:
            bairros = {bairro}
        
        for b in bairros:
            preco_medio = self.calcular_preco_medio_m2(b)
            if preco_medio == 0:
                continue
            
            imoveis_bairro = self.obter_imoveis_por_bairro(b)
            
            for imovel in imoveis_bairro:
                percentual_diferenca = ((preco_medio - imovel.preco_por_m2) / preco_medio) * 100
                
                # Verifica se está 10% ou mais abaixo do preço médio
                if percentual_diferenca >= self.percentual_oportunidade:
                    oportunidades.append((imovel, preco_medio, percentual_diferenca))
        
        # Ordena por maior percentual abaixo do mercado
        oportunidades.sort(key=lambda x: x[2], reverse=True)
        return oportunidades
    
    def calcular_yields(self) -> List[Tuple[Imovel, float]]:
        """
        Calcula o yield anual bruto de todos os imóveis com dados de aluguel.
        
        Retorna lista de tuplas: (imovel, yield_percentual)
        """
        yields = []
        
        for imovel in self.imoveis:
            if imovel.aluguel_mensal > 0:
                yields.append((imovel, imovel.yield_anual))
        
        # Ordena por maior yield
        yields.sort(key=lambda x: x[1], reverse=True)
        return yields
    
    def gerar_relatorio_bairro(self, bairro: str) -> str:
        """Gera relatório detalhado para um bairro específico."""
        imoveis_bairro = self.obter_imoveis_por_bairro(bairro)
        if not imoveis_bairro:
            return f"\n❌ Sem dados suficientes para análise do bairro {bairro}.\n"
        
        preco_medio_m2 = self.calcular_preco_medio_m2(bairro)
        
        relatorio = [
            f"\n{'=' * 80}",
            f"ANÁLISE DO BAIRRO: {bairro.upper()}",
            f"{'=' * 80}",
            f"\n📊 Estatísticas Gerais:",
            f"   • Total de imóveis analisados: {len(imoveis_bairro)}",
            f"   • Preço médio por m²: R$ {preco_medio_m2:,.2f}",
        ]
        
        # Oportunidades neste bairro
        oportunidades = self.identificar_oportunidades(bairro)
        if oportunidades:
            relatorio.append(f"\n💰 Oportunidades de Compra (≥{self.percentual_oportunidade}% abaixo do mercado):")
            relatorio.append(f"   Total: {len(oportunidades)} imóvel(is)\n")
            
            for i, (imovel, preco_medio, perc_abaixo) in enumerate(oportunidades, 1):
                relatorio.extend([
                    f"   {i}. {imovel.nome_empreendimento}",
                    f"      • Plataforma: {imovel.plataforma}",
                    f"      • Metragem: {imovel.metragem} m²",
                    f"      • Preço de venda: R$ {imovel.preco_venda:,.2f}",
                    f"      • Preço por m²: R$ {imovel.preco_por_m2:,.2f}",
                    f"      • Preço médio do bairro: R$ {preco_medio:,.2f}/m²",
                    f"      • 🎯 ABAIXO DO MERCADO: {perc_abaixo:.2f}%",
                    ""
                ])
        else:
            relatorio.append(f"\n❌ Nenhuma oportunidade encontrada neste bairro.\n")
        
        # Yields neste bairro
        yields_bairro = [(i, y) for i, y in self.calcular_yields() if i.bairro == bairro]
        if yields_bairro:
            relatorio.append(f"\n📈 Análise de Rentabilidade (Yield Anual Bruto):")
            relatorio.append(f"   Total: {len(yields_bairro)} imóvel(is) com dados de aluguel\n")
            
            for i, (imovel, yield_val) in enumerate(yields_bairro, 1):
                classificacao = self._classificar_yield(yield_val)
                relatorio.extend([
                    f"   {i}. {imovel.nome_empreendimento}",
                    f"      • Plataforma: {imovel.plataforma}",
                    f"      • Metragem: {imovel.metragem} m²",
                    f"      • Preço de venda: R$ {imovel.preco_venda:,.2f}",
                    f"      • Aluguel mensal: R$ {imovel.aluguel_mensal:,.2f}",
                    f"      • Yield Bruto: {yield_val:.2f}% ao ano",
                    f"      • 🏆 Classificação: {classificacao}",
                    ""
                ])
        
        return "\n".join(relatorio)
    
    def _classificar_yield(self, yield_val: float) -> str:
        """Classifica o yield em categorias."""
        if yield_val >= 8.0:
            return "EXCELENTE (≥8%)"
        elif yield_val >= 6.0:
            return "ALTA RENTABILIDADE (6-8%)"
        elif yield_val >= 4.0:
            return "BOA RENTABILIDADE (4-6%)"
        else:
            return "BAIXA RENTABILIDADE (<4%)"
    
    def gerar_relatorio_completo(self) -> str:
        """Gera relatório consolidado de todas as análises."""
        if not self.imoveis:
            return "\n❌ Nenhum imóvel cadastrado para análise.\n"
        
        bairros = sorted(set(i.bairro for i in self.imoveis))
        
        relatorio = [
            "\n" + "=" * 80,
            "RELATÓRIO CONSOLIDADO - ANÁLISE DE OPORTUNIDADES IMOBILIÁRIAS",
            "LONDRINA/PR - ZONA SUL",
            "=" * 80,
            f"\n📍 Bairros analisados: {', '.join(bairros)}",
            f"📊 Total de imóveis: {len(self.imoveis)}",
            "\n" + "=" * 80,
        ]
        
        # Relatório por bairro
        for bairro in bairros:
            relatorio.append(self.gerar_relatorio_bairro(bairro))
        
        # Ranking geral de oportunidades
        relatorio.extend([
            "\n" + "=" * 80,
            "🏆 RANKING GERAL - MELHORES OPORTUNIDADES DE COMPRA",
            "=" * 80,
        ])
        
        todas_oportunidades = self.identificar_oportunidades()
        if todas_oportunidades:
            relatorio.append(f"\nTop {min(10, len(todas_oportunidades))} oportunidades:\n")
            
            for i, (imovel, preco_medio, perc_abaixo) in enumerate(todas_oportunidades[:10], 1):
                relatorio.extend([
                    f"{i}. {imovel.nome_empreendimento} - {imovel.bairro}",
                    f"   • Plataforma: {imovel.plataforma}",
                    f"   • Metragem: {imovel.metragem} m²",
                    f"   • Preço: R$ {imovel.preco_venda:,.2f} (R$ {imovel.preco_por_m2:,.2f}/m²)",
                    f"   • 🎯 Abaixo do mercado: {perc_abaixo:.2f}%",
                    ""
                ])
        else:
            relatorio.append("\n❌ Nenhuma oportunidade encontrada.\n")
        
        # Ranking geral de rentabilidade
        relatorio.extend([
            "\n" + "=" * 80,
            "📈 RANKING GERAL - MAIOR RENTABILIDADE (YIELD)",
            "=" * 80,
        ])
        
        todos_yields = self.calcular_yields()
        if todos_yields:
            relatorio.append(f"\nTop {min(10, len(todos_yields))} rentabilidades:\n")
            
            for i, (imovel, yield_val) in enumerate(todos_yields[:10], 1):
                classificacao = self._classificar_yield(yield_val)
                relatorio.extend([
                    f"{i}. {imovel.nome_empreendimento} - {imovel.bairro}",
                    f"   • Plataforma: {imovel.plataforma}",
                    f"   • Preço: R$ {imovel.preco_venda:,.2f} | Aluguel: R$ {imovel.aluguel_mensal:,.2f}",
                    f"   • 🏆 Yield: {yield_val:.2f}% ao ano - {classificacao}",
                    ""
                ])
        else:
            relatorio.append("\n❌ Nenhum imóvel com dados de aluguel para calcular yield.\n")
        
        relatorio.append("=" * 80 + "\n")
        
        return "\n".join(relatorio)
    
    def exportar_oportunidades_json(self, arquivo: str = "oportunidades.json"):
        """Exporta as oportunidades para um arquivo JSON."""
        oportunidades = self.identificar_oportunidades()
        
        dados = []
        for imovel, preco_medio, perc_abaixo in oportunidades:
            dados.append({
                "nome_empreendimento": imovel.nome_empreendimento,
                "bairro": imovel.bairro,
                "plataforma": imovel.plataforma,
                "metragem": imovel.metragem,
                "preco_venda": imovel.preco_venda,
                "preco_por_m2": imovel.preco_por_m2,
                "preco_medio_bairro": preco_medio,
                "percentual_abaixo_mercado": perc_abaixo,
                "aluguel_mensal": imovel.aluguel_mensal,
                "yield_anual": imovel.yield_anual if imovel.aluguel_mensal > 0 else None
            })
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Oportunidades exportadas para {arquivo}")


def criar_dados_exemplo():
    """Cria arquivo de dados de exemplo para demonstração."""
    dados_exemplo = [
        # Gleba Palhano - Incluindo uma oportunidade abaixo do mercado
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Gleba Palhano",
            "nome_empreendimento": "Residencial Verona",
            "metragem": 72.0,
            "preco_venda": 460000.0,
            "aluguel_mensal": 2800.0,
            "endereco": "Rua das Orquídeas, 123"
        },
        {
            "plataforma": "OLX",
            "bairro": "Gleba Palhano",
            "nome_empreendimento": "Edifício Toscana",
            "metragem": 85.0,
            "preco_venda": 650000.0,
            "aluguel_mensal": 3500.0,
            "endereco": "Av. Ayrton Senna, 456"
        },
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Gleba Palhano",
            "nome_empreendimento": "Residencial Jardim Europeu",
            "metragem": 78.0,
            "preco_venda": 520000.0,
            "aluguel_mensal": 3100.0,
            "endereco": "Rua das Camélias, 789"
        },
        {
            "plataforma": "OLX",
            "bairro": "Gleba Palhano",
            "nome_empreendimento": "Residencial São Paulo",
            "metragem": 80.0,
            "preco_venda": 550000.0,
            "aluguel_mensal": 3300.0,
            "endereco": "Av. Madre Leônia Milito, 555"
        },
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Gleba Palhano",
            "nome_empreendimento": "Residencial Villa Verde - OPORTUNIDADE",
            "metragem": 75.0,
            "preco_venda": 420000.0,
            "aluguel_mensal": 2700.0,
            "endereco": "Rua das Tulipas, 999"
        },
        # Alto da Boa Vista - Incluindo uma oportunidade
        {
            "plataforma": "OLX",
            "bairro": "Alto da Boa Vista",
            "nome_empreendimento": "Residencial Aurora",
            "metragem": 92.0,
            "preco_venda": 520000.0,
            "aluguel_mensal": 3200.0,
            "endereco": "Rua Mato Grosso, 321"
        },
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Alto da Boa Vista",
            "nome_empreendimento": "Edifício Bela Vista",
            "metragem": 75.0,
            "preco_venda": 380000.0,
            "aluguel_mensal": 2400.0,
            "endereco": "Rua Pernambuco, 654"
        },
        {
            "plataforma": "OLX",
            "bairro": "Alto da Boa Vista",
            "nome_empreendimento": "Condomínio Horizonte",
            "metragem": 88.0,
            "preco_venda": 495000.0,
            "aluguel_mensal": 3000.0,
            "endereco": "Av. Brasília, 987"
        },
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Alto da Boa Vista",
            "nome_empreendimento": "Residencial das Palmeiras",
            "metragem": 70.0,
            "preco_venda": 350000.0,
            "aluguel_mensal": 2300.0,
            "endereco": "Rua Sergipe, 234"
        },
        {
            "plataforma": "OLX",
            "bairro": "Alto da Boa Vista",
            "nome_empreendimento": "Apartamento Vista Alegre - OPORTUNIDADE",
            "metragem": 78.0,
            "preco_venda": 340000.0,
            "aluguel_mensal": 2250.0,
            "endereco": "Rua Goiás, 876"
        },
        # Jardim Shangri-lá - Incluindo uma oportunidade abaixo do mercado
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Jardim Shangri-lá",
            "nome_empreendimento": "Residencial Paraíso",
            "metragem": 65.0,
            "preco_venda": 340000.0,
            "aluguel_mensal": 2200.0,
            "endereco": "Rua dos Jacarandás, 147"
        },
        {
            "plataforma": "OLX",
            "bairro": "Jardim Shangri-lá",
            "nome_empreendimento": "Edifício Primavera",
            "metragem": 70.0,
            "preco_venda": 385000.0,
            "aluguel_mensal": 2500.0,
            "endereco": "Rua das Acácias, 258"
        },
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Jardim Shangri-lá",
            "nome_empreendimento": "Condomínio Vista Verde",
            "metragem": 80.0,
            "preco_venda": 420000.0,
            "aluguel_mensal": 2700.0,
            "endereco": "Av. dos Ipês, 369"
        },
        {
            "plataforma": "OLX",
            "bairro": "Jardim Shangri-lá",
            "nome_empreendimento": "Residencial das Flores",
            "metragem": 68.0,
            "preco_venda": 320000.0,
            "aluguel_mensal": 2100.0,
            "endereco": "Rua das Violetas, 741"
        },
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Jardim Shangri-lá",
            "nome_empreendimento": "Apartamento Solar das Orquídeas - OPORTUNIDADE",
            "metragem": 72.0,
            "preco_venda": 310000.0,
            "aluguel_mensal": 2050.0,
            "endereco": "Rua das Magnólias, 555"
        },
        # Lago Parque
        {
            "plataforma": "OLX",
            "bairro": "Lago Parque",
            "nome_empreendimento": "Residencial Laguna",
            "metragem": 95.0,
            "preco_venda": 580000.0,
            "aluguel_mensal": 3600.0,
            "endereco": "Rua do Lago, 741"
        },
        {
            "plataforma": "ZAP Imóveis",
            "bairro": "Lago Parque",
            "nome_empreendimento": "Edifício Água Viva",
            "metragem": 82.0,
            "preco_venda": 450000.0,
            "aluguel_mensal": 2900.0,
            "endereco": "Av. das Águas, 852"
        },
        {
            "plataforma": "OLX",
            "bairro": "Lago Parque",
            "nome_empreendimento": "Condomínio Beira Lago",
            "metragem": 100.0,
            "preco_venda": 620000.0,
            "aluguel_mensal": 3800.0,
            "endereco": "Rua da Margem, 963"
        }
    ]
    
    arquivo = "dados_imoveis_londrina.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_exemplo, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Arquivo de dados de exemplo criado: {arquivo}")
    return arquivo


def main():
    """Função principal do programa."""
    print("\n" + "=" * 80)
    print("SISTEMA DE ANÁLISE DE OPORTUNIDADES IMOBILIÁRIAS")
    print("Londrina/PR - Zona Sul")
    print("=" * 80 + "\n")
    
    # Cria dados de exemplo se não existir arquivo
    arquivo_dados = "dados_imoveis_londrina.json"
    if not os.path.exists(arquivo_dados):
        print("📁 Criando arquivo de dados de exemplo...")
        arquivo_dados = criar_dados_exemplo()
        print()
    
    # Inicializa o analisador
    analisador = AnalisadorImoveis()
    
    # Carrega dados
    print("📥 Carregando dados dos imóveis...")
    analisador.carregar_dados_json(arquivo_dados)
    print()
    
    # Gera e exibe relatório completo
    print("📊 Gerando relatório de análise...")
    relatorio = analisador.gerar_relatorio_completo()
    print(relatorio)
    
    # Exporta oportunidades
    print("💾 Exportando oportunidades...")
    analisador.exportar_oportunidades_json()
    print()
    
    print("✅ Análise concluída com sucesso!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
