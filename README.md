# Sistema de Malha Viária - Análise de Rotas

**Autor:** Lucas Abreu  
**GitHub:** [lucasabreuzip](https://github.com/lucasabreuzip)  
**LinkedIn:** [lucasabreuzip](https://www.linkedin.com/in/lucasabreuzip/)  
**Versão:** 2.0  
**Data:** 09/2025

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Configuração](#configuração)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [API e Dependências](#api-e-dependências)
- [Cache e Performance](#cache-e-performance)
- [Outputs Gerados](#outputs-gerados)
- [Tratamento de Erros](#tratamento-de-erros)
- [Configurações Avançadas](#configurações-avançadas)

## 🎯 Visão Geral

O **Sistema de Malha Viária** é uma aplicação Python avançada para análise otimizada de rotas entre cidades brasileiras, com foco especial no Nordeste. O sistema utiliza a API do GraphHopper para calcular rotas reais, implementa cache inteligente para otimização de performance e gera visualizações interativas das rotas.

### Principais Características:
- ✅ **Processamento Assíncrono**: Utiliza `asyncio` e `aiohttp` para requisições simultâneas
- ✅ **Cache Inteligente**: Sistema de cache com TTL (Time To Live) configurável
- ✅ **Rate Limiting**: Controle automático de taxa de requisições para evitar bloqueios
- ✅ **Mapas Interativos**: Geração de mapas HTML com rotas visualizadas
- ✅ **Cálculo de Custos**: Estimativas de combustível, pedágio e custos totais
- ✅ **Retry Logic**: Sistema robusto de tentativas com backoff exponencial
- ✅ **Configuração Flexível**: Arquivo JSON para personalização completa

## 🚀 Funcionalidades

### 1. **Análise de Rotas**
- Calcula distâncias reais entre cidades usando a API GraphHopper
- Determina tempo de viagem considerando tráfego e condições das estradas
- Calcula velocidade média para cada rota

### 2. **Análise de Custos**
- **Combustível**: Baseado em consumo por km e preço por litro
- **Pedágio**: Estimativa baseada em custos por 100km
- **Custo Total**: Soma de combustível + pedágio

### 3. **Cache Inteligente**
- Armazena resultados em arquivos JSON para evitar requisições desnecessárias
- TTL configurável (padrão: 24 horas, configurado para 168 horas no config.json)
- Limpeza automática de cache expirado
- Validação de integridade dos dados em cache

### 4. **Mapas Interativos**
- Gera mapas HTML usando Folium
- Visualiza rotas completas com polylines
- Marcadores diferenciados para origem (vermelho) e destinos (azul)
- Tooltips informativos com dados de tempo, distância e custo

### 5. **Processamento Assíncrono**
- Múltiplas requisições simultâneas controladas
- Rate limiting para evitar bloqueios da API
- Tratamento robusto de erros e timeouts

## 🏗️ Arquitetura do Sistema

### Componentes Principais:

#### 1. **ConfigurationManager**
- Carrega configurações do `config.json` ou usa padrões
- Valida coordenadas e configurações críticas
- Gerencia acesso seguro a configurações aninhadas

#### 2. **CacheManager**
- Gerencia cache de rotas com validação de TTL
- Salva/carrega dados em formato JSON com timestamp
- Limpeza automática de arquivos expirados

#### 3. **Processamento Assíncrono**
- `get_route_async()`: Busca individual de rota com retry
- `processar_rotas_async()`: Processamento em lote com controle de taxa
- Sistema de retry com backoff exponencial

#### 4. **Geração de Outputs**
- Mapas HTML interativos
- Datasets CSV consolidados
- Logs detalhados de processamento

## ⚙️ Configuração

### Arquivo `config.json`

O sistema é altamente configurável através do arquivo `config.json`:

```json
{
  "capitais": {
    "Salvador": [-12.9714, -38.5014],
    "Recife": [-8.0476, -34.8770],
    // ... outras cidades
  },
  "origens": {
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
  },
  "retry": {
    "max_tentativas": 3,
    "delay_inicial": 1,
    "backoff_multiplicador": 2
  }
}
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GRAPHHOPPER_API_KEY=sua_chave_api_aqui
```

## 📦 Instalação

### 1. **Requisitos do Sistema**
- Python 3.7+
- Conexão com internet para API GraphHopper
- Chave de API do GraphHopper (gratuita disponível)

### 2. **Dependências Python**

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install pandas folium aiohttp polyline python-dotenv
```

### 3. **Configuração da API**

1. Acesse [GraphHopper](https://www.graphhopper.com/) e crie uma conta gratuita
2. Obtenha sua chave de API
3. Crie o arquivo `.env` com sua chave:

```env
GRAPHHOPPER_API_KEY=sua_chave_api_aqui
```

## 🚀 Como Executar

### Execução Simples

```bash
python malha_viaria_otimizado.py
```

### Execução com Log Detalhado

Para debugging e análise detalhada:

```bash
python -u malha_viaria_otimizado.py
```

### Exemplo de Saída Esperada:

```
====== INICIANDO =======
✅ Configurações carregadas : (config.json)
✅ Configurações validadas com sucesso
✅ (API key) carregada da variável do ambiente
================================================================================
Iniciando processamento de rotas (versão assíncrona)
🧹 Removidos 0 arquivos de cache antigos
Processando: Recife
🚗 Buscando rota assíncrona Recife → Salvador (tentativa 1)
✅ Recife → Salvador: 9.99h, 806.7km, R$90.11
💾 Mapa assíncrono salvo como: mapa_entregas_recife.html
Processando: Salvador
✅ Salvador → Recife: 9.99h, 806.7km, R$90.11
💾 Arquivo CSV único salvo como: datasets_gerados/rotas__nordeste.csv
✅ Processamento concluído!
```

## 📁 Estrutura de Arquivos

```
case_magalu_2025/
├── malha_viaria_otimizado.py    # Código principal
├── config.json                  # Configurações do sistema
├── .env                        # Chave da API (criar)
├── requirements.txt            # Dependências (criar se necessário)
├── README.md                   # Esta documentação
├── cache_rotas/               # Cache de rotas (auto-criado)
│   ├── rota_Recife_Salvador.json
│   ├── rota_Salvador_Recife.json
│   └── ...
├── datasets_gerados/          # Outputs CSV (auto-criado)
│   └── rotas__nordeste.csv
└── mapa_entregas_*.html       # Mapas interativos gerados
```

## 🌐 API e Dependências

### GraphHopper API
- **URL Base**: `https://graphhopper.com/api/1/route`
- **Limite Gratuito**: 2.500 requisições/dia
- **Timeout**: 30 segundos por requisição
- **Rate Limit**: Controlado automaticamente pelo sistema

### Bibliotecas Principais:
- **`aiohttp`**: Requisições HTTP assíncronas
- **`pandas`**: Manipulação de dados e geração de CSV
- **`folium`**: Geração de mapas interativos
- **`polyline`**: Decodificação de coordenadas da API
- **`python-dotenv`**: Gerenciamento de variáveis de ambiente

## ⚡ Cache e Performance

### Sistema de Cache:
- **Localização**: Diretório `cache_rotas/`
- **Formato**: JSON com timestamp
- **TTL**: 168 horas (configurável)
- **Validação**: Verificação de integridade dos dados

### Otimizações de Performance:
- **Conexões Simultâneas**: Limitadas a 2 (configurável)
- **Delay entre Requests**: 0.5s para evitar rate limiting
- **Retry com Backoff**: Exponencial para falhas temporárias
- **Timeout Configurável**: 30s por requisição

### Exemplo de Cache:
```json
{
  "distance_km": 806.658371,
  "tempo_h": 9.988949722222221,
  "coords": [[-8.0476, -34.87699], ...],
  "velocidade_media_kmh": 80.75,
  "custo_combustivel": 36.97,
  "custo_pedagio": 53.14,
  "custo_total_estimado": 90.11,
  "timestamp": "2025-09-16T10:30:00.000000"
}
```

## 📊 Outputs Gerados

### 1. **Dataset CSV** (`rotas__nordeste.csv`)
```csv
origem,destino,distancia_km,tempo_horas,velocidade_media_kmh,custo_combustivel,custo_pedagio,custo_total_estimado
Recife,Salvador,806.66,9.99,80.75,36.97,53.14,90.11
Salvador,Recife,806.66,9.99,80.75,36.97,53.14,90.11
```

### 2. **Mapas HTML Interativos**
- Um mapa para cada cidade de origem
- Visualização completa das rotas
- Tooltips com informações detalhadas
- Marcadores diferenciados por tipo

### 3. **Cache de Rotas** (JSON)
- Dados detalhados de cada rota
- Coordenadas completas para visualização
- Métricas calculadas
- Timestamp para controle de TTL

## 🛠️ Tratamento de Erros

### Tipos de Erro Tratados:

1. **Erros de API**:
   - Rate limiting (HTTP 429)
   - Timeouts de conexão
   - Respostas inválidas
   - Falhas de rede

2. **Erros de Cache**:
   - Arquivos corrompidos
   - Cache expirado
   - Permissões de arquivo

3. **Erros de Configuração**:
   - Chave de API ausente
   - Coordenadas inválidas
   - Arquivo de configuração malformado

### Sistema de Retry:
- **Máximo de Tentativas**: 3 (configurável)
- **Delay Inicial**: 1 segundo
- **Backoff Exponencial**: Multiplicador 2x
- **Rate Limit Handling**: Respeita header `Retry-After`

## ⚙️ Configurações Avançadas

### Personalização de Cidades:
Adicione novas cidades no `config.json`:

```json
{
  "capitais": {
    "Nova_Cidade": [-latitude, -longitude]
  }
}
```

### Ajuste de Performance:
```json
{
  "processamento": {
    "conexoes_simultaneas": 2,
    "delay_entre_requests": 0.5,
    "modo_sequencial": true
  }
}
```

### Customização de Custos:
```json
{
  "custos": {
    "consumo_km_por_litro": 12.0,
    "combustivel_por_litro": 5.50,
    "pedagio_por_100km": 15.0
  }
}
```

### Debug e Logging:
```json
{
  "sistema": {
    "debug": true
  }
}
```

## 🚨 Solução de Problemas

### Problemas Comuns:

1. **"GRAPHHOPPER_API_KEY não encontrada"**
   - Verifique se o arquivo `.env` existe
   - Confirme se a chave está correta

2. **Rate Limit Atingido**
   - O sistema trata automaticamente
   - Aumente o delay entre requisições se necessário

3. **Coordenadas Inválidas**
   - Verifique formato: `[latitude, longitude]`
   - Latitude: -90 a 90, Longitude: -180 a 180

4. **Cache Corrompido**
   - Delete a pasta `cache_rotas` para recriá-la
   - O sistema validará automaticamente

### Logs de Debug:
Para ativar logs detalhados, modifique a configuração de logging no código ou configure `debug: true` no config.json.

## 📝 Licença e Contribuições

Este projeto foi desenvolvido como parte de um case técnico. Para contribuições ou dúvidas:

- **Email**: Via LinkedIn
- **GitHub**: [lucasabreuzip](https://github.com/lucasabreuzip)

---

**Nota**: Este sistema foi projetado para ser eficiente, confiável e fácil de usar. Todas as configurações são opcionais e o sistema funcionará com as configurações padrão se necessário.