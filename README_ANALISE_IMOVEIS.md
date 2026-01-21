# 🏢 Sistema de Análise de Oportunidades Imobiliárias - Londrina/PR (Zona Sul)

## 📋 Descrição

Sistema inteligente de análise de mercado imobiliário desenvolvido para identificar oportunidades de investimento em apartamentos na Zona Sul de Londrina/PR. O sistema analisa dados de preços de venda e aluguel para:

- ✅ Identificar **oportunidades de compra abaixo do valor de mercado** (10% ou mais)
- ✅ Calcular **rentabilidade anual projetada (yield)** baseada em dados de aluguel
- ✅ Gerar **relatórios consolidados** por bairro e ranking geral
- ✅ Exportar dados em formato JSON para análises adicionais

## 🎯 Funcionalidades

### 1. Análise de Preços
- Cálculo do preço médio por m² em cada bairro
- Identificação de imóveis com preço 10% ou mais abaixo da média
- Ranking de oportunidades por percentual de desconto

### 2. Análise de Rentabilidade (Yield)
- Cálculo do yield anual bruto: `[(Aluguel Mensal × 12) ÷ Preço de Venda] × 100`
- Classificação automática:
  - 🏆 **EXCELENTE**: ≥8% ao ano
  - 📈 **ALTA RENTABILIDADE**: 6-8% ao ano
  - 💰 **BOA RENTABILIDADE**: 4-6% ao ano
  - 📉 **BAIXA RENTABILIDADE**: <4% ao ano

### 3. Relatórios Detalhados
- Relatório por bairro com estatísticas específicas
- Ranking geral de melhores oportunidades de compra
- Ranking geral de maior rentabilidade
- Exportação de dados em JSON

## 🚀 Como Usar

### Pré-requisitos
- Python 3.7 ou superior
- Nenhuma biblioteca externa é necessária (usa apenas bibliotecas padrão do Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/maatheeuushlv/dio-curso-git-github.git
cd dio-curso-git-github

# Execute o script
python3 analise_imoveis_londrina.py
```

### Uso Básico

O sistema vem com dados de exemplo pré-configurados. Na primeira execução, ele criará automaticamente um arquivo `dados_imoveis_londrina.json` com dados simulados de imóveis.

```bash
python3 analise_imoveis_londrina.py
```

### Adicionando Seus Próprios Dados

Edite o arquivo `dados_imoveis_londrina.json` com os dados reais dos imóveis:

```json
[
  {
    "plataforma": "ZAP Imóveis",
    "bairro": "Gleba Palhano",
    "nome_empreendimento": "Residencial Verona",
    "metragem": 72.0,
    "preco_venda": 460000.0,
    "aluguel_mensal": 2800.0,
    "endereco": "Rua das Orquídeas, 123"
  }
]
```

#### Campos obrigatórios:
- **plataforma**: Nome da plataforma (OLX, ZAP Imóveis, etc.)
- **bairro**: Nome do bairro da Zona Sul
- **nome_empreendimento**: Nome do condomínio/edifício
- **metragem**: Área em metros quadrados (m²)
- **preco_venda**: Preço de venda em reais (R$)

#### Campos opcionais:
- **aluguel_mensal**: Valor do aluguel mensal em reais (necessário para cálculo de yield)
- **endereco**: Endereço completo do imóvel

## 📊 Exemplo de Saída

```
================================================================================
RELATÓRIO CONSOLIDADO - ANÁLISE DE OPORTUNIDADES IMOBILIÁRIAS
LONDRINA/PR - ZONA SUL
================================================================================

📍 Bairros analisados: Alto da Boa Vista, Gleba Palhano, Jardim Shangri-lá, Lago Parque
📊 Total de imóveis: 12

================================================================================
ANÁLISE DO BAIRRO: GLEBA PALHANO
================================================================================

📊 Estatísticas Gerais:
   • Total de imóveis analisados: 3
   • Preço médio por m²: R$ 7,361.11

💰 Oportunidades de Compra (≥10% abaixo do mercado):
   Total: 1 imóvel(is)

   1. Residencial Verona
      • Plataforma: ZAP Imóveis
      • Metragem: 72 m²
      • Preço de venda: R$ 460,000.00
      • Preço por m²: R$ 6,388.89
      • Preço médio do bairro: R$ 7,361.11/m²
      • 🎯 ABAIXO DO MERCADO: 13.21%

📈 Análise de Rentabilidade (Yield Anual Bruto):
   Total: 3 imóvel(is) com dados de aluguel

   1. Residencial Verona
      • Plataforma: ZAP Imóveis
      • Metragem: 72 m²
      • Preço de venda: R$ 460,000.00
      • Aluguel mensal: R$ 2,800.00
      • Yield Bruto: 7.30% ao ano
      • 🏆 Classificação: ALTA RENTABILIDADE (6-8%)
```

## 🗺️ Bairros da Zona Sul de Londrina/PR

O sistema está otimizado para análise dos seguintes bairros da Zona Sul:

- Gleba Palhano
- Alto da Boa Vista
- Jardim Shangri-lá
- Lago Parque
- Parque das Nações
- Jardim Petrópolis
- Entre outros bairros da região sul

## 📁 Arquivos Gerados

Após a execução, o sistema gera os seguintes arquivos:

1. **dados_imoveis_londrina.json**: Dados de entrada com informações dos imóveis
2. **oportunidades.json**: Arquivo com todas as oportunidades identificadas, incluindo:
   - Dados do imóvel
   - Preço médio do bairro
   - Percentual abaixo do mercado
   - Yield anual (quando disponível)

## 🔍 Metodologia de Análise

### Identificação de Oportunidades
Um imóvel é considerado uma oportunidade quando:
- Seu preço por m² está **10% ou mais abaixo** do preço médio do bairro
- Quanto maior o percentual abaixo do mercado, melhor a oportunidade

### Cálculo do Yield
O yield anual bruto é calculado pela fórmula:
```
Yield (%) = [(Aluguel Mensal × 12) ÷ Preço de Venda] × 100
```

**Exemplo:**
- Preço de venda: R$ 520.000
- Aluguel mensal: R$ 3.200
- Yield: [(3.200 × 12) ÷ 520.000] × 100 = 7,38% ao ano

## 🌐 Fontes de Dados

As informações devem ser consultadas nas seguintes plataformas:

1. **OLX**: https://www.olx.com.br/
   - Filtrar por: Londrina/PR > Zona Sul > Apartamentos
   
2. **ZAP Imóveis**: https://www.zapimoveis.com.br/
   - Filtrar por: Londrina/PR > Zona Sul > Apartamentos à venda

## 📝 Notas Importantes

1. **Dados Simulados**: Os dados de exemplo são fictícios e servem apenas para demonstração do sistema
2. **Dados Reais**: Para análises reais, substitua os dados de exemplo por informações coletadas das plataformas OLX e ZAP Imóveis
3. **Yield Líquido**: O yield calculado é bruto e não considera impostos, taxas condominiais, manutenção, etc.
4. **Due Diligence**: Este sistema é uma ferramenta de triagem. Sempre realize análise completa antes de investir

## 🤝 Contribuindo

Este projeto faz parte do curso de Git e GitHub da DIO. Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é parte do material educativo do curso de Git e GitHub da Digital Innovation One (DIO).

## 👨‍💻 Autor

Sistema desenvolvido como parte do repositório educacional **dio-curso-git-github**.

## 🔗 Links Úteis

- [Repositório Original](https://github.com/maatheeuushlv/dio-curso-git-github)
- [DIO - Digital Innovation One](https://www.dio.me/)
- [OLX](https://www.olx.com.br/)
- [ZAP Imóveis](https://www.zapimoveis.com.br/)

---

**Feito com 💙 para análise de investimentos imobiliários em Londrina/PR**
