import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_fake_data(file_path, num_rows=500):
    """Simula a exportação de dados brutos de um ERP/Banco de Dados."""
    if not os.path.exists('data'):
        os.makedirs('data')
        
    products = ['Chapa de Aço', 'Bobina Galvanizada', 'Perfil U', 'Viga I', 'Corte e Dobra']
    data = []
    
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(num_rows):
        dt = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        data.append({
            'order_id': 1000 + i,
            'transaction_date': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'product': random.choice(products),
            'quantity': random.randint(1, 50),
            'total_price': round(random.uniform(500.0, 15000.0), 2),
            'status': random.choice(['Faturado', 'Pendente', 'Cancelado'])
        })
    
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    # Simulando um dado sujo para o Sênior tratar: algumas linhas com preço nulo
    return file_path