from pydantic import BaseModel, EmailStr, Field
from datetime import date, time, datetime
from model import models

# --- Pydantic Schemas ---

class Aluno(BaseModel):
    """Schema para representar um aluno.
    """
    id_aluno: int
    nome: str
    email: EmailStr
    data_nascimento: date
    data_cadastro: datetime

class NovoAluno(BaseModel):
    """Schema para criar um novo aluno.
    """
    nome: str = "João da Silva"
    email: EmailStr = "jsilva@gmail.com"
    data_nascimento: date = datetime(2000, 1, 1).date()

class AlunoBuscaSchema(BaseModel):
    """Schema para buscar um aluno.
    """
    id_aluno: int 

    class Config:
        from_attributes = True

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

def apresentar_aluno(aluno: models.AlunoDB) -> dict:
    """Função auxiliar para apresentar os dados de um aluno.
    """
    return {
        "id_aluno": aluno.id_aluno,
        "nome": aluno.nome,
        "email": aluno.email,
        "data_nascimento": aluno.data_nascimento,
        "data_cadastro": aluno.data_cadastro
    }

def apresentar_aluno_listagem(alunos: list[models.AlunoDB]) -> dict:
    """Função auxiliar para apresentar a listagem de alunos.
    """
    result = []
    for aluno in alunos:
        result.append({
            "id_aluno": aluno.id_aluno,
            "nome": aluno.nome,
            "email": aluno.email,
            "data_nascimento": aluno.data_nascimento,
            "data_cadastro": aluno.data_cadastro
        })

    return {"alunos": result}