# Backup do banco de dados local - NÃO ENVIAR PARA O GITHUB
# Este arquivo contém dados sensíveis do seu banco local

# Se precisar fazer backup, use:
# python -c "from app.database import engine; from sqlalchemy import text; import pandas as pd; conn = engine.connect(); df = pd.read_sql('SELECT * FROM transacoes', conn); df.to_csv('backup_transacoes.csv', index=False)"

# Para restaurar (apenas em ambiente local):
# python -c "import pandas as pd; from app.database import engine; from sqlalchemy import text; df = pd.read_csv('backup_transacoes.csv'); df.to_sql('transacoes', engine, if_exists='append', index=False)"
