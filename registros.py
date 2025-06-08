
import hashlib
from datetime import datetime

def gerar_hash_senha(senha):
    """
    Gera um hash SHA-256 seguro da senha.
    """
    return hashlib.sha256(senha.encode()).hexdigest()

def registrar_usuario():
    """
    Coleta dados do usuário, gera hash da senha e insere no banco.
    """
    print("\n=== Registro de Novo Usuário ===")
    username = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    email = input("Digite o e-mail: ")
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    senha_hash = gerar_hash_senha(senha)

    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Usuarios (username, password, email, data_registro)
            VALUES (?, ?, ?, ?);
        ''', (username, senha_hash, email, data_registro))
        conn.commit()
        conn.close()
        print("✅ Usuário registrado com sucesso.")
    except sqlite3.IntegrityError as e:
        print("❌ Erro ao registrar usuário:")
        if "UNIQUE constraint failed" in str(e):
            print("   - Nome de usuário ou e-mail já estão em uso.")
        else:
            print(f"   - {e}")
