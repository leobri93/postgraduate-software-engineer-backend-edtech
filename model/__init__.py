from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import os

# importando os elementos definidos no modelo
from model.base import Base
from model import models

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)

# --- Migração simples: adiciona colunas novas em 'alunos' se não existirem ---
def _ensure_alunos_columns(engine):
    try:
        with engine.begin() as conn:
            # obtém colunas atuais da tabela 'alunos'
            result = conn.execute(text("PRAGMA table_info('alunos')"))
            cols = [row[1] for row in result.fetchall()]

            # colunas que adicionamos no modelo
            to_add = []
            if 'cep' not in cols:
                to_add.append("cep TEXT")
            if 'estado' not in cols:
                to_add.append("estado TEXT")
            if 'cidade' not in cols:
                to_add.append("cidade TEXT")
            if 'rua' not in cols:
                to_add.append("rua TEXT")

            for coldef in to_add:
                conn.execute(text(f"ALTER TABLE alunos ADD COLUMN {coldef}"))
    except Exception:
        pass


_ensure_alunos_columns(engine)