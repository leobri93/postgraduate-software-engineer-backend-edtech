from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

# --- Pydantic Schemas ---
class Atividade(BaseModel):
    id_atividade: int
    id_aluno: int
    data_inicio: date
    hora_inicio: time
    duracao: int
    status: str 

    class Config:
        from_attributes = True

class AtividadeHistorico(BaseModel):
    id_atividade: int
    data_inicio: date
    hora_inicio: time
    duracao: int
    status: str

class ListagemAtividades(BaseModel):
    """Schema para listar atividades.
    """
    alunos: list[AtividadeHistorico]

    class Config:
        from_attributes = True