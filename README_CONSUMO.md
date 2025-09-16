# 📊 Sistema de Análise Demográfica - Estados Nordeste

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IBGE API](https://img.shields.io/badge/Data%20Source-IBGE%20API-green.svg)](https://sidra.ibge.gov.br)

Sistema automatizado para análise demográfica e econômica dos estados do Nordeste e adjacentes, com foco em **Recife** e **Salvador**. Extrai dados oficiais do IBGE para gerar insights estratégicos sobre potencial de mercado.

## 🚀 Quick Start

```bash
# Clone e execute
git clone https://github.com/lucasabreuzip/case_magalu_2025.git
cd case_magalu_2025
pip install requests pandas
python dados_consumo_estados_visinhos.py
```

**Output:** Dataset CSV com 13 estados analisados via API IBGE

## 🎯 Features & Use Cases

| Feature | Descrição | Caso de Uso |
|---------|-----------|-------------|
| 🏢 **Análise Demográfica** | População, PIB, renda por estado | Expansão comercial |
| 📊 **Score de Atratividade** | Ranking 0-75 pontos | Priorização de investimentos |
| 🗺️ **Distâncias Reais** | Integração com malha viária | Planejamento logístico |
| 💰 **Classes A-E** | Segmentação socioeconômica | Estratégias de mercado |
| 📈 **Export CSV** | Dados estruturados | Business Intelligence |

## 🏗️ Arquitetura do Código

```python
# Fluxo Principal
main() → processar_estado() → IBGEApiClient → calcular_score_atratividade() → CSV
```

### 🔧 Componentes Core

| Classe/Função | Responsabilidade | APIs IBGE |
|---------------|------------------|-----------|
| `IBGEApiClient` | Coleta dados oficiais | 6579, 5938, 6387, 7060 |
| `processar_estado()` | Orquestra análise completa | - |
| `calcular_score_atratividade()` | Gera ranking 0-75 pontos | - |
| `carregar_distancias_reais()` | Integra malha viária | - |

### 📊 Métricas Calculadas

**Score de Atratividade (0-75 pontos):**
```
🏆 Score = População(25) + Renda(25) + Classes(10) + Proximidade(15)
```

**Segmentação Socioeconômica:**
-  **Classe A** (4%): R$ 26.400/mês
-  **Classe B** (16%): R$ 13.200/mês  
-  **Classe C** (42%): R$ 5.280/mês
-  **Classe D** (28%): R$ 2.640/mês
-  **Classe E** (10%): R$ 858/mês

## 📊 Exemplo de Execução

<details>
<summary>🖥️ <strong>Clique para ver saída completa</strong></summary>

```console
🚀 Análise Demográfica - Estados Vizinhos (Recife e Salvador)
================================================================================
⏰ Início: 16/09/2025 14:30:15
📡 Coletando dados demográficos via APIs IBGE

🛣️ CARREGANDO DISTÂNCIAS REAIS...
✅ Distâncias reais carregadas: 24 rotas encontradas
📊 Distâncias Reais: 13/13 estados (100% com dados reais)

📍 PROCESSANDO ESTADOS:
✅ População Pernambuco: 9,674,793 hab (2025)
✅ PIB Pernambuco: R$ 197,922,000,000 (2021)
✅ Renda Pernambuco: R$ 2,846
✅ Pernambuco: Pop 9,674,793 | PIB/cap R$20,448 | Score 65.2

💾 Dataset: datasets_gerados/dataset_demografica_vizinhos_recife_salvador.csv
✅ 13 estados processados | API IBGE
```
</details>

## 📁 Output & Integração

**Arquivo Gerado:**
```
📂 datasets_gerados/
  └── 📄 dataset_demografica_vizinhos_recife_salvador.csv
```

| Column | Exemplo | Descrição |
|--------|---------|-----------|
| `Estado` | "Pernambuco" | Nome do estado |
| `Populacao` | 9674793 | Habitantes (IBGE 2025) |
| `PIB_Per_Capita` | 20448 | PIB per capita (R$) |
| `Score_Atratividade` | 65.2 | Ranking final (0-75) |
| `Distancia_Recife` | 0 | Distância rodoviária (km) |

## ⚙️ Configuração & APIs

### 🌐 Fontes de Dados IBGE
| API SIDRA | Tabela | Dados Coletados |
|-----------|--------|-----------------|
| 📊 **6579** | Estimativas Populacionais | População por estado |
| 💰 **5938** | PIB Municípios | Produto Interno Bruto |
| 📈 **6387** | PNAD Contínua | Renda média nacional |
| 🏙️ **7060** | IPCA Metropolitano | Inflação regional |

### 🎛️ Fatores Regionais
```python
FATORES_REGIONAIS = {
    29: 0.95,  # 🌴 Bahia - Alto
    26: 0.88,  # 🏠 Pernambuco - Médio-alto  
    23: 0.85,  # 🌊 Ceará - Médio
    21: 0.75,  # 🌾 Maranhão - Médio-baixo
}
```

### 🛡️ Confiabilidade
- ⏱️ **Rate limiting:** 0.5s entre requests
- 🔄 **Fallback:** 3 anos de dados históricos
- ✅ **Error handling:** Retry automático com degradação


## 👤 Autor & Licença

**Lucas Abreu** (@lucasabreuzip)  
🐙 [GitHub](https://github.com/lucasabreuzip) • 💼 [LinkedIn](https://www.linkedin.com/in/lucasabreuzip/)

📄 **Licença:** MIT License

---
**Este projeto foi desenvolvido como parte de um case técnico.**

⭐ **Se este projeto te ajudou, dê uma estrela!** ⭐