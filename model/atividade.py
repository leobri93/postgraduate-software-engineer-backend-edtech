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

class AtividadeDB(Base):
    __tablename__ = "atividades"
    id_atividade = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    id_aluno = mapped_column(ForeignKey("alunos.id_aluno"), index=True)
    data_inicio = mapped_column(Date)
    hora_inicio : Mapped[time] = mapped_column(Time, nullable=False)
    duracao = mapped_column(Integer)
    status = mapped_column(SQLEnum('iniciada', 'concluida', 'pendente_correcao', name='atividade_status_enum'))

    aluno = relationship("AlunoDB", back_populates="atividades")