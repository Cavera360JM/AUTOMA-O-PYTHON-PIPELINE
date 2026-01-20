import pandas as pd
import logging
from datetime import datetime
import os
from sqlalchemy import create_engine # Necessário para MySQL

# Configuração de Logs Profissional
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f"logs/execution_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

class DataPipeline:
    def __init__(self, input_source, type='csv'):
        """
        input_source: Caminho do arquivo ou string de conexão MySQL
        type: 'csv' ou 'mysql'
        """
        self.input_source = input_source
        self.type = type
        self.df = None
        self.metrics = {}

    def extract(self, query=None):
        """Extração polimórfica: Aceita CSV ou Banco de Dados."""
        try:
            logging.info(f"Iniciando extração via {self.type}...")
            
            if self.type == 'csv':
                if not os.path.exists(self.input_source):
                    raise FileNotFoundError(f"Arquivo não encontrado: {self.input_source}")
                self.df = pd.read_csv(self.input_source)
            
            elif self.type == 'mysql':
                # Requer: mysql-connector-python e sqlalchemy
                engine = create_engine(self.input_source)
                self.df = pd.read_sql(query, engine)
                
            logging.info(f"Sucesso: {len(self.df)} registros extraídos.")
            return self
        except Exception as e:
            logging.error(f"Falha na extração: {e}")
            raise

    def transform(self):
        """Transformação com lógica de negócio e higienização."""
        try:
            logging.info("Iniciando Pipeline de Transformação...")
            
            # 1. Tratamento de tipos e nulos (Sênior cuida da qualidade)
            self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
            self.df = self.df.dropna(subset=['total_price']) # Remove vendas sem valor
            
            # 2. Regras de Negócio (Margem, Imposto, Performance)
            self.df['tax_amount'] = self.df['total_price'] * 0.18
            self.df['net_revenue'] = self.df['total_price'] - self.df['tax_amount']
            
            # 3. Cálculo de métricas para o Dashboard
            self.metrics['total_revenue'] = float(self.df['total_price'].sum())
            self.metrics['avg_ticket'] = float(self.df['total_price'].mean())
            self.metrics['total_orders'] = len(self.df)
            self.metrics['last_update'] = datetime.now().strftime("%H:%M:%S")
            
            logging.info("Transformação aplicada com sucesso.")
            return self
        except Exception as e:
            logging.error(f"Erro na transformação: {e}")
            raise

    def load(self):
        """Persistência dos dados processados."""
        try:
            if not os.path.exists("output"):
                os.makedirs("output")
                
            filename = f"output/data_final_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            self.df.to_csv(filename, index=False)
            logging.info(f"Pipeline finalizado. Arquivo gerado: {filename}")
            return filename
        except Exception as e:
            logging.error(f"Erro no carregamento: {e}")
            raise

    def get_metrics(self):
        """Getter para interface visual."""
        return self.metrics