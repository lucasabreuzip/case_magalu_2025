"""
SISTEMA DE CONSUMO DEMOGRÁFICO - ESTADOS VIZINHOS

Sistema automatizado para análise demográfica e econômica dos estados do Nordeste e adjacentes, 
com foco em **Recife** e **Salvador**. Extrai dados oficiais do IBGE para gerar insights estratégicos sobre potencial de mercado.

Autor: Lucas Abreu - lucasabreuzip
GitBuh: https://github.com/lucasabreuzip
Linkedin: https://www.linkedin.com/in/lucasabreuzip/
Versão: 2.0
Data: 09/2025
"""

import requests
import pandas as pd
import time
import os
from datetime import datetime

DATASETS_DIR = "datasets_gerados"
os.makedirs(DATASETS_DIR, exist_ok=True)

# =============================================================================
# CONFIGURAÇÕES E CONSTANTES
# =============================================================================

ESTADOS_VIZINHOS = {
    "Pernambuco": {"codigo": 26, "capital": "Recife", "distancia_recife": 0, "distancia_salvador": 800},
    "Bahia": {"codigo": 29, "capital": "Salvador", "distancia_recife": 800, "distancia_salvador": 0},
    "Paraíba": {"codigo": 25, "capital": "João Pessoa", "distancia_recife": 120, "distancia_salvador": 920},
    "Ceará": {"codigo": 23, "capital": "Fortaleza", "distancia_recife": 800, "distancia_salvador": 1400},
    "Alagoas": {"codigo": 27, "capital": "Maceió", "distancia_recife": 285, "distancia_salvador": 632},
    "Piauí": {"codigo": 22, "capital": "Teresina", "distancia_recife": 1050, "distancia_salvador": 1200},
    "Sergipe": {"codigo": 28, "capital": "Aracaju", "distancia_recife": 632, "distancia_salvador": 356},
    "Minas Gerais": {"codigo": 31, "capital": "Belo Horizonte", "distancia_recife": 1200, "distancia_salvador": 1372},
    "Espírito Santo": {"codigo": 32, "capital": "Vitória", "distancia_recife": 1350, "distancia_salvador": 1200},
    "Goiás": {"codigo": 52, "capital": "Goiânia", "distancia_recife": 1600, "distancia_salvador": 1450},
    "Tocantins": {"codigo": 17, "capital": "Palmas", "distancia_recife": 1400, "distancia_salvador": 1100},
    "Maranhão": {"codigo": 21, "capital": "São Luís", "distancia_recife": 1100, "distancia_salvador": 1050},
    "Rio Grande do Norte": {"codigo": 24, "capital": "Natal", "distancia_recife": 300, "distancia_salvador": 1100},
}

RM_CODES = {29: "2901", 26: "2601", 23: "2301"}  # Salvador, Recife, Fortaleza
FATORES_REGIONAIS = {29: 0.95, 26: 0.88, 23: 0.85, 21: 0.75, 25: 0.82, 24: 0.87, 27: 0.79, 28: 0.84, 22: 0.72}

# =============================================================================
# CLASSE CENTRALIZADA DE APIs IBGE
# =============================================================================

class IBGEApiClient:
    
    @staticmethod
    def _fetch_api(url, timeout=20):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                for item in data[1:]:  # Pula header
                    if item.get('V') and item['V'] not in ['Valor', '..', '-', '...']:
                        return item['V']
        except:
            pass
        return None
    
    @classmethod
    def get_populacao(cls, codigo_estado, nome_estado):         #População por estado (Tabela 6579)
        for ano in [2025, 2024, 2023]:
            url = f"https://apisidra.ibge.gov.br/values/t/6579/n3/{codigo_estado}/v/9324/p/{ano}"
            result = cls._fetch_api(url)
            if result:
                pop = int(result)
                print(f"✅ População {nome_estado}: {pop:,} hab ({ano})")
                return pop
        return None
    
    @classmethod
    def get_pib(cls, codigo_estado, nome_estado):         #PIB por estado (Tabela 5938)

        for ano in [2021, 2020]:
            url = f"https://apisidra.ibge.gov.br/values/t/5938/n3/{codigo_estado}/v/37/p/{ano}"
            result = cls._fetch_api(url)
            if result:
                pib = float(result) * 1000
                print(f"✅ PIB {nome_estado}: R$ {pib:,.0f} ({ano})")
                return pib
        return None
    
    @classmethod
    def get_renda_nacional(cls):  #Rendimento médio nacional via PNAD (Tabela 6387)
        for periodo in ["202304", "202303", "202302"]:
            url = f"https://apisidra.ibge.gov.br/values/t/6387/n1/1/v/5935/p/{periodo}"
            result = cls._fetch_api(url)
            if result:
                renda = float(result)
                print(f"✅ Renda Nacional: R$ {renda:,.0f} ({periodo})")
                return renda
        return 3234
    
    @classmethod
    def get_ipca_rm(cls, codigo_estado, nome_estado):         #IPCA por Região Metropolitana (Tabela 7060)
        rm_codigo = RM_CODES.get(codigo_estado)
        if not rm_codigo:
            return None
        
        for periodo in ["202311", "202310", "202309"]:
            url = f"https://apisidra.ibge.gov.br/values/t/7060/n7/{rm_codigo}/v/69/p/{periodo}"
            result = cls._fetch_api(url)
            if result:
                ipca = float(result)
                print(f"✅ IPCA {nome_estado}: {ipca}% ({periodo})")
                return ipca
        return None

# =============================================================================
# FUNÇÕES DE PROCESSAMENTO
# =============================================================================

#Carrega distâncias reais do CSV gerado pelo script de malha viária
def carregar_distancias_reais():
    arquivo = os.path.join(DATASETS_DIR, "dataset_rotas_nordeste.csv")
    distancias = {}
    
    if os.path.exists(arquivo):
        try:
            df = pd.read_csv(arquivo)
            capitais_estados = {"Salvador": "Bahia", "Recife": "Pernambuco", "Aracaju": "Sergipe",
                              "Maceió": "Alagoas", "João Pessoa": "Paraíba", "Natal": "Rio Grande do Norte",
                              "Fortaleza": "Ceará", "Teresina": "Piauí", "São Luís": "Maranhão",
                              "Belo Horizonte": "Minas Gerais", "Vitória": "Espírito Santo",
                              "Goiânia": "Goiás", "Palmas": "Tocantins"}
            
            for _, row in df.iterrows():
                origem = capitais_estados.get(row['origem'], row['origem'])
                destino = capitais_estados.get(row['destino'], row['destino'])
                dist = row['distancia_km']
                
                if origem not in distancias: distancias[origem] = {}
                if destino not in distancias: distancias[destino] = {}
                distancias[origem][destino] = distancias[destino][origem] = dist
            
            print(f"✅ Distâncias reais carregadas: {len(df)} rotas encontradas")
        except Exception as e:
            print(f"⚠️ Erro ao carregar distâncias: {e}")
    
    return distancias

#Atualiza configuração com distâncias reais
def atualizar_distancias(estados_config, distancias_reais):
    estados_atualizados = {}
    
    for estado, config in estados_config.items():
        novo_config = config.copy()
        tem_dados_reais = False
        
        # Atualizar distâncias para Recife e Salvador
        for base, campo in [("Pernambuco", "recife"), ("Bahia", "salvador")]:
            if base in distancias_reais and estado in distancias_reais[base]:
                novo_config[f'distancia_{campo}'] = round(distancias_reais[base][estado])
                novo_config[f'fonte_distancia_{campo}'] = 'API_Real'
                tem_dados_reais = True
        
        if tem_dados_reais:
            estados_atualizados[estado] = novo_config
            print(f"✅ {estado} incluído (dados API)")
    
    return estados_atualizados

#Calcula renda regional baseada em fatores oficiais
def calcular_renda_regional(renda_nacional, codigo_estado, nome_estado, pib_per_capita):
    fator_regional = FATORES_REGIONAIS.get(codigo_estado, 0.8)
    fator_pib = min(pib_per_capita / 50000, 1.2)
    fator_final = (fator_regional * 0.7) + (fator_pib * 0.3)
    renda = renda_nacional * fator_final
    print(f"✅ Renda {nome_estado}: R$ {renda:,.0f}")
    return renda

#Calcula consumo por classes socioeconômicas
def calcular_consumo_classes(renda_media, populacao, pib_per_capita):

    fator_renda = renda_media / 3100
    fator_pib = min(pib_per_capita / 40000, 1.5)
    
    if fator_renda > 1.2 and fator_pib > 1.1:
        dist = {'A': 0.04, 'B': 0.16, 'C': 0.42, 'D': 0.28, 'E': 0.10}
    elif fator_renda > 0.9:
        dist = {'A': 0.02, 'B': 0.11, 'C': 0.37, 'D': 0.35, 'E': 0.15}
    else:
        dist = {'A': 0.01, 'B': 0.07, 'C': 0.30, 'D': 0.40, 'E': 0.22}
    
    rendas_classe = [26400, 13200, 5280, 2640, 858]  # A, B, C, D, E
    propensoes = [0.85, 0.80, 0.75, 0.70, 0.65]
    
    consumo_total = sum(populacao * perc * renda * prop * 12 / 1e9 
                       for perc, renda, prop in zip(dist.values(), rendas_classe, propensoes))
    return consumo_total

#Calcula score de atratividade de mercado
def calcular_score_atratividade(dados):

    pop_score = min((dados['populacao'] / 8000000) * 25, 25)
    renda_score = min((dados['renda_mensal'] / 3100) * 25, 25)
    classe_score = 10  # Simplificado
    
    dist_recife = dados.get('distancia_recife', 999)
    if dist_recife <= 300: prox_score = 15
    elif dist_recife <= 600: prox_score = 12
    elif dist_recife <= 1000: prox_score = 8
    elif dist_recife <= 1400: prox_score = 4
    else: prox_score = 1
    
    return pop_score + renda_score + classe_score + prox_score

#Processa um estado completo
def processar_estado(estado_nome, config, api_client):

    codigo = config['codigo']
    print(f"\n📊 Processando {estado_nome} (Código IBGE: {codigo})")
    
    # APIs básicas
    populacao = api_client.get_populacao(codigo, estado_nome)
    pib_total = api_client.get_pib(codigo, estado_nome)
    if not populacao or not pib_total:
        return None
    
    pib_per_capita = pib_total / populacao
    
    # IPCA (opcional)
    ipca = api_client.get_ipca_rm(codigo, estado_nome)
    
    # Renda regional
    renda_nacional = api_client.get_renda_nacional()
    renda_mensal = calcular_renda_regional(renda_nacional, codigo, estado_nome, pib_per_capita)
    
    # Consumo e score
    consumo = calcular_consumo_classes(renda_mensal, populacao, pib_per_capita)
    
    resultado = {
        'nome': estado_nome, 'codigo_ibge': codigo, 'capital': config['capital'],
        'populacao': populacao, 'pib_total': pib_total, 'pib_per_capita': pib_per_capita,
        'renda_mensal': renda_mensal, 'consumo_bilhoes': consumo,
        'distancia_recife': config['distancia_recife'], 'distancia_salvador': config['distancia_salvador']
    }
    
    if ipca:
        resultado['ipca_rm'] = ipca
    
    resultado['score_atratividade'] = calcular_score_atratividade(resultado)
    
    print(f"✅ {estado_nome}: Pop {populacao:,} | PIB/cap R${pib_per_capita:,.0f} | Renda R${renda_mensal:,.0f} | Score {resultado['score_atratividade']:.1f}")
    return resultado

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

#Executa análise demográfica otimizada
def main():
    print("=" * 80)
    print("🚀 Análise Demográfica - Estados Vizinhos (Recife e Salvador)")
    print("=" * 80)
    print(f"⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("📡 Coletando dados demográficos via APIs IBGE\n")
    
    # Carregar e atualizar distâncias
    print("🛣️ CARREGANDO DISTÂNCIAS REAIS...")
    distancias_reais = carregar_distancias_reais()
    estados_config = atualizar_distancias(ESTADOS_VIZINHOS, distancias_reais)
    
    print(f"📊 Distâncias Reais: {len(estados_config)}/{len(estados_config)} estados (100% com dados reais)\n")
    
    # Processar estados
    api_client = IBGEApiClient()
    resultados = {}
    
    print("📍 PROCESSANDO ESTADOS:")
    print(f"Analisando {len(estados_config)} estados para ambos os centros...")
    
    for estado_nome, config in estados_config.items():
        if config['distancia_recife'] <= 2500:  # Limite de análise
            resultado = processar_estado(estado_nome, config, api_client)
            if resultado:
                resultados[estado_nome] = resultado
            time.sleep(0.5)  # Rate limiting
    
    # Salvar resultados em CSV
    if resultados:
        dados_csv = []
        for estado, dados in resultados.items():
            dados_csv.append({
                'Estado': estado, 'Codigo_IBGE': dados['codigo_ibge'], 'Populacao': dados['populacao'],
                'PIB_Per_Capita': dados['pib_per_capita'], 'Renda_Mensal': dados['renda_mensal'],
                'Consumo_Bilhoes': dados['consumo_bilhoes'], 'Score_Atratividade': dados['score_atratividade'],
                'Distancia_Recife': dados['distancia_recife'], 'Distancia_Salvador': dados['distancia_salvador']
            })
        
        df = pd.DataFrame(dados_csv)
        arquivo_csv = os.path.join(DATASETS_DIR, f"dataset_demografica_vizinhos_recife_salvador.csv")
        df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig')
        print(f"\n💾 Dataset: {arquivo_csv}")
        print(f"✅ {len(resultados)} estados processados | API IBGE")
    else:
        print("❌ Erro: Nenhum estado processado")
    
    return resultados

if __name__ == "__main__":
    main()