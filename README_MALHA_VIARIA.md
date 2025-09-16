# 🗺️ Sistema de Malha Viária - Análise de Rotas

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GraphHopper API](https://img.shields.io/badge/API-GraphHopper-green.svg)](https://www.graphhopper.com/)
[![Async Support](https://img.shields.io/badge/Async-Supported-brightgreen.svg)](https://docs.python.org/3/library/asyncio.html)

Sistema avançado para análise otimizada de rotas entre cidades brasileiras com foco no **Nordeste**. Utiliza processamento **assíncrono**, **cache inteligente** e gera **mapas interativos** com cálculos de custos em tempo real via API GraphHopper.

## 🚀 Quick Start

```bash
# Clone e configure
git clone https://github.com/lucasabreuzip/case_magalu_2025.git
cd case_magalu_2025

# Instale dependências
pip install pandas folium aiohttp polyline python-dotenv

# Configure API key
echo "GRAPHHOPPER_API_KEY=sua_chave_api_aqui" > .env

# Execute análise
python dados_malha_viaria.py
```

**Output:** Mapas HTML interativos + Dataset CSV de rotas + Cache otimizado

## 🎯 Features & Use Cases

| Feature | Descrição | Caso de Uso |
|---------|-----------|-------------|
| 🚀 **Processamento Assíncrono** | `asyncio` + `aiohttp` para requisições simultâneas | Análise em larga escala |
| 💾 **Cache Inteligente** | TTL configurável + validação de integridade | Performance otimizada |
| 🗺️ **Mapas Interativos** | Visualização HTML com Folium + polylines | Apresentações executivas |
| 💰 **Cálculo de Custos** | Combustível + pedágio + tempo de viagem | Planejamento logístico |
| 🔄 **Rate Limiting** | Controle automático de requisições | Conformidade com API |

## 🏗️ Arquitetura do Código

```python
# Fluxo Principal
main() → processar_rotas_async() → get_route_async() → CacheManager → Folium Maps
```

### 🔧 Componentes Core

| Classe/Função | Responsabilidade | Tecnologia |
|---------------|------------------|------------|
| `ConfigurationManager` | Gerencia configurações e validações | JSON + dotenv |
| `CacheManager` | Cache inteligente com TTL | JSON + timestamp |
| `get_route_async()` | Requisições assíncronas com retry | aiohttp + asyncio |
| `processar_rotas_async()` | Orquestra processamento em lote | Rate limiting |
| `gerar_mapa_folium()` | Visualização interativa | Folium + polylines |

### 📊 Métricas Calculadas

**Cálculo de Custos:**
```
💰 Custo Total = Combustível + Pedágio
🚗 Combustível = (Distância ÷ Consumo) × Preço/Litro  
🛣️ Pedágio = (Distância ÷ 100) × Taxa Regional
⏱️ Tempo = Distância ÷ Velocidade Média
```

**Performance Assíncrona:**
- ⚡ **Conexões simultâneas:** 2 (configurável)
- 🕐 **Delay entre requests:** 0.5s
- 🔄 **Retry com backoff:** Exponencial 2x
- ⏲️ **TTL Cache:** 168h (7 dias)

## 📊 Exemplo de Execução

<details>
<summary>🖥️ <strong>Clique para ver saída completa</strong></summary>

```console
====== INICIANDO SISTEMA DE MALHA VIÁRIA =======
✅ Configurações carregadas: config.json
✅ Configurações validadas com sucesso
✅ API key GraphHopper carregada do ambiente
================================================================================
🚀 Iniciando processamento de rotas (versão assíncrona)
🧹 Removidos 0 arquivos de cache antigos

📍 PROCESSANDO ROTAS:
🚗 Buscando rota assíncrona Recife → Salvador (tentativa 1)
✅ Recife → Salvador: 9.99h, 806.7km, R$90.11

� Buscando rota assíncrona Salvador → Recife (tentativa 1)  
✅ Salvador → Recife: 9.99h, 806.7km, R$90.11

💾 Mapas gerados:
  📄 mapa_entregas_recife.html
  📄 mapa_entregas_salvador.html

📊 Dataset: datasets_gerados/dataset_rotas_nordeste.csv
✅ Processamento concluído! | GraphHopper API
```
</details>

## 📁 Output & Integração

**Arquivos Gerados:**
```
📂 datasets_gerados/
  └── 📄 dataset_rotas_nordeste.csv

📂 cache_rotas/
  ├── 📄 rota_Recife_Salvador.json
  └── 📄 rota_Salvador_Recife.json

📂 mapas/
  ├── 📄 mapa_entregas_recife.html
  └── 📄 mapa_entregas_salvador.html
```

| Column | Exemplo | Descrição |
|--------|---------|-----------|
| `origem` | "Recife" | Cidade de origem |
| `destino` | "Salvador" | Cidade de destino |
| `distancia_km` | 806.66 | Distância rodoviária real (km) |
| `tempo_horas` | 9.99 | Tempo de viagem (horas) |
| `velocidade_media_kmh` | 80.75 | Velocidade média da rota |
| `custo_total_estimado` | 90.11 | Custo total (R$) |

## ⚙️ Configuração & APIs

### 🌐 API GraphHopper
| Endpoint | Limites | Dados Coletados |
|----------|---------|-----------------|
| 🗺️ **Route API** | 2.500 req/dia (gratuito) | Distância, tempo, coordenadas |
| ⚡ **Timeout** | 30 segundos | Rotas otimizadas |
| 🔄 **Rate Limit** | Auto-controlado | Polylines decodificadas |

### 🎛️ Configuração Principal (config.json)
```json
{
  "capitais": {
    "Salvador": [-12.9714, -38.5014],
    "Recife": [-8.0476, -34.8770]
  },
  "custos": {
    "combustivel_por_litro": 5.5,
    "consumo_km_por_litro": 12,
    "pedagio_por_100km": 15
  },
  "cache": {
    "ttl_horas": 168
  }
}
```

### 🛡️ Confiabilidade
- ⏱️ **Retry Logic:** 3 tentativas com backoff exponencial
- 💾 **Cache TTL:** 168 horas (7 dias)
- � **Rate Limiting:** 0.5s entre requisições
- ✅ **Error Handling:** Timeout e falhas de rede

### 🚀 Performance Assíncrona
```python
CONFIGURACOES_ASYNC = {
    "conexoes_simultaneas": 2,
    "delay_entre_requests": 0.5,
    "timeout_request": 30,
    "max_tentativas_retry": 3
}
```

## � Autor & Licença

**Lucas Abreu** (@lucasabreuzip)  
🐙 [GitHub](https://github.com/lucasabreuzip) • 💼 [LinkedIn](https://www.linkedin.com/in/lucasabreuzip/)

📄 **Licença:** MIT License

---
**Este projeto foi desenvolvido como parte de um case técnico.**

⭐ **Se este projeto te ajudou, dê uma estrela!** ⭐