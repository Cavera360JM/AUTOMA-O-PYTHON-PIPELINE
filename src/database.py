from sqlalchemy import create_engine
import pandas as pd
import logging
from urllib.parse import quote_plus  # Importante para tratar senhas com @

class MySQLConnection:
    def __init__(self):
        self.user = "root"
        # Usamos quote_plus para que o @ da senha não quebre a URL de conexão
        self.password = quote_plus("88014946@Mar")
        self.host = "localhost"
        self.database = "analytics_db"
        self.port = "3306"
        
        # String de conexão corrigida
        self.conn_str = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        
        # Criar engine com verificação de erro imediata
        try:
            self.engine = create_engine(self.conn_str)
            logging.info("Engine de conexão criada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao criar engine: {e}")

    def save_data(self, df, table_name="automacao"):
        """Insere o DataFrame no MySQL."""
        try:
            # Usamos chunksize para ser mais performático (Nível Sênior)
            df.to_sql(table_name, con=self.engine, if_exists='append', index=False, chunksize=1000)
            logging.info(f"Dados inseridos com sucesso na tabela {table_name}.")
        except Exception as e:
            logging.error(f"Erro ao salvar no MySQL: {e}")
            raise

    def get_data(self, query="SELECT * FROM automacao"):
        """Busca dados do MySQL."""
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            logging.error(f"Erro ao buscar dados do MySQL: {e}")
            raise