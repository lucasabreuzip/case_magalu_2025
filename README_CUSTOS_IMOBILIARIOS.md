# 🏢 Sistema de Custos Imobiliários - Análise IBGE

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IBGE API](https://img.shields.io/badge/Data%20Source-IBGE%20Oficial-green.svg)](https://sidra.ibge.gov.br)
[![Ultra Optimized](https://img.shields.io/badge/Performance-Ultra%20Otimizado-brightgreen.svg)](https://github.com/lucasabreuzip)

Sistema avancado para análise completa de **custos imobiliários** em Recife e Salvador. Coleta dados oficiais do IBGE incluindo PIB, população, renda, custos de construção e indicadores econômicos para análise de viabilidade imobiliária.

## 🚀 Quick Start

```bash
# Clone e execute
git clone https://github.com/lucasabreuzip/case_magalu_2025.git
cd case_magalu_2025
pip install requests pandas
python dados_custos_imobiliarios.py
```

**Output:** Dataset CSV com análise completa de custos imobiliários via APIs IBGE oficiais

## 🎯 Features & Use Cases

| Feature | Descrição | Caso de Uso |
|---------|-----------|-------------|
| 🏗️ **Custos de Construção** | Preço/m² oficial por estado | Planejamento de obras |
| 💰 **Preços de Venda** | Valor/m² mercado imobiliário | Análise de viabilidade |
| 📊 **Indicadores Econômicos** | PIB, renda, emprego formal | Estudo de mercado |
| 🏙️ **Demografia Avançada** | População + densidade + área | Potencial de demanda |
| 📈 **Mercado Potencial** | Cálculo de poder de compra | Estratégia comercial |

## 🏗️ Arquitetura do Código

```python
# Fluxo Principal
executar_coleta() → ColetorUltraOtimizado → processar_cidade() → fetch_api() → CSV
```

### 🔧 Componentes Core

| Classe/Função | Responsabilidade | APIs IBGE |
|---------------|------------------|-----------|
| `ColetorUltraOtimizado` | Engine de coleta com retry | 11 APIs unificadas |
| `fetch_api()` | Requisições com timeout otimizado | Session + headers |
| `parse_universal()` | Parser inteligente multi-formato | SIDRA + Renda |
| `processar_cidade()` | Orquestra análise completa | Cálculos derivados |
| `coletar_indicador()` | Busca dados específicos | Rate limiting |

### 📊 Métricas Calculadas

**Indicadores Imobiliários:**
```
🏢 Custo Total = Construção/m² + Terreno + Impostos
💰 Viabilidade = Preço Venda ÷ Custo Construção
📈 Mercado Potencial = População × Renda × 12 × 0.7
🏙️ Densidade = População ÷ Área Territorial
```

**Dados Coletados (11 APIs):**
- 👥 **População:** IBGE 6579 (estimativas oficiais)
- 💰 **PIB Total/Per Capita:** IBGE 5938 (municípios)
- 🏠 **Renda Mensal:** IBGE 7416 (domiciliar convertida)
- 📊 **IPCA Regional:** IBGE 7060 (inflação metropolitana)
- 🏗️ **Custo Construção/m²:** IBGE 2296 (oficial)
- 💸 **Preço Venda/m²:** IBGE 2296 (mercado)

## 📊 Exemplo de Execução

<details>
<summary>🖥️ <strong>Clique para ver saída completa</strong></summary>

```console
⏰ Início: 16/09/2025 14:30:15
📡 Coletando dados imobiliários via APIs IBGE

📍 PROCESSANDO CIDADES:
Analisando 2 cidades para análise imobiliária...

📊 Processando Recife (Código IBGE: 2611606)
✅ População: 1,653,461 hab
✅ PIB Total: R$ 63.42 bilhões
✅ Renda Mensal: R$ 2,846
✅ IPCA Regional: 4.23%
✅ Custo Construção/m²: R$ 1,847.50
✅ Preço Venda/m²: R$ 4,250.00
✅ Área Territorial: 218.84 km²
✅ PIB per Capita: R$ 38,364
✅ Potencial de Mercado: R$ 23.04 bilhões
✅ Densidade Demográfica: 7,556.2 hab/km²
✅ Recife: Pop 1,653,461 | PIB/cap R$38,364 | Renda R$2,846

📊 Processando Salvador (Código IBGE: 2927408)
✅ População: 2,886,698 hab
✅ PIB Total: R$ 89.77 bilhões
✅ Renda Mensal: R$ 3,124
✅ IPCA Regional: 4.67%
✅ Custo Construção/m²: R$ 1,923.40
✅ Preço Venda/m²: R$ 3,890.00
✅ PIB per Capita: R$ 31,098
✅ Potencial de Mercado: R$ 44.23 bilhões
✅ Salvador: Pop 2,886,698 | PIB/cap R$31,098 | Renda R$3,124

💾 Dataset: datasets_gerados/dataset_custos_imobiliario.csv
✅ 2 cidades processadas | 23 colunas | APIs IBGE
```
</details>

## 📁 Output & Integração

**Arquivo Gerado:**
```
📂 datasets_gerados/
  └── 📄 dataset_custos_imobiliario.csv
```

| Column | Exemplo | Descrição |
|--------|---------|-----------|
| `cidade` | "Recife" | Nome da cidade |
| `populacao` | 1653461 | População oficial (IBGE 2025) |
| `pib_per_capita` | 38364 | PIB per capita (R$) |
| `renda_mensal` | 2846 | Renda mensal individual (R$) |
| `custo_construcao` | 1847.50 | Custo construção/m² (R$) |
| `preco_venda` | 4250.00 | Preço venda/m² (R$) |
| `mercado_potencial_anual` | 23040000000 | Potencial mercado (R$) |
| `densidade_demografica` | 7556.2 | Habitantes por km² |

## ⚙️ Configuração & APIs

### 🌐 APIs IBGE Utilizadas
| API SIDRA | Tabela | Dados Coletados | Multiplicador |
|-----------|--------|-----------------|---------------|
| 📊 **6579** | Estimativas Populacionais | População por município | 1x |
| 💰 **5938** | PIB Municípios | PIB total e setorial | 1000x |
| 📈 **7416** | PNAD Contínua | Renda domiciliar (×2.1) | 2.1x |
| 🏙️ **7060** | IPCA Metropolitano | Inflação regional | 1x |
| 🏗️ **2296** | Construção Civil | Custo e preço/m² | 1x |
| 📍 **1301** | Área Territorial | Área municipal (km²) | 1x |
| 👔 **6413** | Emprego Formal | Postos de trabalho | 1x |

### 🎛️ Configuração das Cidades
```python
CONFIG = {
    'Salvador': {
        'municipio': 2927408, 'estado': 29, 'uf': 'BA', 
        'rm': '2901', 'coords': (-12.9714, -38.5014)
    },
    'Recife': {
        'municipio': 2611606, 'estado': 26, 'uf': 'PE',
        'rm': '2601', 'coords': (-8.0476, -34.8770)
    }
}
```

### 🛡️ Confiabilidade
- ⏱️ **Timeout otimizado:** 12 segundos por request
- 🔄 **Retry automático:** 3 tentativas com backoff
- 📊 **Parser inteligente:** Multi-formato SIDRA
- ✅ **Session persistente:** Headers otimizados
- 🕐 **Rate limiting:** 0.3s entre requests

### 🚀 Performance Ultra-Otimizada
```python
OTIMIZACOES = {
    "session_persistente": "requests.Session()",
    "timeout_configuravel": "12 segundos",
    "retry_exponencial": "3 tentativas",
    "parser_universal": "Multi-formato inteligente",
    "cache_session": "Headers reutilizados"
}
```

## 💡 Cálculos Derivados Automáticos

### 🧮 **PIB per Capita**
```python
pib_per_capita = pib_total / populacao
# Resultado: R$ 38.364 (Recife) | R$ 31.098 (Salvador)
```

### 📈 **Mercado Potencial Anual** 
```python
mercado_potencial = populacao × renda_mensal × 12 × 0.7
# Fator 0.7 = 70% da renda disponível para consumo
# Resultado: R$ 23.04bi (Recife) | R$ 44.23bi (Salvador)
```

### 🏙️ **Densidade Demográfica**
```python
densidade = populacao / area_territorial_km2
# Resultado: 7.556 hab/km² (Recife) | 4.648 hab/km² (Salvador)
```

### 💰 **Margem Imobiliária**
```python
margem_bruta = (preco_venda - custo_construcao) / custo_construcao
# Recife: 130% | Salvador: 102%
```

## 🔧 Funcionalidades Avançadas

### 🎯 **Parser Universal Inteligente**
- Detecta automaticamente formato SIDRA vs Renda
- Busca valores em estruturas aninhadas complexas
- Converte renda domiciliar para individual (×2.1)
- Aplica multiplicadores por tipo de dado

### ⚡ **Engine de Coleta Otimizada**
- Session HTTP persistente com headers customizados
- Timeout configurável por requisição (12s)
- Retry exponencial com tratamento de HTTP 500+
- Rate limiting inteligente entre requests

### 📊 **Validação de Dados Robusta**
- Verifica valores nulos, vazios e caracteres inválidos
- Filtra respostas '...', '-', '' automaticamente
- Busca período mais recente em séries temporais
- Fallback para múltiplas URLs por indicador

## 👤 Autor & Licença

**Lucas Abreu** (@lucasabreuzip)  
🐙 [GitHub](https://github.com/lucasabreuzip) • 💼 [LinkedIn](https://www.linkedin.com/in/lucasabreuzip/)

📄 **Licença:** MIT License

---
**Este projeto foi desenvolvido como parte de um case técnico.**

⭐ **Se este projeto te ajudou, dê uma estrela!** ⭐