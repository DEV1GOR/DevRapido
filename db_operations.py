import sqlite3
import os
from datetime import datetime

DB_FILE = 'quiz_app.db' 

def conectar_db():
    
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON;") 
        print(f"Conectado ao banco de dados: {DB_FILE}")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas():
   
    conn = conectar_db()
    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL, -- Em um app real, armazene hashes de senhas!
            email TEXT UNIQUE NOT NULL,
            data_registro TEXT NOT NULL -- Formato YYYY-MM-DD HH:MM:SS
        );
    ''')
    print("Tabela 'Usuarios' criada ou já existe.")


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            criado_por INTEGER NOT NULL,
            data_criacao TEXT NOT NULL,
            FOREIGN KEY (criado_por) REFERENCES Usuarios(id) ON DELETE CASCADE
        );
    ''')
    print("Tabela 'Quizzes' criada ou já existe.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Perguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            texto_pergunta TEXT NOT NULL,
            tipo_pergunta TEXT NOT NULL, -- Ex: 'multipla_escolha', 'verdadeiro_falso', 'resposta_curta'
            pontuacao INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (quiz_id) REFERENCES Quizzes(id) ON DELETE CASCADE
        );
    ''')
    print("Tabela 'Perguntas' criada ou já existe.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OpcoesRespostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta_id INTEGER NOT NULL,
            texto_opcao TEXT NOT NULL,
            correta INTEGER NOT NULL DEFAULT 0, -- 1 para correta, 0 para incorreta
            FOREIGN KEY (pergunta_id) REFERENCES Perguntas(id) ON DELETE CASCADE
        );
    ''')
    print("Tabela 'OpcoesRespostas' criada ou já existe.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TentativasQuiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT, -- Pode ser NULL se o quiz não foi concluído
            pontuacao_final INTEGER, -- Pontuação total obtida nesta tentativa
            FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (quiz_id) REFERENCES Quizzes(id) ON DELETE CASCADE
        );
    ''')
    print("Tabela 'TentativasQuiz' criada ou já existe.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RespostasUsuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tentativa_id INTEGER NOT NULL,
            pergunta_id INTEGER NOT NULL,
            opcao_selecionada_id INTEGER, -- ID da opção se for múltipla escolha
            resposta_texto TEXT, -- Texto da resposta se for tipo 'resposta_curta'
            correta INTEGER NOT NULL, -- 1 se a resposta do usuário estiver correta, 0 caso contrário
            FOREIGN KEY (tentativa_id) REFERENCES TentativasQuiz(id) ON DELETE CASCADE,
            FOREIGN KEY (pergunta_id) REFERENCES Perguntas(id) ON DELETE CASCADE,
            FOREIGN KEY (opcao_selecionada_id) REFERENCES OpcoesRespostas(id) ON DELETE CASCADE
        );
    ''')
    print("Tabela 'RespostasUsuarios' criada ou já existe.")

    conn.commit()
    conn.close()
    print("Todas as tabelas foram criadas com sucesso ou já existiam.")

def verificar_db():
    # n mexer na função verificar_db está dando erros e essa é a versão que funciona
    if os.path.exists(DB_FILE):
        print(f"\nArquivo do banco de dados '{DB_FILE}' encontrado.")
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()
            print("Tabelas existentes no banco de dados:")
            for tabela in tabelas:
                print(f"- {tabela[0]}")
            conn.close()
    else:
        print(f"\nArquivo do banco de dados '{DB_FILE}' NÃO encontrado.")


def obter_perguntas_do_quiz(quiz_id):

    conn = None
    perguntas_com_opcoes = []
    try:
        conn = conectar_db() 
        if conn is None:
            return [] 
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        query = """
        SELECT
            p.id AS pergunta_id,
            p.texto_pergunta,
            p.tipo_pergunta,
            p.pontuacao,
            op.id AS opcao_id,
            op.texto_opcao,
            op.correta
        FROM
            Perguntas p
        JOIN
            OpcoesRespostas op ON p.id = op.pergunta_id
        WHERE
            p.quiz_id = ?
        ORDER BY
            p.id, op.id;
        """
        cursor.execute(query, (quiz_id,))
        rows = cursor.fetchall()

        perguntas_dict = {}
        for row in rows:
            pergunta_id = row['pergunta_id']
            if pergunta_id not in perguntas_dict:
                perguntas_dict[pergunta_id] = {
                    'id': pergunta_id,
                    'texto_pergunta': row['texto_pergunta'],
                    'tipo_pergunta': row['tipo_pergunta'],
                    'pontuacao': row['pontuacao'],
                    'opcoes_resposta': []
                }
            perguntas_dict[pergunta_id]['opcoes_resposta'].append({
                'id': row['opcao_id'],
                'texto_opcao': row['texto_opcao'],
                'correta': bool(row['correta']) # Converte 0/1 para True/False
            })

        perguntas_com_opcoes = list(perguntas_dict.values())

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        
    finally:
        if conn:
            conn.close()
    return perguntas_com_opcoes

if __name__ == "__main__":
 
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Arquivo '{DB_FILE}' existente removido para recriação.")

    print("Iniciando a criação das tabelas...")
    criar_tabelas()
    print("\nVerificando a estrutura do banco de dados...")
    verificar_db()

    conn = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Usuarios WHERE username = 'admin_quiz'")
        usuario_admin_existente = cursor.fetchone()
        if not usuario_admin_existente:
            cursor.execute("INSERT INTO Usuarios (username, password, email, data_registro) VALUES (?, ?, ?, ?)",
                           ('admin_quiz', 'senha_hash_segura', 'admin@quiz.com', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            admin_id = cursor.lastrowid
            print(f"Usuário 'admin_quiz' inserido com ID: {admin_id}")
        else:
            admin_id = usuario_admin_existente['id']
            print(f"Usuário 'admin_quiz' já existe com ID: {admin_id}")

        cursor.execute("SELECT id FROM Quizzes WHERE titulo = 'Quiz de Conhecimentos Gerais'")
        quiz_existente = cursor.fetchone()
        if not quiz_existente:
            cursor.execute("INSERT INTO Quizzes (titulo, descricao, criado_por, data_criacao) VALUES (?, ?, ?, ?)",
                           ('Quiz de Conhecimentos Gerais', 'Um quiz divertido sobre diversos temas.', admin_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            quiz_id_exemplo = cursor.lastrowid
            print(f"Quiz 'Quiz de Conhecimentos Gerais' inserido com ID: {quiz_id_exemplo}")

            # Pergunta 1 apenas exemplos trocar as perguntas dps
            cursor.execute("INSERT INTO Perguntas (quiz_id, texto_pergunta, tipo_pergunta, pontuacao) VALUES (?, ?, ?, ?)",
                           (quiz_id_exemplo, 'Qual a capital do Brasil?', 'multipla_escolha', 5))
            pergunta_id_1 = cursor.lastrowid
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_1, 'Rio de Janeiro', 0))
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_1, 'São Paulo', 0))
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_1, 'Brasília', 1))
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_1, 'Belo Horizonte', 0))

            # Pergunta 2 apenas exemplos trocar as perguntas dps
            cursor.execute("INSERT INTO Perguntas (quiz_id, texto_pergunta, tipo_pergunta, pontuacao) VALUES (?, ?, ?, ?)",
                           (quiz_id_exemplo, 'Quem descobriu o Brasil?', 'multipla_escolha', 10))
            pergunta_id_2 = cursor.lastrowid
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_2, 'Dom Pedro I', 0))
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_2, 'Cristóvão Colombo', 0))
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_2, 'Pedro Álvares Cabral', 1))
            cursor.execute("INSERT INTO OpcoesRespostas (pergunta_id, texto_opcao, correta) VALUES (?, ?, ?)",
                           (pergunta_id_2, 'Vasco da Gama', 0))
            conn.commit()
            print("Perguntas e opções de exemplo inseridas.")
        else:
            quiz_id_exemplo = quiz_existente['id']
            print(f"Quiz 'Quiz de Conhecimentos Gerais' já existe com ID: {quiz_id_exemplo}")

        print(f"\n--- Perguntas para o Quiz ID {quiz_id_exemplo} ---")
        perguntas = obter_perguntas_do_quiz(quiz_id_exemplo)
        if perguntas:
            for p in perguntas:
                print(f"ID da Pergunta: {p['id']}, Texto: {p['texto_pergunta']}")
                for o in p['opcoes_resposta']:
                    print(f"  - Opção: {o['texto_opcao']} (Correta: {o['correta']})")
        else:
            print("Nenhuma pergunta encontrada para este quiz ou quiz não existe.")

        print("\n--- Testando com um Quiz ID inexistente (ex: 999) ---")
        perguntas_inexistente = obter_perguntas_do_quiz(999)
        if not perguntas_inexistente:
            print("Nenhuma pergunta encontrada para o Quiz ID 999 (esperado).")

    except sqlite3.Error as e:
        print(f"Erro durante a inicialização/teste do banco de dados: {e}")
    finally:
        if conn:
            conn.close()

