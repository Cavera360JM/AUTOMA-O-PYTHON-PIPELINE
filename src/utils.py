import os
import logging

def setup_directories(directories):
    """Garante que a infraestrutura de pastas existe antes de rodar."""
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Diretório criado: {directory}")

def format_currency(value):
    """Formata valores para padrão brasileiro."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")