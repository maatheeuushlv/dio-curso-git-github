#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Filtragem de Dados de Imóveis

Aplica filtros para separar cessão de direitos, validar valores e tipos de imóveis.

Autor: Sistema de Análise Imobiliária
Data: 2026-01-21
"""

import json
import re
from typing import List, Dict, Tuple


class FiltradorImoveis:
    """Classe para filtragem de dados de imóveis."""
    
    def __init__(self):
        self.palavras_cessao = [
            'cessão de direitos',
            'cessao de direitos',
            'transferência de direitos',
            'transferencia de direitos'
        ]
        
        self.palavras_exclusao_tipo = [
            r'\bcasa\b',
            r'\bcasas\b',
            r'\bterreno\b',
            r'\blote\b',
            r'\bsala comercial\b',
            r'\bsala comerci',
            r'\bgalpão\b',
            r'\bgalpao\b',
            r'\bchácara\b',
            r'\bchacara\b',
            r'\bsítio\b',
            r'\bsitio\b',
            r'\bponto comercial\b',
            r'\bsobrado\b'
        ]
        
        self.valor_maximo = 700000.0
    
    def eh_cessao_direitos(self, titulo: str, descricao: str) -> bool:
        """
        Verifica se o anúncio é de cessão de direitos.
        
        Args:
            titulo: Título do anúncio
            descricao: Descrição do anúncio
        
        Returns:
            True se for cessão de direitos, False caso contrário
        """
        texto_completo = f"{titulo} {descricao}".lower()
        
        for palavra in self.palavras_cessao:
            if palavra in texto_completo:
                return True
        
        return False
    
    def eh_tipo_valido(self, titulo: str, descricao: str) -> bool:
        """
        Verifica se é um apartamento (não casa, terreno, etc).
        
        Args:
            titulo: Título do anúncio
            descricao: Descrição do anúncio
        
        Returns:
            True se for apartamento, False caso contrário
        """
        texto_completo = f"{titulo} {descricao}".lower()
        
        # Usar regex para buscar palavra completa (word boundary)
        for padrao in self.palavras_exclusao_tipo:
            if re.search(padrao, texto_completo, re.IGNORECASE):
                return False
        
        return True
    
    def eh_preco_valido(self, preco: float) -> bool:
        """
        Verifica se o preço está dentro do limite.
        
        Args:
            preco: Preço do imóvel
        
        Returns:
            True se válido, False caso contrário
        """
        if preco is None:
            return False
        
        return preco <= self.valor_maximo
    
    def filtrar_dados(self, arquivo_entrada: str) -> Tuple[List[Dict], List[Dict]]:
        """
        Aplica todos os filtros nos dados.
        
        Args:
            arquivo_entrada: Caminho do arquivo JSON com dados brutos
        
        Returns:
            Tupla com (dados_filtrados, cessao_direitos)
        """
        print("\n" + "="*80)
        print("APLICANDO FILTROS NOS DADOS")
        print("="*80)
        
        # Carregar dados
        try:
            with open(arquivo_entrada, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
            return [], []
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON: {arquivo_entrada}")
            return [], []
        
        print(f"📊 Total de anúncios carregados: {len(dados)}")
        
        cessao_direitos = []
        dados_filtrados = []
        
        # Estatísticas
        stats = {
            'total': len(dados),
            'cessao': 0,
            'preco_invalido': 0,
            'tipo_invalido': 0,
            'validos': 0
        }
        
        for imovel in dados:
            titulo = imovel.get('titulo', '')
            descricao = imovel.get('descricao', '')
            
            # Filtro 1: Cessão de direitos
            if self.eh_cessao_direitos(titulo, descricao):
                cessao_direitos.append(imovel)
                stats['cessao'] += 1
                continue
            
            # Filtro 2: Valor máximo (apenas para vendas)
            if imovel.get('tipo_anuncio') == 'venda':
                preco = imovel.get('preco_venda')
                if not self.eh_preco_valido(preco):
                    stats['preco_invalido'] += 1
                    continue
            
            # Filtro 3: Tipo de imóvel (apenas apartamentos)
            if not self.eh_tipo_valido(titulo, descricao):
                stats['tipo_invalido'] += 1
                continue
            
            # Adicionar aos dados válidos
            dados_filtrados.append(imovel)
            stats['validos'] += 1
        
        # Exibir estatísticas
        print("\n📈 Estatísticas da Filtragem:")
        print(f"   • Total de anúncios: {stats['total']}")
        print(f"   • Cessão de direitos: {stats['cessao']}")
        print(f"   • Preço acima do limite: {stats['preco_invalido']}")
        print(f"   • Tipo inválido (não apartamento): {stats['tipo_invalido']}")
        print(f"   • ✅ Anúncios válidos: {stats['validos']}")
        
        return dados_filtrados, cessao_direitos
    
    def salvar_dados_filtrados(self, dados_filtrados: List[Dict], 
                               cessao_direitos: List[Dict],
                               arquivo_principal: str = 'dados_imoveis_londrina.json',
                               arquivo_cessao: str = 'cessao_direitos.json'):
        """
        Salva os dados filtrados em arquivos JSON.
        
        Args:
            dados_filtrados: Lista de imóveis válidos
            cessao_direitos: Lista de imóveis com cessão de direitos
            arquivo_principal: Caminho do arquivo principal
            arquivo_cessao: Caminho do arquivo de cessão
        """
        # Salvar dados principais
        with open(arquivo_principal, 'w', encoding='utf-8') as f:
            json.dump(dados_filtrados, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Dados principais salvos em: {arquivo_principal}")
        print(f"   Total: {len(dados_filtrados)} imóveis")
        
        # Salvar cessão de direitos
        if cessao_direitos:
            with open(arquivo_cessao, 'w', encoding='utf-8') as f:
                json.dump(cessao_direitos, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Cessão de direitos salva em: {arquivo_cessao}")
            print(f"   Total: {len(cessao_direitos)} imóveis")
        else:
            print("ℹ️  Nenhum imóvel de cessão de direitos encontrado")
        
        print("\n✅ Filtragem concluída com sucesso!")
        print("="*80 + "\n")


def main():
    """Função principal para teste do filtrador."""
    filtrador = FiltradorImoveis()
    
    # Aplicar filtros
    dados_filtrados, cessao_direitos = filtrador.filtrar_dados('dados_imoveis_bruto.json')
    
    # Salvar resultados
    filtrador.salvar_dados_filtrados(dados_filtrados, cessao_direitos)
    
    # Exibir amostras
    if dados_filtrados:
        print("\n📋 Amostra de imóveis válidos:")
        for i, imovel in enumerate(dados_filtrados[:3], 1):
            print(f"\n{i}. {imovel.get('nome_empreendimento')} - {imovel.get('bairro')}")
            print(f"   Plataforma: {imovel.get('plataforma')}")
            print(f"   Tipo: {imovel.get('tipo_anuncio')}")
            if imovel.get('preco_venda'):
                print(f"   Preço venda: R$ {imovel.get('preco_venda'):,.2f}")
            if imovel.get('preco_aluguel'):
                print(f"   Preço aluguel: R$ {imovel.get('preco_aluguel'):,.2f}")
    
    if cessao_direitos:
        print("\n📋 Amostra de cessão de direitos:")
        for i, imovel in enumerate(cessao_direitos[:3], 1):
            print(f"\n{i}. {imovel.get('titulo')[:60]}...")
            print(f"   Bairro: {imovel.get('bairro')}")


if __name__ == "__main__":
    main()
