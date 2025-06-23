from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime

# --- Pydantic Schemas ---

class NovoAluno(BaseModel):
    nome: str
    email: EmailStr
    data_nascimento: date 

class Aluno(BaseModel):
    id_aluno: int
    nome: str
    email: EmailStr
    data_nascimento: date
    data_cadastro: datetime

class AlunoDelSchema(BaseModel):
    """Schema para deletar um aluno.
    """
    message: str

class ListagemAlunos(BaseModel):
    """Schema para listar alunos.
    """
    alunos: list[Aluno]
    
    class Config:
        from_attributes = True