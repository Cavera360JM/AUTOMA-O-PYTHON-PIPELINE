from src.processor import DataPipeline
from src.generator import generate_fake_data
from src.utils import setup_directories
import logging

def run_orchestrator():
    # 1. Setup inicial de infraestrutura
    setup_directories(['data', 'logs', 'output'])
    
    RAW_DATA_PATH = "data/raw_sales.csv"
    
    try:
        # 2. Mock: Gerando os dados fictícios
        logging.info("--- INICIANDO PROCESSO DE ETL ---")
        generate_fake_data(RAW_DATA_PATH)
        
        # 3. Execução do Pipeline Sênior
        pipeline = DataPipeline(RAW_DATA_PATH)
        
        # O padrão de 'Method Chaining' (pipeline.extract().transform()...)
        # é muito comum em bibliotecas de alto nível.
        pipeline.extract().transform().load()
        
        logging.info("--- ETL FINALIZADO COM SUCESSO ---")
        print("\n✅ Sucesso! Verifique a pasta /output para os resultados e /logs para o histórico.")
        
    except Exception as e:
        logging.critical(f"Falha catastrófica no orquestrador: {e}")
        print("\n❌ Erro crítico. Verifique o arquivo de Log na pasta /logs.")

if __name__ == "__main__":
    run_orchestrator()