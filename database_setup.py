import sqlite3
import os
from datetime import datetime

# --- Configurações do Banco de Dados ---
DB_FILE = 'quiz_app.db' # Nome do arquivo do banco de dados SQLite

def conectar_db():
    """
    Conecta ao banco de dados SQLite. Se o arquivo não existir, ele será criado.
    Retorna o objeto de conexão.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON;") # Habilita o suporte a chaves estrangeiras
        print(f"Conectado ao banco de dados: {DB_FILE}")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas():
    """
    Cria todas as tabelas necessárias para o aplicativo de quiz.
    """
    conn = conectar_db()
    if conn is None:
        return

    cursor = conn.cursor()

    # Tabela Usuarios
    # Armazena informações dos usuários (jogadores)
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

    # Tabela Quizzes
    # Armazena os diferentes quizzes disponíveis
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

    # Tabela Perguntas
    # Armazena as perguntas de cada quiz
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

    # Tabela OpcoesRespostas
    # Armazena as opções de resposta para perguntas de múltipla escolha
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

    # Tabela TentativasQuiz
    # Registra cada vez que um usuário inicia um quiz
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

    # Tabela RespostasUsuarios
    # Armazena as respostas dadas pelos usuários em cada tentativa
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
    """
    Verifica se o arquivo do banco de dados existe e se as tabelas foram criadas.
    """
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

# --- Execução Principal ---
if __name__ == "__main__":
    # Remove o arquivo do banco de dados se ele já existir para começar do zero
    # CUIDADO: Isso apagará todos os dados existentes! Use apenas para testes.
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Arquivo '{DB_FILE}' existente removido para recriação.")

    print("Iniciando a criação das tabelas...")
    criar_tabelas()
    print("\nVerificando a estrutura do banco de dados...")
    verificar_db()
