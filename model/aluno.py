from sqlalchemy import ForeignKey, create_engine, Integer, String, Date, Time, DateTime, Text, Boolean, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped 
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime, time
import os

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# --- Database configuration ---
engine = create_engine(db_url, connect_args={"check_same_thread": False})
Base = declarative_base()

# --- SQLAlchemy Models ---
class AlunoDB(Base):
    __tablename__ = "alunos"
    id_aluno = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = mapped_column(String, index=True)
    email = mapped_column(String, unique=True, index=True)
    data_nascimento = mapped_column(Date)
    data_cadastro = mapped_column(DateTime, default=datetime.now)

    atividades = relationship("AtividadeDB", back_populates="aluno")
    respostas = relationship("RespostaAlunoDB", back_populates="aluno")