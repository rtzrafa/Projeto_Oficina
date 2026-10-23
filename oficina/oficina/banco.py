import os
import mysql.connector
from mysql.connector import Error

# Dicionário central de configuração
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Senai@118'),
    'database': os.environ.get('DB_NAME', 'saep_db'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'charset': 'utf8mb4'
}

def obter_conexao():
    """Retorna uma nova conexão ativa com o banco MySQL ou None em caso de falha."""
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"[ERRO BANCO DE DADOS] Falha na conexão: {e}")
        return None

# Bloco executável para teste em aula
if __name__ == '__main__':
    con = obter_conexao()
    if con:
        print("[SUCESSO] Conexão com saep_db estabelecida com sucesso!")
        cursor = con.cursor()
        cursor.execute("SHOW TABLES;")
        print("Tabelas encontradas:", [t[0] for t in cursor.fetchall()])
        con.close()
    else:
        print("[FALHA] Não foi possível conectar ao MySQL. Verifique se o MySQL está rodando.")
