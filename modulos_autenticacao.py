import sqlite3
import datetime

NOME_DO_BANCO = 'quiz_app.db'

def conectar_db():
    """
    Funçãozinha pra conectar no banco.
    Se não achar o arquivo, ele cria 
    """
    conn = sqlite3.connect(NOME_DO_BANCO)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def criar_tabela_usuarios_se_nao_existe():
    """
    Essa função garante que a tabela de usuários exista.
    Rodar ela é bom pra não ter erro na primeira vez!
    """
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL, -- ALERTA PROFESSOR: Aqui que a gente vai hashar futuramente!
            email TEXT UNIQUE NOT NULL,
            data_registro TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
    print(">> Estrutura da tabela 'Usuarios' verificada/criada. Bora pra action!")


def registrar_usuario(username, password, email):
    """
    Cadastra um novo jogador no nosso game.
    Retorna True se deu boa, False se já existir o usuário ou e-mail.
    """
    conn = conectar_db()
    cursor = conn.cursor()
    data_e_hora_agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ALERTA PROFESSOR: Senha em texto puro AQUI é só pra testar!
    # A GENTE VAI MELHORAR ISSO!
    # Ex: senha_segura = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    senha_para_salvar = password # Por enquanto, tá assim, direto.

    try:
        cursor.execute(
            "INSERT INTO Usuarios (username, password, email, data_registro) VALUES (?, ?, ?, ?)",
            (username, senha_para_salvar, email, data_e_hora_agora)
        )
        conn.commit()
        print(f"✅ Sucesso! Usuário '{username}' cadastrado. Bem-vindo ao jogo!")
        return True
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: Usuarios.username" in str(e):
            print(f"❌ Erro! Puts, o nome de usuário '{username}' já tá sendo usado. Tenta outro!")
        elif "UNIQUE constraint failed: Usuarios.email" in str(e):
            print(f"❌ Erro! Esse e-mail '{email}' já tem conta. Esqueceu a senha?")
        else:
            print(f"❌ Erro de banco de dados: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    finally:
        conn.close()

def verificar_login(username, password):
    """
    Checa se o jogador pode entrar no game.
    Retorna o ID do usuário se o login for OK, ou None se algo der errado.
    """
    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, password FROM Usuarios WHERE username = ?",
            (username,)
        )
        resultado = cursor.fetchone() # Pega a primeira linha que achar

        if resultado:
            id_do_usuario, senha_guardada = resultado
            # ALERTA PROFESSOR: Se a gente usasse hash, a comparação seria diferente aqui!
            # Ex: if bcrypt.checkpw(password.encode('utf-8'), senha_guardada.encode('utf-8')):
            if senha_guardada == password: # Por enquanto, compara direto.
                print(f"🎉 É isso aí! Login do '{username}' feito com sucesso. Partiu quiz!")
                return id_do_usuario
            else:
                print(f"❌ Senha incorreta para o usuário '{username}'. Tenta de novo, amigão.")
        else:
            print(f"❌ Usuário '{username}' não encontrado. Cadastra primeiro, ou digitou errado?")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao tentar logar: {e}")
        return None
    finally:
        conn.close()

# --- BLOCÃO DE TESTE (Só pra gente ver funcionando na prática!) ---
if __name__ == "__main__":
    print("==== Começando os testes de Autenticação ====")

    # 1. Garante que a tabela 'Usuarios' exista (se já rodou, não faz nada)
    criar_tabela_usuarios_se_nao_existe()

    print("\n--- TESTANDO O REGISTRO DE USUÁRIOS ---")
    # Tentativa 1: Registrar um usuário novinho em folha
    registrar_usuario("jogador_teste_1", "senha123", "teste1@email.com")

    # Tentativa 2: Tentar registrar o mesmo usuário (deve dar erro)
    registrar_usuario("jogador_teste_1", "outrasenha", "outro@email.com")

    # Tentativa 3: Tentar registrar com um e-mail já usado (deve dar erro)
    registrar_usuario("jogador_teste_2", "senhaabc", "teste1@email.com")

    # Tentativa 4: Registrar mais um usuário diferente
    registrar_usuario("novato_no_quiz", "topsecret", "novato@email.com")


    print("\n--- TESTANDO O LOGIN DE USUÁRIOS ---")
    # Tentativa 1: Login com sucesso!
    id_logado = verificar_login("jogador_teste_1", "senha123")
    if id_logado:
        print(f"ID do jogador logado: {id_logado}")

    # Tentativa 2: Senha errada para o mesmo usuário
    verificar_login("jogador_teste_1", "senhaerrada")

    # Tentativa 3: Tentar logar com usuário que não existe
    verificar_login("nao_existo", "qualquer_coisa")

    # Tentativa 4: Login do segundo usuário que cadastramos
    id_novato = verificar_login("novato_no_quiz", "topsecret")
    if id_novato:
        print(f"ID do novato logado: {id_novato}")


    print("\n==== Testes de Autenticação Finalizados! ====")
    print("Agora é só integrar isso com o frontend! 😉")