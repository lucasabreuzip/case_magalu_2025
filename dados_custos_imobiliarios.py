"""
SISTEMA DE CUSTOS IMOBILIÁRIOS

Sistema avancado para análise completa de **custos imobiliários** em Recife e Salvador. Coleta dados oficiais do IBGE incluindo PIB,
população, renda, custos de construção e indicadores econômicos para análise de viabilidade imobiliária.

Autor: Lucas Abreu - lucasabreuzip
GitBuh: https://github.com/lucasabreuzip
Linkedin: https://www.linkedin.com/in/lucasabreuzip/
Versão: 2.0
Data: 09/2025
"""
import requests, json, time, os, pandas as pd
from datetime import datetime
from typing import Any, Dict, Optional

# Configuração ultra-compacta
DATASETS_DIR = "datasets_gerados"
os.makedirs(DATASETS_DIR, exist_ok=True)

CONFIG = {
    'Salvador': {'municipio': 2927408, 'estado': 29, 'uf': 'BA', 'rm': '2901', 'coords': (-12.9714, -38.5014)},
    'Recife': {'municipio': 2611606, 'estado': 26, 'uf': 'PE', 'rm': '2601', 'coords': (-8.0476, -34.8770)}
}

# APIs consolidadas - formato: nome: [URLs, parser, multiplicador]
APIS = {
    'populacao': (['https://apisidra.ibge.gov.br/values/t/6579/n6/{municipio}/v/9324/p/last%201'], 'sidra', 1),
    'pib_total': (['https://apisidra.ibge.gov.br/values/t/5938/n6/{municipio}/v/37/p/last%201'], 'sidra', 1000),
    'renda_mensal': (['https://apisidra.ibge.gov.br/values/t/7416/n3/{estado}/v/4705/p/last%201'], 'renda', 1),
    'ipca_regional': (['https://apisidra.ibge.gov.br/values/t/7060/n7/{rm}/v/69/p/last%201'], 'sidra', 1),
    'custo_construcao': (['https://apisidra.ibge.gov.br/values/t/2296/n3/{estado}/v/48/p/last%201'], 'sidra', 1),
    'preco_venda': (['https://apisidra.ibge.gov.br/values/t/2296/n3/{estado}/v/1198/p/last%201'], 'sidra', 1),
    'area_territorial': (['https://apisidra.ibge.gov.br/values/t/1301/n6/{municipio}/v/616/p/last%201'], 'sidra', 1),
    'industria': (['https://apisidra.ibge.gov.br/values/t/5938/n6/{municipio}/v/518/p/last%201'], 'sidra', 1000),
    'servicos': (['https://apisidra.ibge.gov.br/values/t/5938/n6/{municipio}/v/513/p/last%201'], 'sidra', 1000),
    'agropecuaria': (['https://apisidra.ibge.gov.br/values/t/5938/n6/{municipio}/v/517/p/last%201'], 'sidra', 1000),
    'emprego_formal': (['https://apisidra.ibge.gov.br/values/t/6413/n6/{municipio}/v/10441/p/last%201'], 'sidra', 1)
}

class ColetorUltraOtimizado:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Magalu-Ultra/1.0', 'Accept': 'application/json'})
        self.timeout = 12

    def fetch_api(self, url: str) -> Optional[Any]:
        """Método unificado para todas as chamadas de API com retry automático"""
        for tentativa in range(3):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code == 200:
                    return resp.json()
                if resp.status_code >= 500:
                    time.sleep(1 + tentativa * 0.5)
                    continue
                return None
            except Exception:
                time.sleep(0.8 * (tentativa + 1))
        return None

    def parse_universal(self, data: Any, parser_tipo: str, multiplicador: float = 1) -> Optional[float]:
        """Parser unificado inteligente para todos os formatos de resposta"""
        if not data:
            return None
        try:
            # SIDRA padrão - busca valor em estruturas aninhadas
            if parser_tipo == 'sidra':
                if isinstance(data, list):
                    # Formato lista com cabeçalho
                    for item in data[1:] if len(data) > 1 else data:
                        if isinstance(item, dict):
                            valor = item.get('V')
                            if valor and valor not in ['...', '-', '']:
                                return float(valor) * multiplicador
                    # Formato servicodados com séries
                    for item in data:
                        if isinstance(item, dict):
                            # Busca em série
                            if 'serie' in item and isinstance(item['serie'], dict):
                                for periodo in sorted(item['serie'].keys(), reverse=True):
                                    valor = item['serie'][periodo]
                                    if valor and valor not in ['...', '-', '']:
                                        return float(valor) * multiplicador
                            # Busca em resultados
                            if 'resultados' in item:
                                for resultado in item['resultados']:
                                    for serie_obj in resultado.get('series', []):
                                        serie_data = serie_obj.get('serie', {})
                                        for periodo in sorted(serie_data.keys(), reverse=True):
                                            valor = serie_data[periodo]
                                            if valor and valor not in ['...', '-', '']:
                                                return float(valor) * multiplicador
            
            # Renda - converte domiciliar para individual
            elif parser_tipo == 'renda':
                if isinstance(data, list) and len(data) > 1:
                    for item in data[1:]:
                        valor = item.get('V')
                        if valor and valor not in ['...', '-', '']:
                            return float(valor) * 2.1  # Fator de conversão domiciliar
        except Exception:
            pass
        return None

    def coletar_indicador(self, nome: str, contexto: Dict[str, Any]) -> Optional[float]:
        """Coleta um indicador específico usando configuração unificada"""
        if nome not in APIS:
            return None
        
        urls, parser, multiplicador = APIS[nome]
        for url_template in urls:
            try:
                url = url_template.format(**contexto)
                data = self.fetch_api(url)
                valor = self.parse_universal(data, parser, multiplicador)
                if valor is not None:
                    # Formatar saída conforme o tipo
                    if nome == 'populacao':
                        print(f"✅ População: {valor:,.0f} hab")
                    elif nome == 'pib_total':
                        print(f"✅ PIB Total: R$ {valor/1000000000:,.2f} bilhões")
                    elif nome == 'renda_mensal':
                        print(f"✅ Renda Mensal: R$ {valor:,.0f}")
                    elif nome == 'ipca_regional':
                        print(f"✅ IPCA Regional: {valor:.2f}%")
                    elif nome == 'custo_construcao':
                        print(f"✅ Custo Construção/m²: R$ {valor:,.2f}")
                    elif nome == 'preco_venda':
                        print(f"✅ Preço Venda/m²: R$ {valor:,.2f}")
                    elif nome == 'area_territorial':
                        print(f"✅ Área Territorial: {valor:,.2f} km²")
                    elif nome in ['industria', 'servicos', 'agropecuaria']:
                        if valor >= 1000000000:
                            print(f"✅ {nome.title()}: R$ {valor/1000000000:,.2f} bilhões")
                        else:
                            print(f"✅ {nome.title()}: R$ {valor/1000000:,.1f} milhões")
                    elif nome == 'emprego_formal':
                        print(f"✅ Emprego Formal: {valor:,.0f} postos")
                    return valor
            except KeyError:
                continue
            time.sleep(0.3)
        return None

    def processar_cidade(self, cidade: str) -> Dict[str, Any]:
        """Processa uma cidade completa com todos os indicadores"""
        cfg = CONFIG[cidade]
        contexto = {'municipio': cfg['municipio'], 'estado': cfg['estado'], 'rm': cfg['rm']}
        
        print(f"\n📊 Processando {cidade} (Código IBGE: {cfg['municipio']})")
        
        # Coleta todos os indicadores base
        dados = {f'{k}': self.coletar_indicador(k, contexto) for k in APIS.keys()}
        
        # Cálculos derivados
        if dados['pib_total'] and dados['populacao']:
            dados['pib_per_capita'] = dados['pib_total'] / dados['populacao']
            print(f"✅ PIB per Capita: R$ {dados['pib_per_capita']:,.2f}")
        
        if dados['populacao'] and dados['renda_mensal']:
            dados['mercado_potencial_anual'] = dados['populacao'] * dados['renda_mensal'] * 12 * 0.7
            print(f"✅ Potencial de Mercado: R$ {dados['mercado_potencial_anual']/1000000000:,.2f} bilhões")
        
        if dados['area_territorial'] and dados['populacao']:
            dados['densidade_demografica'] = dados['populacao'] / dados['area_territorial']
            print(f"✅ Densidade Demográfica: {dados['densidade_demografica']:,.1f} hab/km²")
        
        # Metadados
        dados.update({
            'cidade': cidade, 'uf': cfg['uf'], 'codigo_municipio': cfg['municipio'],
            'codigo_estado': cfg['estado'], 'regiao_metropolitana': cfg['rm'],
            'latitude': cfg['coords'][0], 'longitude': cfg['coords'][1],
            'data_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fonte_dados': 'IBGE Oficiais'
        })
        
        print(f"✅ {cidade}: Pop {dados['populacao']:,.0f} | PIB/cap R${dados['pib_per_capita']:,.0f} | Renda R${dados['renda_mensal']:,.0f}")
        
        return dados

def executar_coleta():
    """Função principal ultra-compacta"""
    print("=" * 80)
    print("🚀 Coletor Ultra-Otimizado - Dados Custos Imobiliários")
    print("=" * 80)
    print(f"⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("📡 Coletando dados imobiliários via APIs IBGE\n")
    
    coletor = ColetorUltraOtimizado()
    registros = []
    
    print("📍 PROCESSANDO CIDADES:")
    print(f"Analisando {len(CONFIG)} cidades para análise imobiliária...")
    
    for cidade in CONFIG.keys():
        dados = coletor.processar_cidade(cidade)
        registros.append(dados)
        time.sleep(0.8)
    
    if not registros:
        print("❌ Erro: Nenhuma cidade processada")
        return None
    
    # Gerar dataset
    df = pd.DataFrame(registros)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    arquivo = os.path.join(DATASETS_DIR, f'dataset_custos_imobiliario.csv')
    df.to_csv(arquivo, index=False, encoding='utf-8-sig')
    
    print(f"\n💾 Dataset: {arquivo}")
    print(f"✅ {len(registros)} cidades processadas | {len(df.columns)} colunas | APIs IBGE")
    return arquivo

if __name__ == '__main__':
    executar_coleta()