🚀 Enterprise Data Pipeline: Python + MySQL + Streamlit
Este repositório apresenta uma solução completa de Engenharia e Análise de Dados. O projeto simula um cenário corporativo onde dados brutos de vendas são extraídos, transformados via um pipeline ETL (Extract, Transform, Load) resiliente, persistidos em um banco de dados relacional (MySQL) e visualizados em um dashboard executivo interativo.

🛠️ Tecnologias Utilizadas
Python 3.14+: Linguagem core para lógica de automação.

Pandas: Processamento e manipulação de grandes volumes de dados.

MySQL: Persistência de dados relacional de alta performance.

SQLAlchemy: Camada de abstração e ORM para comunicação segura com o banco.

Streamlit: Framework para criação do Dashboard de BI reativo.

Logging: Auditoria completa do processo de execução.

🌟 Diferenciais Técnicos (Nível Sênior)
Arquitetura Modular: Separação clara de responsabilidades entre ingestão, processamento e visualização.

Persistência Robusta: Uso de quote_plus para tratamento de credenciais especiais e conexões otimizadas via SQLAlchemy.

Observabilidade: Implementação de logs rotativos para monitoramento de falhas e auditoria de carga.

Data Quality: Pipeline com tratamento de tipos, higienização de valores nulos e validação de schema.

UX de Negócio: Dashboard com KPIs financeiros reais (Margem de Lucro, Impostos, Ticket Médio) e filtros dinâmicos.

🏗️ Estrutura do Projeto
app.py: Interface Web e Dashboard de Business Intelligence.

src/processor.py: Motor de ETL e lógica de transformação de dados.

src/database.py: Singleton de conexão e operações com MySQL.

src/generator.py: Gerador de massa de dados para simulação de sistemas legados.

src/utils.py: Utilitários de infraestrutura (pastas, logs, formatação).

🚀 Como Rodar o Projeto
Configurar o MySQL:

Crie o banco analytics_db.

Execute o script DDL presente na documentação para criar a tabela automacao.

Instalar Dependências:

Bash

pip install pandas streamlit sqlalchemy mysql-connector-python
Executar a Aplicação:

Bash

python -m streamlit run app.py
📈 Roadmap de Evolução
[ ] Conteinerização com Docker para isolamento de ambiente.

[ ] Implementação de Testes Unitários com PyTest.

[ ] Integração de módulo de Machine Learning para Forecast de vendas.

Desenvolvido por João Miguel Dias da Silva Conecte-se comigo no LinkedIn
