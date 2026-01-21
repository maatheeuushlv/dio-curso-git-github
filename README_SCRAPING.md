# 🏢 Sistema Automatizado de Análise de Oportunidades Imobiliárias

## 🎯 Londrina/PR - Zona Sul | Web Scraping REAL

Sistema completo que realiza **extração automática de dados reais** das plataformas OLX e ZAP Imóveis para identificar oportunidades de investimento em apartamentos.

---

## ⚡ Características Principais

### ✅ Web Scraping REAL
- **Extração automática** de anúncios de OLX e ZAP Imóveis
- **NÃO utiliza dados simulados** - todos os dados vêm de scraping em tempo real
- Suporte a paginação para coletar múltiplas páginas de resultados
- Headers HTTP apropriados e delays entre requisições

### ✅ Filtragem Inteligente
- **Separação de "Cessão de Direitos"** em arquivo específico
- **Filtro de preço**: Apenas imóveis ≤ R$ 700.000
- **Filtro de tipo**: Exclusivamente apartamentos (exclui casas, terrenos, etc.)
- Validação automática de dados

### ✅ Análise de Oportunidades
- Identificação de imóveis **10% ou mais abaixo do valor de mercado**
- Cálculo de preço médio por m² por bairro
- Ranking de melhores oportunidades

### ✅ Cálculo de Rentabilidade (Yield)
- Fórmula: `[(Aluguel Médio × 12) ÷ Preço de Venda] × 100`
- Classificação automática (Excelente, Alta, Boa, Baixa)
- Aluguel médio calculado por bairro

### ✅ Relatórios Consolidados
- **Formato JSON** - Dados estruturados
- **Formato Markdown** - Relatório legível e formatado
- Top 10 oportunidades e rentabilidades

---

## 📋 Pré-requisitos

### Python 3.7+
```bash
python3 --version
```

### Dependências
```bash
pip install -r requirements.txt
```

**Principais bibliotecas:**
- `requests` - Requisições HTTP
- `beautifulsoup4` - Parsing de HTML
- `lxml` - Parser HTML rápido

---

## 🚀 Como Usar

### 1. Instalação

```bash
# Clone o repositório
git clone https://github.com/maatheeuushlv/dio-curso-git-github.git
cd dio-curso-git-github

# Instale as dependências
pip install -r requirements.txt
```

### 2. Execução Completa

```bash
# Executar o sistema completo (scraping + filtragem + análise)
python3 main_scraping.py
```

O sistema irá:
1. ✅ Executar web scraping de OLX e ZAP Imóveis
2. ✅ Filtrar e validar os dados extraídos
3. ✅ Identificar oportunidades de compra
4. ✅ Calcular rentabilidade (yield)
5. ✅ Gerar relatórios consolidados

### 3. Execução Modular

Você também pode executar cada módulo separadamente:

```bash
# Apenas scraping
python3 scraper_imoveis.py

# Apenas filtragem (requer dados_imoveis_bruto.json)
python3 filtrador_imoveis.py

# Análise com dados já filtrados
python3 analise_imoveis_londrina.py
```

---

## 📁 Arquivos Gerados

### Durante a execução:

1. **`dados_imoveis_bruto.json`**
   - Dados extraídos diretamente via scraping
   - Sem filtragem ou validação

2. **`dados_imoveis_londrina.json`**
   - Dados filtrados e validados
   - Apenas apartamentos válidos ≤ R$ 700.000

3. **`cessao_direitos.json`**
   - Imóveis identificados como "cessão de direitos"
   - Separados para análise específica

4. **`relatorio_final.json`**
   - Relatório estruturado em JSON
   - Top 10 oportunidades e yields

5. **`relatorio_final.md`**
   - Relatório formatado em Markdown
   - Legível e pronto para compartilhamento

---

## 🔍 Estrutura dos Dados Extraídos

### Formato de cada imóvel:

```json
{
  "plataforma": "ZAP Imóveis",
  "nome_empreendimento": "Residencial Verona",
  "bairro": "Gleba Palhano",
  "preco_venda": 460000,
  "preco_aluguel": null,
  "metragem": 72,
  "titulo": "Apartamento 2 quartos à venda - Gleba Palhano",
  "descricao": "Apartamento moderno com 2 quartos...",
  "link": "https://www.zapimoveis.com.br/...",
  "tipo_anuncio": "venda"
}
```

---

## 📊 Critérios de Análise

### Oportunidades de Compra
- **Critério:** Imóveis com preço ≥10% abaixo da média do bairro
- **Cálculo:** Preço médio por m² do bairro vs. preço do imóvel
- **Resultado:** Lista ordenada por percentual de desconto

### Rentabilidade (Yield)
- **Fórmula:** `[(Aluguel Médio Mensal × 12) ÷ Preço de Venda] × 100`
- **Classificação:**
  - 🏆 Excelente: ≥8% ao ano
  - 📈 Alta: 6-8% ao ano
  - 💰 Boa: 4-6% ao ano
  - 📉 Baixa: <4% ao ano

---

## 🛠️ Módulos do Sistema

### 1. `scraper_imoveis.py`
**Web scraper principal**
- Classe `ScraperImoveis`
- Métodos para extração de OLX e ZAP Imóveis
- Processamento de preços e metragens
- Paginação automática

### 2. `filtrador_imoveis.py`
**Filtro e validação de dados**
- Classe `FiltradorImoveis`
- Separação de cessão de direitos
- Filtro de preço máximo
- Validação de tipo de imóvel

### 3. `main_scraping.py`
**Orquestrador principal**
- Integra scraping, filtragem e análise
- Funções `analisar_oportunidades()` e `calcular_yield()`
- Geração de relatórios consolidados

### 4. `analise_imoveis_londrina.py`
**Sistema de análise original**
- Mantido para compatibilidade
- Pode trabalhar com dados simulados ou reais

---

## ⚙️ Configurações

### Ajustar URLs de busca

Edite as URLs em `scraper_imoveis.py` no método `executar_scraping()`:

```python
urls = {
    'olx_venda': 'https://www.olx.com.br/imoveis/venda/apartamentos/...',
    'olx_aluguel': 'https://www.olx.com.br/imoveis/aluguel/apartamentos/...',
    'zap_venda': 'https://www.zapimoveis.com.br/venda/apartamentos/...',
    'zap_aluguel': 'https://www.zapimoveis.com.br/aluguel/apartamentos/...'
}
```

### Ajustar filtros

Edite `filtrador_imoveis.py`:

```python
self.valor_maximo = 700000.0  # Alterar valor máximo
self.palavras_cessao = [...]  # Adicionar palavras-chave
self.palavras_exclusao_tipo = [...]  # Adicionar tipos a excluir
```

### Ajustar limites de paginação

Em `scraper_imoveis.py`:

```python
max_paginas = 5  # Alterar número máximo de páginas
```

---

## 🔒 Considerações Legais e Éticas

### ⚠️ IMPORTANTE

1. **Respeite os Termos de Uso** das plataformas
2. **Verifique robots.txt** antes de executar scraping
3. **Use delays apropriados** entre requisições (1-3 segundos)
4. **Não sobrecarregue** os servidores das plataformas
5. **Use os dados de forma ética** e legal

### Robots.txt
Sempre verifique:
- https://www.olx.com.br/robots.txt
- https://www.zapimoveis.com.br/robots.txt

### Rate Limiting
O sistema implementa delays automáticos:
```python
self.delay_min = 1  # segundos
self.delay_max = 3  # segundos
```

---

## 🐛 Troubleshooting

### Problema: Nenhum anúncio extraído

**Possíveis causas:**
1. Estrutura HTML dos sites mudou
2. Bloqueio por User-Agent
3. Conexão com internet

**Solução:**
- Inspecione as páginas e atualize os seletores CSS
- Verifique se os sites estão acessíveis
- Use diferentes User-Agents

### Problema: Erro de importação

```bash
ModuleNotFoundError: No module named 'requests'
```

**Solução:**
```bash
pip install -r requirements.txt
```

### Problema: Timeout nas requisições

**Solução:**
- Aumente o timeout: `response = self.session.get(url, timeout=60)`
- Verifique sua conexão com internet

---

## 📈 Exemplos de Saída

### Oportunidade Identificada:
```
1. Residencial Villa Verde - Gleba Palhano
   • Plataforma: ZAP Imóveis
   • Preço: R$ 420,000.00
   • Metragem: 75 m²
   • Preço/m²: R$ 5,600.00
   • Preço médio do bairro: R$ 6,635.52/m²
   • 🎯 Abaixo do mercado: 15.61%
```

### Cálculo de Yield:
```
1. Apartamento Vista Alegre - Alto da Boa Vista
   • Plataforma: OLX
   • Preço: R$ 340,000.00
   • Aluguel médio do bairro: R$ 2,250.00/mês
   • 🏆 Yield: 7.94% ao ano
   • Classificação: Alta rentabilidade (6-8%)
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto faz parte do material educativo do curso de Git e GitHub da Digital Innovation One (DIO).

---

## 👨‍💻 Autor

Sistema desenvolvido como parte do repositório educacional **dio-curso-git-github**.

---

## 🔗 Links Úteis

- [Repositório](https://github.com/maatheeuushlv/dio-curso-git-github)
- [DIO - Digital Innovation One](https://www.dio.me/)
- [OLX](https://www.olx.com.br/)
- [ZAP Imóveis](https://www.zapimoveis.com.br/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)

---

**Feito com 💙 para análise automatizada de investimentos imobiliários em Londrina/PR**
