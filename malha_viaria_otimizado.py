"""
SISTEMA DE MALHA VIÁRIA

Sistema para análise de rotas entre cidades utilizando GraphHopper API.
Suporta cache inteligente, processamento assíncrono e geração de mapas interativos.

Autor: Lucas Abreu
GitBuh: https://github.com/lucasabreuzip
Linkedin: https://www.linkedin.com/in/lucasabreuzip/
Versão: 2.0
Data: 09/2025
"""

import os
import json
import polyline
import folium
import pandas as pd
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import sys
from dotenv import load_dotenv

# ==============================================================
# CONFIGURAÇÕES GLOBAIS E CONSTANTES
# ==============================================================

VERSION = "2.0"
SYSTEM_NAME = "SISTEMA DE MALHA VIÁRIA - LUCAS ABREU"

# Configurações de encoding para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================
# CONFIGURAÇÃO DE LOGGING
# ==============================================================

def configurar_logging(nivel: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, nivel.upper()),
        format='%(message)s', 
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)


logger = configurar_logging()
logger.info("====== INICIANDO =======")

# ==============================================================
# GERENCIAMENTO DE CONFIGURAÇÕES
# ==============================================================

class ConfigurationManager:
    
    
    def __init__(self):
        self.config = self._carregar_configuracoes()
        self._validar_configuracoes()
    
    #Carrega configurações do arquivo JSON ou usa valores padrão
    def _carregar_configuracoes(self) -> Dict:

        config_padrao = {
            "sistema": {
                "versao": VERSION,
                "nome": SYSTEM_NAME,
                "debug": False
            },
            "origens": {
                "Recife": [-8.0476, -34.8770],
                "Salvador": [-12.9714, -38.5014]
            },
            "capitais": {
                "Fortaleza": [-3.7319, -38.5267],
                "Natal": [-5.7945, -35.2110],
                "João Pessoa": [-7.1195, -34.8450],
                "Recife": [-8.0476, -34.8770],
                "Maceió": [-9.6658, -35.7353],
                "Aracaju": [-10.9472, -37.0731],
                "Salvador": [-12.9714, -38.5014],
                "Teresina": [-5.0892, -42.8019],
                "São Luís": [-2.5387, -44.2828]
            },
            "diretorios": {
                "cache": "cache_rotas",
                "datasets": "datasets_gerados"
            },
            "cache": {
                "ttl_horas": 24,
                "auto_cleanup": True
            },
            "retry": {
                "max_tentativas": 3,
                "delay_inicial": 1,
                "backoff_multiplicador": 2
            },
            "graphhopper": {
                "url": "https://graphhopper.com/api/1/route",
                "vehicle": "car",
                "locale": "pt_BR",
                "points_encoded": True,
                "timeout": 30
            },
            "custos": {
                "consumo_km_por_litro": 12.0,
                "combustivel_por_litro": 5.50,
                "pedagio_por_100km": 15.0
            },
            "processamento": {
                "conexoes_simultaneas": 2,
                "delay_entre_requests": 0.5,
                "modo_sequencial": True
            }
        }
        
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config_arquivo = json.load(f)
                self._merge_config(config_padrao, config_arquivo)
                logger.info("✅ Configurações carregadas : (config.json)")
                return config_padrao
        except FileNotFoundError:
            logger.info("(config.json) não encontrado, usando configurações padrão")
            return config_padrao
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro config.json: {e}")
            return config_padrao
    
    def _merge_config(self, base: Dict, update: Dict) -> None:
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    #Valida configurações críticas
    def _validar_configuracoes(self) -> None:
        # Validar coordenadas
        for secao in ['origens', 'capitais']:
            for nome, coords in self.config[secao].items():
                if not self._validar_coordenadas(tuple(coords)):
                    logger.error(f"❌ Coordenadas inválidas para {nome}: {coords}")
                    sys.exit(1)
        
        # Validar diretorios
        cache_dir = self.config['diretorios']['cache']
        datasets_dir = self.config['diretorios']['datasets']
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(datasets_dir, exist_ok=True)
        
        logger.info("✅ Configurações validadas com sucesso")

   #Valida se as coordenadas estão em formato válido
    def _validar_coordenadas(self, coords: Tuple[float, float]) -> bool:
        try:
            lat, lon = coords
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (TypeError, ValueError):
            return False
    
    #Acesso seguro a configurações aninhadas
    def get(self, *keys) -> any:

        result = self.config
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return None
        return result
    
    #Retorna origens como tuplas
    def get_origens(self) -> Dict[str, Tuple[float, float]]:
        return {nome: tuple(coords) for nome, coords in self.config['origens'].items()}
    
    #Retorna origens como tuplas
    def get_capitais(self) -> Dict[str, Tuple[float, float]]:
        return {nome: tuple(coords) for nome, coords in self.config['capitais'].items()}

# ==============================================================
# INICIALIZAÇÃO DO SISTEMA
# ==============================================================

#Inicializa o sistema, carrega configurações
def inicializar_sistema() -> Tuple[ConfigurationManager, str]:

    load_dotenv()  # Carrega variáveis de ambiente
    
    # Carregar configurações
    config_manager = ConfigurationManager()
    
    # Obter a key da API
    api_key = os.getenv('GRAPHHOPPER_API_KEY')
    if not api_key:
        logger.error("❌ GRAPHHOPPER_API_KEY não encontrada no arquivo .env")
        sys.exit(1)
    
    logger.info("✅ (API key) carregada da variável do ambiente")
    return config_manager, api_key

# Inicializar sistema
CONFIG_MANAGER, API_KEY = inicializar_sistema()

# ==============================================================
# FUNÇÕES DE CACHE E UTILIDADES
# ==============================================================

#Gerenciador de cache para rotas
class CacheManager:
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.cache_dir = config_manager.get('diretorios', 'cache')
        self.ttl_horas = config_manager.get('cache', 'ttl_horas')

    #Carrega dados do cache verificando TTL
    def carregar_cache(self, origem_nome: str, destino_nome: str) -> Optional[Dict]:

        filename = os.path.join(self.cache_dir, f"rota_{origem_nome}_{destino_nome}.json")
        
        if not os.path.exists(filename):
            return None
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                dados = json.load(f)
            
            # Verificar TTL
            if 'timestamp' in dados:
                timestamp = datetime.fromisoformat(dados['timestamp'])
                if datetime.now() - timestamp > timedelta(hours=self.ttl_horas):
                    logger.info(f"🕒 Cache expirado para rota {origem_nome} → {destino_nome}")
                    os.remove(filename)
                    return None
            
            #Verificar se contém dados obrigatórios
            campos_obrigatorios = ['distance_km', 'tempo_h', 'coords']
            for campo in campos_obrigatorios:
                if campo not in dados:
                    logger.warning(f"🗂️ Cache incompleto para {origem_nome} → {destino_nome}, removendo")
                    os.remove(filename)
                    return None
            
            #Adicionar métricas se não existirem (compatibilidade com cache antigo)
            if 'velocidade_media_kmh' not in dados:
                metricas_extras = calcular_metricas_adicionais(
                    dados['distance_km'], 
                    dados['tempo_h'], 
                    self.config
                )
                dados.update(metricas_extras)
                # Salvar cache atualizado
                self.salvar_cache(origem_nome, destino_nome, dados)
            
            logger.debug(f"✅ Cache válido encontrado para rota {origem_nome} → {destino_nome}")
            return dados
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"⚠️ Erro ao ler cache para {origem_nome} → {destino_nome}: {e}")
            return None
    
     #Salva dados no cache com timestamp
    def salvar_cache(self, origem_nome: str, destino_nome: str, dados: Dict) -> None:
        filename = os.path.join(self.cache_dir, f"rota_{origem_nome}_{destino_nome}.json")
        
        dados_com_timestamp = {
            **dados,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(dados_com_timestamp, f, indent=2)
            logger.debug(f"💾 Cache salvo para rota {origem_nome} → {destino_nome}")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar cache para {origem_nome} → {destino_nome}: {e}")
    

# Remove arquivos de cache antigos
    def limpar_cache_antigo(self) -> None:

        if not os.path.exists(self.cache_dir):
            return
        
        limite_tempo = datetime.now() - timedelta(hours=self.ttl_horas)
        removidos = 0
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.cache_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    
                    if 'timestamp' in dados:
                        timestamp = datetime.fromisoformat(dados['timestamp'])
                        if timestamp < limite_tempo:
                            os.remove(filepath)
                            removidos += 1
                except Exception as e:
                    logger.warning(f"Erro ao verificar cache {filename}: {e}")
        
        if removidos > 0:
            logger.info(f"🧹 Removidos {removidos} arquivos de cache antigos")

#Valida se a resposta da API contém os dados necessários
def validar_resposta_api(data: Dict) -> bool:
    try:
        if 'paths' not in data or not data['paths']:
            return False
        
        path = data['paths'][0]
        campos_necessarios = ['distance', 'time', 'points']
        
        for campo in campos_necessarios:
            if campo not in path:
                return False
        
        # Validar valores numericos
        if not isinstance(path['distance'], (int, float)) or path['distance'] <= 0:
            return False
        if not isinstance(path['time'], (int, float)) or path['time'] <= 0:
            return False
        
        return True
    except (KeyError, TypeError, IndexError):
        return False

#Calcula metricas adicionais como velocidade media e custos
def calcular_metricas_adicionais(distancia_km: float, tempo_h: float, config_manager: ConfigurationManager) -> Dict:
    velocidade_media = distancia_km / tempo_h if tempo_h > 0 else 0
    
    # Cálculos de custo baseados nas configuração
    consumo = config_manager.get('custos', 'consumo_km_por_litro')
    preco_combustivel = config_manager.get('custos', 'combustivel_por_litro')
    pedagio_100km = config_manager.get('custos', 'pedagio_por_100km')
    
    custo_combustivel = (distancia_km / consumo) * preco_combustivel
    custo_pedagio = (distancia_km / 100) * pedagio_100km
    custo_total = custo_combustivel + custo_pedagio
    
    return {
        'velocidade_media_kmh': round(velocidade_media, 2),
        'custo_combustivel': round(custo_combustivel, 2),
        'custo_pedagio': round(custo_pedagio, 2),
        'custo_total_estimado': round(custo_total, 2)
    }

# Inicializar gerenciador de cache
CACHE_MANAGER = CacheManager(CONFIG_MANAGER)


# ==============================================================
# PROCESSAMENTO DE ROTAS
# ==============================================================

#Versão assíncrona da busca de rota com retry para rate limiting
async def get_route_async(session: aiohttp.ClientSession, origin: Tuple[float, float], 
                         destination: Tuple[float, float], api_key: str, 
                         origem_nome: str, destino_nome: str) -> Optional[Dict]:
    
    # Verificar cache primeiro
    dados_cache = CACHE_MANAGER.carregar_cache(origem_nome, destino_nome)
    if dados_cache:
        return dados_cache

    # Configurações da API
    url = CONFIG_MANAGER.get('graphhopper', 'url')
    params = {
        "point": [f"{origin[0]},{origin[1]}", f"{destination[0]},{destination[1]}"],
        "vehicle": CONFIG_MANAGER.get('graphhopper', 'vehicle'),
        "locale": CONFIG_MANAGER.get('graphhopper', 'locale'),
        "points_encoded": str(CONFIG_MANAGER.get('graphhopper', 'points_encoded')).lower(),
        "key": api_key,
    }

    # Configurações de retry ciclo
    max_tentativas = CONFIG_MANAGER.get('retry', 'max_tentativas')
    delay_inicial = CONFIG_MANAGER.get('retry', 'delay_inicial')
    multiplicador = CONFIG_MANAGER.get('retry', 'backoff_multiplicador')
    timeout = CONFIG_MANAGER.get('graphhopper', 'timeout')

    for tentativa in range(max_tentativas):
        try:
            # Delay progressivo entre tentativas para evitar rate limiting
            if tentativa > 0:
                delay = delay_inicial * (multiplicador ** (tentativa - 1))
                logger.info(f"⏳ Aguardando {delay}s antes da tentativa {tentativa + 1} para {origem_nome} → {destino_nome}")
                await asyncio.sleep(delay)

            logger.info(f"🚗 Buscando rota assíncrona {origem_nome} → {destino_nome} (tentativa {tentativa + 1})")
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                if response.status == 429:  # Too Many Requests
                    if tentativa < max_tentativas - 1:
                        retry_after = response.headers.get('Retry-After', delay_inicial * (multiplicador ** tentativa))
                        try:
                            retry_after = float(retry_after)
                        except ValueError:
                            retry_after = delay_inicial * (multiplicador ** tentativa)
                        logger.warning(f"⏱️ Rate limit atingido para {origem_nome} → {destino_nome}. Aguardando {retry_after}s...")
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        logger.error(f"❌ Rate limit persistente para {origem_nome} → {destino_nome} após {max_tentativas} tentativas")
                        return None
                
                response.raise_for_status()
                data = await response.json()

                # Validar resposta
                if not validar_resposta_api(data):
                    logger.error(f"❌ Resposta inválida da API para rota {origem_nome} → {destino_nome}")
                    return None

                path = data["paths"][0]
                distance_m = path["distance"]
                time_ms = path["time"]
                polyline_encoded = path["points"]
                
                try:
                    coords = polyline.decode(polyline_encoded)
                except Exception as e:
                    logger.error(f"❌ Erro ao decodificar polyline para rota {origem_nome} → {destino_nome}: {e}")
                    return None

                # Calcular métricas básicas
                distancia_km = distance_m / 1000
                tempo_h = time_ms / (1000 * 60 * 60)
                
                # Calcular métricas adicionais
                metricas_extras = calcular_metricas_adicionais(distancia_km, tempo_h, CONFIG_MANAGER)

                resultado = {
                    "distance_km": distancia_km,
                    "tempo_h": tempo_h,
                    "coords": coords,
                    **metricas_extras
                }

                # Salvar no cache
                CACHE_MANAGER.salvar_cache(origem_nome, destino_nome, resultado)
                logger.info(f"✅ Rota assíncrona {origem_nome} → {destino_nome} processada com sucesso")
                return resultado

        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                continue  # Será tratado acima
            logger.error(f"❌ Erro HTTP assíncrono ao buscar rota {origem_nome} → {destino_nome}: {e}")
            if tentativa == max_tentativas - 1:
                raise
        except asyncio.TimeoutError:
            logger.error(f"⏰ Timeout assíncrono ao buscar rota {origem_nome} → {destino_nome}")
            if tentativa == max_tentativas - 1:
                raise
        except Exception as e:
            logger.error(f"💥 Erro inesperado assíncrono ao buscar rota {origem_nome} → {destino_nome}: {e}")
            if tentativa == max_tentativas - 1:
                raise

    return None

# Processa rotas de forma assíncrona com controle de taxa para evitar rate limiting
async def processar_rotas_async(origem_nome: str, origem_coord: Tuple[float, float], 
                               capitais: Dict[str, Tuple[float, float]], api_key: str) -> pd.DataFrame:
    logger.info(f"Processando: {origem_nome}")
    dados_rotas = []
    bounds = [origem_coord]

    # Configurações de processamento
    limite_conexoes = CONFIG_MANAGER.get('processamento', 'conexoes_simultaneas')
    delay_requests = CONFIG_MANAGER.get('processamento', 'delay_entre_requests')

    # Criar sessão assíncrona com limite de conexões para evitar rate limiting
    connector = aiohttp.TCPConnector(limit=limite_conexoes)
    async with aiohttp.ClientSession(connector=connector) as session:
        destinos_validos = [(destino_nome, destino_coord) for destino_nome, destino_coord in capitais.items() 
                           if destino_nome != origem_nome]
        
        # Processar rotas sequencialmente para evitar rate limiting
        for destino_nome, destino_coord in destinos_validos:
            try:
                # Delay entre requisições para respeitar rate limits
                await asyncio.sleep(delay_requests)
                
                resultado = await get_route_async(session, origem_coord, destino_coord, api_key, origem_nome, destino_nome)
                
                if resultado is None:
                    logger.warning(f"⚠️ Não foi possível obter rota assíncrona {origem_nome} → {destino_nome}")
                    continue
                
                logger.info(f"✅ {origem_nome} → {destino_nome}: {resultado['tempo_h']:.2f}h, {resultado['distance_km']:.1f}km, R${resultado['custo_total_estimado']:.2f}")
                
                bounds.append(destino_coord)
                
                # Adiciona dados ao dataset
                dados_rotas.append({
                    "origem": origem_nome,
                    "destino": destino_nome,
                    "distancia_km": round(resultado["distance_km"], 2),
                    "tempo_horas": round(resultado["tempo_h"], 2),
                    "velocidade_media_kmh": resultado["velocidade_media_kmh"],
                    "custo_combustivel": resultado["custo_combustivel"],
                    "custo_pedagio": resultado["custo_pedagio"],
                    "custo_total_estimado": resultado["custo_total_estimado"]
                })
                
            except Exception as e:
                logger.error(f"❌ Erro ao processar rota assíncrona {origem_nome} → {destino_nome}: {e}")
                continue

    if dados_rotas:
        criar_mapa_com_resultados(origem_nome, origem_coord, dados_rotas, capitais)

    return pd.DataFrame(dados_rotas)

# Cria mapa usando dados processados
def criar_mapa_com_resultados(origem_nome: str, origem_coord: Tuple[float, float], 
                             dados_rotas: List[Dict], capitais: Dict[str, Tuple[float, float]]) -> None:
    mapa = folium.Map(location=origem_coord, zoom_start=6, tiles="cartodbpositron")
    bounds = [origem_coord]

    # Adicionar marcador de origem
    folium.Marker(
        location=origem_coord,
        tooltip=f"Origem: {origem_nome}",
        icon=folium.Icon(color='red')
    ).add_to(mapa)

    # Adicionar rotas e destinos
    for rota in dados_rotas:
        destino_nome = rota['destino']
        destino_coord = capitais[destino_nome]
        
        # Busca coordenadas de rotas do cache
        dados_cache = CACHE_MANAGER.carregar_cache(origem_nome, destino_nome)
        if dados_cache and 'coords' in dados_cache:
            folium.PolyLine(
                locations=dados_cache["coords"],
                color="red",
                weight=5,
                opacity=0.8,
                tooltip=f"{destino_nome}: {rota['tempo_horas']:.2f}h, {rota['distancia_km']:.1f}km, R${rota['custo_total_estimado']:.2f}"
            ).add_to(mapa)

        # Adicionar marcador de destino
        folium.Marker(
            location=destino_coord,
            tooltip=f"{destino_nome}: {rota['tempo_horas']:.2f}h, {rota['distancia_km']:.1f}km",
            icon=folium.Icon(color='blue')
        ).add_to(mapa)
        
        bounds.append(destino_coord)

    # Ajustar vista do mapa
    if bounds:
        mapa.fit_bounds(bounds)

    # Salvar mapa
    mapa_filename = f"mapa_entregas_{origem_nome.lower().replace(' ', '_')}.html"
    try:
        mapa.save(mapa_filename)
        logger.info(f"💾 Mapa assíncrono salvo como: {mapa_filename}")
    except Exception as e:
        logger.error(f"❌ Erro ao salvar mapa assíncrono: {e}")


# ========================
# EXECUÇÃO PRINCIPAL
# ========================

async def main_async():

    logger.info("=" * 80)
    logger.info("Iniciando processamento de rotas (versão assíncrona)")
    
    # Limpar cache antigo se configurado
    if CONFIG_MANAGER.get('cache', 'auto_cleanup'):
        CACHE_MANAGER.limpar_cache_antigo()
    
    todos_dados = []
    
    # Obter origens e capitais
    origens = CONFIG_MANAGER.get_origens()
    capitais = CONFIG_MANAGER.get_capitais()

    #  fazer processamento de cada origem
    for origem_nome, origem_coord in origens.items():
        try:
            df = await processar_rotas_async(origem_nome, origem_coord, capitais, API_KEY)
            if not df.empty:
                todos_dados.append(df)
            else:
                logger.warning(f"⚠️ Nenhuma rota processada para {origem_nome}")
        except Exception as e:
            logger.error(f"❌ Erro ao processar rotas de {origem_nome}: {e}")

    if todos_dados:
        df_consolidado = pd.concat(todos_dados, ignore_index=True)
        
        # Salvar CSV consolidado
        datasets_dir = CONFIG_MANAGER.get('diretorios', 'datasets')
        arquivo_consolidado = os.path.join(datasets_dir, "rotas__nordeste.csv")
        try:
            df_consolidado.to_csv(arquivo_consolidado, index=False)
            logger.debug(f"💾 Arquivo CSV único salvo como: {arquivo_consolidado}")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar arquivo CSV: {e}")
    else:
        logger.error("❌ Nenhum dado foi processado com sucesso")

    logger.info("✅ Processamento concluído!")


if __name__ == "__main__":
    try:
        # Executar sistema
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("🛑 Processamento interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro crítico na execução: {e}")
        logger.info("� Verifique as configurações e a conectividade")
        sys.exit(1)