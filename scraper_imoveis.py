#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraper para Extração de Dados de Imóveis
OLX e ZAP Imóveis - Londrina/PR (Zona Sul)

Este módulo realiza a extração REAL de anúncios das plataformas OLX e ZAP Imóveis.
NÃO utiliza dados simulados ou estáticos.

Autor: Sistema de Análise Imobiliária
Data: 2026-01-21
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, parse_qs
import random


class ScraperImoveis:
    """Classe para extração de dados de imóveis de OLX e ZAP Imóveis."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.delay_min = 1
        self.delay_max = 3
    
    def processar_preco(self, texto_preco: str) -> Optional[float]:
        """
        Converte string de preço para número.
        Exemplos: "R$ 460.000" → 460000, "R$ 1.800/mês" → 1800
        """
        if not texto_preco:
            return None
        
        try:
            # Remove espaços e caracteres especiais
            texto_limpo = texto_preco.replace('R$', '').replace('r$', '')
            texto_limpo = texto_limpo.replace('/mês', '').replace('/mes', '')
            texto_limpo = texto_limpo.replace(' ', '').replace('\n', '')
            
            # Remove pontos de milhar e substitui vírgula por ponto
            texto_limpo = texto_limpo.replace('.', '')
            texto_limpo = texto_limpo.replace(',', '.')
            
            # Extrai apenas números e ponto decimal
            match = re.search(r'(\d+\.?\d*)', texto_limpo)
            if match:
                return float(match.group(1))
            
            return None
        except (ValueError, AttributeError):
            return None
    
    def processar_metragem(self, texto_metragem: str) -> Optional[float]:
        """
        Extrai metragem do texto.
        Exemplos: "72 m²" → 72, "85m²" → 85, "72.5 m2" → 72.5
        """
        if not texto_metragem:
            return None
        
        try:
            # Remove espaços e busca por padrão numérico antes de m² ou m2
            match = re.search(r'(\d+\.?\d*)\s*m[²2]', texto_metragem, re.IGNORECASE)
            if match:
                return float(match.group(1))
            
            return None
        except (ValueError, AttributeError):
            return None
    
    def extrair_nome_empreendimento(self, titulo: str, descricao: str = "") -> str:
        """
        Tenta extrair o nome do empreendimento/condomínio do título ou descrição.
        """
        # Padrões comuns: "Residencial X", "Edifício X", "Condomínio X"
        padroes = [
            r'(?:Residencial|residencial)\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç\s]+)',
            r'(?:Edifício|edifício|Edificio|edificio)\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç\s]+)',
            r'(?:Condomínio|condomínio|Condominio|condominio)\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç\s]+)',
            r'(?:Ed\.|ed\.)\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç\s]+)'
        ]
        
        texto_completo = f"{titulo} {descricao}"
        
        for padrao in padroes:
            match = re.search(padrao, texto_completo)
            if match:
                nome = match.group(0).strip()
                # Limita o tamanho do nome
                palavras = nome.split()[:4]
                return ' '.join(palavras)
        
        # Se não encontrar, retorna as primeiras palavras do título
        palavras = titulo.split()[:3]
        return ' '.join(palavras) if palavras else "Não informado"
    
    def extrair_bairro(self, texto_localizacao: str) -> str:
        """
        Extrai o bairro da string de localização.
        """
        if not texto_localizacao:
            return "Não informado"
        
        # Remove "Londrina, " e pega o próximo termo
        texto_limpo = texto_localizacao.replace('Londrina,', '').replace('Londrina -', '')
        texto_limpo = texto_limpo.replace('PR', '').strip()
        
        # Pega a primeira parte (geralmente o bairro)
        partes = texto_limpo.split(',')
        if partes:
            bairro = partes[0].strip()
            return bairro if bairro else "Não informado"
        
        return "Não informado"
    
    def delay_request(self):
        """Adiciona delay aleatório entre requisições."""
        time.sleep(random.uniform(self.delay_min, self.delay_max))
    
    def extrair_olx(self, url_busca: str, tipo_anuncio: str = "venda") -> List[Dict]:
        """
        Extrai anúncios da OLX.
        
        Args:
            url_busca: URL de busca da OLX
            tipo_anuncio: "venda" ou "aluguel"
        
        Returns:
            Lista de dicionários com dados dos imóveis
        """
        print(f"\n🔍 Extraindo dados da OLX ({tipo_anuncio})...")
        anuncios = []
        pagina = 1
        max_paginas = 5  # Limitar a 5 páginas para não sobrecarregar
        
        try:
            while pagina <= max_paginas:
                # Adiciona parâmetro de página
                url_paginada = f"{url_busca}&o={pagina}" if '?' in url_busca else f"{url_busca}?o={pagina}"
                
                print(f"  📄 Processando página {pagina}...")
                self.delay_request()
                
                try:
                    response = self.session.get(url_paginada, timeout=30)
                    response.raise_for_status()
                except requests.RequestException as e:
                    print(f"  ⚠️  Erro ao acessar página {pagina}: {e}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar cards de anúncios na OLX
                # Seletores podem variar - ajustar conforme estrutura real do site
                cards = soup.find_all('a', attrs={'data-ds-component': 'DS-NewAdCard'})
                
                if not cards:
                    # Tentar outros seletores comuns
                    cards = soup.find_all('li', class_=re.compile(r'.*ad-list-item.*', re.I))
                
                if not cards:
                    print(f"  ℹ️  Nenhum anúncio encontrado na página {pagina}")
                    break
                
                for card in cards:
                    try:
                        # Extrair link
                        link_elem = card if card.name == 'a' else card.find('a')
                        link = urljoin('https://www.olx.com.br', link_elem.get('href', '')) if link_elem else None
                        
                        # Extrair título
                        titulo_elem = card.find(['h2', 'h3'], class_=re.compile(r'.*title.*|.*card-title.*', re.I))
                        titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sem título"
                        
                        # Extrair preço
                        preco_elem = card.find(['span', 'p'], class_=re.compile(r'.*price.*', re.I))
                        preco_texto = preco_elem.get_text(strip=True) if preco_elem else None
                        preco = self.processar_preco(preco_texto) if preco_texto else None
                        
                        # Extrair localização
                        loc_elem = card.find(['span', 'p'], class_=re.compile(r'.*location.*|.*address.*', re.I))
                        localizacao = loc_elem.get_text(strip=True) if loc_elem else ""
                        bairro = self.extrair_bairro(localizacao)
                        
                        # Extrair descrição (se disponível no card)
                        desc_elem = card.find(['p', 'span'], class_=re.compile(r'.*description.*|.*text.*', re.I))
                        descricao = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        # Extrair metragem do título ou descrição
                        texto_completo = f"{titulo} {descricao}"
                        metragem = self.processar_metragem(texto_completo)
                        
                        # Validações básicas
                        if not preco or not link:
                            continue
                        
                        # Montar estrutura de dados
                        imovel = {
                            'plataforma': 'OLX',
                            'nome_empreendimento': self.extrair_nome_empreendimento(titulo, descricao),
                            'bairro': bairro,
                            'preco_venda': preco if tipo_anuncio == 'venda' else None,
                            'preco_aluguel': preco if tipo_anuncio == 'aluguel' else None,
                            'metragem': metragem,
                            'titulo': titulo,
                            'descricao': descricao[:200],  # Limitar tamanho
                            'link': link,
                            'tipo_anuncio': tipo_anuncio
                        }
                        
                        anuncios.append(imovel)
                    
                    except Exception as e:
                        print(f"  ⚠️  Erro ao processar anúncio: {e}")
                        continue
                
                print(f"  ✓ Extraídos {len(cards)} anúncios da página {pagina}")
                pagina += 1
                
                # Verificar se há próxima página
                next_page = soup.find('a', attrs={'data-lurker_list_id': 'next_page'})
                if not next_page:
                    break
        
        except Exception as e:
            print(f"  ❌ Erro geral na extração OLX: {e}")
        
        print(f"  ✅ Total extraído da OLX ({tipo_anuncio}): {len(anuncios)} anúncios")
        return anuncios
    
    def extrair_zapimoveis(self, url_busca: str, tipo_anuncio: str = "venda") -> List[Dict]:
        """
        Extrai anúncios do ZAP Imóveis.
        
        Args:
            url_busca: URL de busca do ZAP Imóveis
            tipo_anuncio: "venda" ou "aluguel"
        
        Returns:
            Lista de dicionários com dados dos imóveis
        """
        print(f"\n🔍 Extraindo dados do ZAP Imóveis ({tipo_anuncio})...")
        anuncios = []
        pagina = 1
        max_paginas = 5
        
        try:
            while pagina <= max_paginas:
                # Adiciona parâmetro de página
                separador = '&' if '?' in url_busca else '?'
                url_paginada = f"{url_busca}{separador}pagina={pagina}"
                
                print(f"  📄 Processando página {pagina}...")
                self.delay_request()
                
                try:
                    response = self.session.get(url_paginada, timeout=30)
                    response.raise_for_status()
                except requests.RequestException as e:
                    print(f"  ⚠️  Erro ao acessar página {pagina}: {e}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar cards de anúncios no ZAP
                cards = soup.find_all(['div', 'article'], class_=re.compile(r'.*result-card.*|.*card-container.*', re.I))
                
                if not cards:
                    # Tentar outros seletores
                    cards = soup.find_all('a', attrs={'data-type': 'property'})
                
                if not cards:
                    print(f"  ℹ️  Nenhum anúncio encontrado na página {pagina}")
                    break
                
                for card in cards:
                    try:
                        # Extrair link
                        link_elem = card if card.name == 'a' else card.find('a')
                        link = urljoin('https://www.zapimoveis.com.br', link_elem.get('href', '')) if link_elem else None
                        
                        # Extrair título
                        titulo_elem = card.find(['h2', 'h3', 'span'], class_=re.compile(r'.*card-title.*|.*property-title.*', re.I))
                        titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sem título"
                        
                        # Extrair preço
                        preco_elem = card.find(['p', 'span', 'div'], class_=re.compile(r'.*price.*|.*valor.*', re.I))
                        preco_texto = preco_elem.get_text(strip=True) if preco_elem else None
                        preco = self.processar_preco(preco_texto) if preco_texto else None
                        
                        # Extrair localização/bairro
                        loc_elem = card.find(['p', 'span'], class_=re.compile(r'.*address.*|.*location.*|.*bairro.*', re.I))
                        localizacao = loc_elem.get_text(strip=True) if loc_elem else ""
                        bairro = self.extrair_bairro(localizacao)
                        
                        # Extrair metragem
                        area_elem = card.find(['span', 'li'], attrs={'itemprop': 'floorSize'})
                        if not area_elem:
                            area_elem = card.find(['span', 'li'], class_=re.compile(r'.*area.*|.*m2.*', re.I))
                        
                        metragem_texto = area_elem.get_text(strip=True) if area_elem else ""
                        metragem = self.processar_metragem(metragem_texto) if metragem_texto else None
                        
                        # Se não achou metragem no elemento específico, buscar no título
                        if not metragem:
                            metragem = self.processar_metragem(titulo)
                        
                        # Extrair descrição
                        desc_elem = card.find(['p', 'div'], class_=re.compile(r'.*description.*|.*resumo.*', re.I))
                        descricao = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        # Validações
                        if not preco or not link:
                            continue
                        
                        # Montar estrutura
                        imovel = {
                            'plataforma': 'ZAP Imóveis',
                            'nome_empreendimento': self.extrair_nome_empreendimento(titulo, descricao),
                            'bairro': bairro,
                            'preco_venda': preco if tipo_anuncio == 'venda' else None,
                            'preco_aluguel': preco if tipo_anuncio == 'aluguel' else None,
                            'metragem': metragem,
                            'titulo': titulo,
                            'descricao': descricao[:200],
                            'link': link,
                            'tipo_anuncio': tipo_anuncio
                        }
                        
                        anuncios.append(imovel)
                    
                    except Exception as e:
                        print(f"  ⚠️  Erro ao processar anúncio: {e}")
                        continue
                
                print(f"  ✓ Extraídos {len(cards)} anúncios da página {pagina}")
                pagina += 1
                
                # Verificar próxima página
                next_button = soup.find(['a', 'button'], class_=re.compile(r'.*next.*|.*proxima.*', re.I))
                if not next_button or 'disabled' in next_button.get('class', []):
                    break
        
        except Exception as e:
            print(f"  ❌ Erro geral na extração ZAP: {e}")
        
        print(f"  ✅ Total extraído do ZAP Imóveis ({tipo_anuncio}): {len(anuncios)} anúncios")
        return anuncios
    
    def executar_scraping(self) -> List[Dict]:
        """
        Executa o scraping completo de todas as plataformas.
        
        Returns:
            Lista consolidada com todos os anúncios extraídos
        """
        print("\n" + "="*80)
        print("INICIANDO WEB SCRAPING DE IMÓVEIS")
        print("Londrina/PR - Zona Sul")
        print("="*80)
        
        todos_anuncios = []
        
        # URLs de busca - Ajustar conforme necessário
        urls = {
            'olx_venda': 'https://www.olx.com.br/imoveis/venda/apartamentos/estado-pr/regiao-de-londrina/londrina?pe=700000',
            'olx_aluguel': 'https://www.olx.com.br/imoveis/aluguel/apartamentos/estado-pr/regiao-de-londrina/londrina',
            'zap_venda': 'https://www.zapimoveis.com.br/venda/apartamentos/pr+londrina/?onde=,Paraná,Londrina,,,,,city,BR>Paraná>NULL>Londrina&precoate=700000',
            'zap_aluguel': 'https://www.zapimoveis.com.br/aluguel/apartamentos/pr+londrina/?onde=,Paraná,Londrina,,,,,city,BR>Paraná>NULL>Londrina'
        }
        
        # Extrair OLX - Venda
        try:
            anuncios_olx_venda = self.extrair_olx(urls['olx_venda'], 'venda')
            todos_anuncios.extend(anuncios_olx_venda)
        except Exception as e:
            print(f"❌ Erro na extração OLX (venda): {e}")
        
        # Extrair OLX - Aluguel
        try:
            anuncios_olx_aluguel = self.extrair_olx(urls['olx_aluguel'], 'aluguel')
            todos_anuncios.extend(anuncios_olx_aluguel)
        except Exception as e:
            print(f"❌ Erro na extração OLX (aluguel): {e}")
        
        # Extrair ZAP - Venda
        try:
            anuncios_zap_venda = self.extrair_zapimoveis(urls['zap_venda'], 'venda')
            todos_anuncios.extend(anuncios_zap_venda)
        except Exception as e:
            print(f"❌ Erro na extração ZAP (venda): {e}")
        
        # Extrair ZAP - Aluguel
        try:
            anuncios_zap_aluguel = self.extrair_zapimoveis(urls['zap_aluguel'], 'aluguel')
            todos_anuncios.extend(anuncios_zap_aluguel)
        except Exception as e:
            print(f"❌ Erro na extração ZAP (aluguel): {e}")
        
        print("\n" + "="*80)
        print(f"✅ SCRAPING CONCLUÍDO: {len(todos_anuncios)} anúncios extraídos")
        print("="*80 + "\n")
        
        return todos_anuncios


def main():
    """Função principal para teste do scraper."""
    scraper = ScraperImoveis()
    
    # Executar scraping
    anuncios = scraper.executar_scraping()
    
    # Salvar resultados
    if anuncios:
        with open('dados_imoveis_bruto.json', 'w', encoding='utf-8') as f:
            json.dump(anuncios, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Dados salvos em: dados_imoveis_bruto.json")
        print(f"📊 Total de anúncios: {len(anuncios)}")
        
        # Estatísticas
        vendas = sum(1 for a in anuncios if a['tipo_anuncio'] == 'venda')
        alugueis = sum(1 for a in anuncios if a['tipo_anuncio'] == 'aluguel')
        print(f"   - Vendas: {vendas}")
        print(f"   - Aluguéis: {alugueis}")
    else:
        print("⚠️  Nenhum anúncio foi extraído.")


if __name__ == "__main__":
    main()
