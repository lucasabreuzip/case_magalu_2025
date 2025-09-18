# 🧠 Análise com Inteligência Artificial - Centro de Distribuição Magalu

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Powered](https://img.shields.io/badge/AI-Machine%20Learning-red.svg)](https://scikit-learn.org)
[![Fuzzy Logic](https://img.shields.io/badge/Fuzzy-Logic%20System-orange.svg)](https://github.com/scikit-fuzzy/scikit-fuzzy)
[![Ultra Optimized](https://img.shields.io/badge/Performance-Ultra%20Otimizado-brightgreen.svg)](https://github.com/lucasabreuzip)

Sistema avançado de **Inteligência Artificial** para análise estratégica de localização para novos centros de distribuição. Combina Machine Learning, Fuzzy Logic e algoritmos genéticos para determinar a melhor cidade entre Recife e Salvador para o o novo CD da Magalu.

## 🚀 Quick Start

```bash
# Clone e execute
git clone https://github.com/lucasabreuzip/case_magalu_2025.git
cd case_magalu_2025
pip install pandas numpy scikit-learn scikit-fuzzy scipy
python ia_analise.py
```

**Output:** Análise completa com recomendação de IA baseada em 23+ variáveis e 4 metodologias avançadas

## 🎯 Features & Use Cases

| Feature | Descrição | Caso de Uso |
|---------|-----------|-------------|
| 🧠 **Machine Learning Ensemble** | 4 modelos com validação cruzada | Predição robusta |
| 🔀 **Fuzzy Logic System** | 13 regras de inferência calibradas | Análise logística |
| 🧬 **Algoritmo Genético** | Otimização automática de pesos | Balanceamento decisório |
| 📊 **Análise Multicomponente** | 23+ variáveis econômicas | Decisão fundamentada |
| 🎯 **Scoring Inteligente** | Normalização robusta + pesos adaptativos | Alta precisão |

## 🏗️ Arquitetura do Código

```python
# Fluxo Principal IA
executar_analise_completa() → AnalisadorCDMagaluCalibrado → ResultadoIA → JSON
```

### � Componentes Core

| Classe/Função | Responsabilidade | Metodologia IA |
|---------------|------------------|----------------|
| `AnalisadorCDMagaluCalibrado` | Engine principal de análise | Ensemble + Fuzzy + GA |
| `analisar_custos_economicos()` | Análise econômica multicomponente | 5 fatores ponderados |
| `analisar_logistica_fuzzy_calibrado()` | Sistema de inferência fuzzy | 13 regras calibradas |
| `treinar_ensemble_calibrado()` | Machine Learning ensemble | 4 modelos + CV |
| `otimizar_pesos_balanceado()` | Algoritmo genético | Differential Evolution |

### 📊 Metodologias IA Implementadas

**Sistema Fuzzy Logic:**
```
🎯 Variáveis: Distância (0-1500km) + Tempo (0-25h) + Custo (0-1500R$)
🔀 Funções: [excelente, boa, regular, ruim] × 3 variáveis
🧠 Regras: 13 regras de inferência calibradas
📈 Output: Eficiência logística (0-100%)
```

**Machine Learning Ensemble:**
- 🌳 **Decision Tree:** max_depth=3, min_samples=10
- 🌲 **Random Forest:** 30 estimators, depth=4
- 🚀 **Gradient Boost:** 30 est, lr=0.1, subsample=0.8
- 🧠 **Neural Network:** (15,10) layers, relu, α=0.1

## � Exemplo de Execução

<details>
<summary>🖥️ <strong>Clique para ver saída completa</strong></summary>

```console
======================================================================
ANÁLISE COM INTELIGÊNCIA ARTIFICIAL
Centro de Distribuição Magalu - Nordeste
======================================================================

Carregando e validando datasets...
   ✓ custos: 2 registros, 9 colunas
   ✓ demografia: 12 registros, 8 colunas
   ✓ rotas: 24 registros, 6 colunas

Executando validações de sanidade...
   Custo construção - Recife: R$ 1848/m²
   Custo construção - Salvador: R$ 1923/m²
   Rotas de Recife: 12, Dist média: 734km
   Rotas de Salvador: 12, Dist média: 823km

Analisando Custos e Economia...
   Score Recife: 0.847 (Custo: 1.00, ROI: 0.92)
   Score Salvador: 0.775 (Custo: 0.96, ROI: 0.78)

Aplicando Fuzzy Logic Calibrado para Logística...
   Eficiência Recife: 78.3% (Dist média: 734km)
   Eficiência Salvador: 69.7% (Dist média: 823km)

Analisando Demografia e Mercado Regional (Corrigido)...
   População 500km de Recife (excl. PE): 8.2M
   População 500km de Salvador (excl. BA): 6.7M
   Score Final Mercado - Recife: 0.623
   Score Final Mercado - Salvador: 0.377

Treinando Ensemble Calibrado...
   Scores CV: neural=0.842, arvore=0.765, random_forest=0.823, gradient_boost=0.798
   Ensemble - Recife: 0.834, Salvador: 0.712

Otimizando pesos com balanceamento...
   Pesos balanceados:
      Custos_Economia: 32.1%
      Logistica_Fuzzy: 28.7%
      Mercado_Regional: 24.3%
      ML_Ensemble: 14.9%

======================================================================
RESULTADO FINAL DA ANÁLISE
======================================================================

CIDADE RECOMENDADA: RECIFE
Vantagem: 7.2%

SCORES FINAIS:
   Recife:   0.847 ⭐
   Salvador: 0.775

Confiança na Decisão: 78.4%

PRINCIPAIS FATORES DECISIVOS:
   1. Custo de construção 15.3% menor em Recife (peso: 32.1%)
   2. Eficiência logística 8.6% superior em Recife
   3. Distância média 89km menor de Recife
   4. ROI 18.0% superior em Recife
   5. População 1.5M maior em 500km de Recife

💾 Resultados salvos em 'resultado_analise_calibrada_magalu.json'
```
</details>

## 📁 Output & Integração

**Arquivo Gerado:**
```
� datasets_gerados/
  └── 📄 resultado_analise_calibrada_magalu.json
```

| Campo | Exemplo | Descrição |
|-------|---------|-----------|
| `cidade_recomendada` | "RECIFE" | Decisão final da IA |
| `score_recife` | 0.847 | Score final normalizado (0-1) |
| `score_salvador` | 0.775 | Score final normalizado (0-1) |
| `vantagem_percentual` | 7.2 | Diferença percentual entre scores |
| `confianca` | 0.784 | Nível de confiança (0-1) |
| `fatores_decisivos` | ["Custo 15.3% menor", ...] | Top 5 fatores identificados |
| `pesos_otimizados` | {"Custos_Economia": 0.321, ...} | Pesos balanceados por categoria |
| `metodologias` | ["Fuzzy Logic", "ML Ensemble", ...] | Técnicas IA utilizadas |

## ⚙️ Configuração & Datasets

### 📊 Datasets Processados
| Dataset | Registros | Colunas | Fonte |
|---------|-----------|---------|-------|
| **dataset_custos_imobiliario.csv** | 2 cidades | 9 vars | APIs IBGE |
| **dataset_rotas_nordeste.csv** | 24 rotas | 6 vars | Graphhopper API |
| **dataset_demografica_vizinhos_recife_salvador.csv** | 12 estados | 8 vars | IBGE + Cálculos |

### 🎛️ Configuração de Modelos IA
```python
MODELOS_CONFIG = {
    'neural': {
        'hidden_layer_sizes': (15, 10),
        'activation': 'relu',
        'alpha': 0.1,
        'early_stopping': True
    },
    'random_forest': {
        'n_estimators': 30,
        'max_depth': 4,
        'min_samples_split': 10
    }
}
```

### 🛡️ Confiabilidade & Validação
- 🔄 **Validação cruzada:** 5-fold para todos os modelos
- 📊 **Data augmentation:** 50 variações ±2% ruído
- ⚖️ **Pesos balanceados:** 15%-40% por categoria
- 🎯 **Normalização robusta:** RobustScaler anti-outliers
- 🕐 **Margem de empate:** 3% para decisões ambíguas

### 🚀 Performance Ultra-Otimizada
```python
OTIMIZACOES_IA = {
    "ensemble_weighting": "CV-score baseado",
    "genetic_algorithm": "200 iterações balanceadas",
    "fuzzy_calibration": "13 regras otimizadas",
    "robust_normalization": "Anti-outliers scaling",
    "early_stopping": "Neural network convergência"
}
```

## 💡 Cálculos IA Automáticos

### 🧮 **Score Econômico Multicomponente**
```python
score_final = (custo_norm * 0.30) + (roi_norm * 0.25) + 
              (pib_norm * 0.15) + (mercado_norm * 0.20) + 
              (densidade_norm * 0.10)
# Resultado: 0.847 (Recife) | 0.775 (Salvador)
```

### 🔀 **Eficiência Fuzzy Logic**
```python
# Sistema com 13 regras calibradas
if distancia='excelente' AND tempo='rapido' AND custo='baixo':
    eficiencia = 'muito_alta'
# Resultado: 78.3% (Recife) | 69.7% (Salvador)
```

### 🧠 **Ensemble ML Ponderado**
```python
ensemble_score = Σ(modelo_score × cv_score) / Σ(cv_scores)
# Neural: 0.842 | Tree: 0.765 | RF: 0.823 | GB: 0.798
# Resultado: 0.834 (Recife) | 0.712 (Salvador)
```

### 🧬 **Otimização Genética de Pesos**
```python
# Differential Evolution (200 iter, pop=20)
objetivo = max_diferenca - penalidade_desbalanco
bounds = [(0.15, 0.40)] * num_categorias
# Resultado: Custos=32.1%, Logística=28.7%, Mercado=24.3%, ML=14.9%
```

## 🔧 Funcionalidades Avançadas

### 🎯 **Sistema Fuzzy Inteligente**
- 3 variáveis de entrada (distância, tempo, custo)
- 13 regras de inferência calibradas para logística
- Membership functions otimizadas para Nordeste
- Bônus automático para destinos próximos (<500km)

### ⚡ **Engine ML Multi-Modelo**
- Ensemble de 4 algoritmos com pesos adaptativos
- Validação cruzada 5-fold para robustez
- Data augmentation com ruído gaussiano ±2%
- Early stopping para evitar overfitting

### 📊 **Algoritmo Genético Balanceado**
- Otimização global com Differential Evolution
- Restrições de peso (15%-40%) para balanceamento
- Função objetivo: maximizar diferença - penalizar extremos
- Convergência garantida em 200 iterações

## � Autor & Licença

**Lucas Abreu** (@lucasabreuzip)  
🐙 [GitHub](https://github.com/lucasabreuzip) • 💼 [LinkedIn](https://www.linkedin.com/in/lucasabreuzip/)

📄 **Licença:** MIT License

---
**Este projeto foi desenvolvido como parte de um case técnico.**

⭐ **Se este projeto te ajudou, dê uma estrela!** ⭐