from sqlalchemy import ForeignKey, create_engine, Integer, String, Date, Time, DateTime, Text, Boolean, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped 
from datetime import date, datetime, time
from  model import Base


# --- SQLAlchemy Models ---
class AlunoDB(Base):
    __tablename__ = "alunos"
    id_aluno = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = mapped_column(String, index=True)
    email = mapped_column(String, unique=True, index=True)
    data_nascimento = mapped_column(Date)
    data_cadastro = mapped_column(DateTime, default=datetime.now)

    atividades = relationship("AtividadeDB", back_populates="aluno")

class AtividadeDB(Base):
    __tablename__ = "atividades"
    id_atividade = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    id_aluno = mapped_column(ForeignKey("alunos.id_aluno"), index=True)
    data_inicio = mapped_column(Date)
    hora_inicio : Mapped[time] = mapped_column(Time, nullable=False)
    duracao = mapped_column(Integer)
    status = mapped_column(SQLEnum('iniciada', 'concluida', 'pendente_correcao', name='atividade_status_enum'))

    aluno = relationship("AlunoDB", back_populates="atividades")