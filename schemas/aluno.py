from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, time, datetime
from typing import Optional
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
    cep: str
    estado: Optional[str]
    cidade: Optional[str]
    rua: Optional[str]

class NovoAluno(BaseModel):
    """Schema para criar um novo aluno.
    """
    nome: str = "João da Silva"
    email: EmailStr = "jsilva@gmail.com"
    data_nascimento: date = datetime(2000, 1, 1).date()
    cep: str = "01001000"

    @field_validator("cep", mode="before")
    def ensure_cep_is_str(cls, v):
        """Garante que `cep` será sempre uma string mesmo quando enviado como número.
        """
        if v is None:
            return v
        return str(v)

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
        "data_cadastro": aluno.data_cadastro,
        "cep": aluno.cep,
        "estado": aluno.estado,
        "cidade": aluno.cidade,
        "rua": aluno.rua
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
            "data_cadastro": aluno.data_cadastro,
            "cep": aluno.cep,
            "estado": aluno.estado,
            "cidade": aluno.cidade,
            "rua": aluno.rua
        })

    return {"alunos": result}


class Endereco(BaseModel):
    """Schema para representar apenas os campos de endereço de um aluno."""
    cep: str
    estado: Optional[str]
    cidade: Optional[str]
    rua: Optional[str]


class AtualizaEndereco(BaseModel):
    """Schema para atualizar os campos de endereço de um aluno.

    Todos os campos são opcionais; quando `cep` é informado, será validado e, se
    necessário, consultada a BrasilAPI para preencher campos faltantes.
    """
    cep: Optional[str] = ""
    estado: Optional[str] = ""
    cidade: Optional[str] = ""
    rua: Optional[str] = ""

    @field_validator("cep", mode="before")
    def ensure_cep_is_str(cls, v):
        if v is None:
            return v
        return str(v)


def apresentar_endereco(aluno: models.AlunoDB) -> dict:
    """Apresenta apenas os campos de endereço de um aluno."""
    return {
        "cep": aluno.cep,
        "estado": aluno.estado,
        "cidade": aluno.cidade,
        "rua": aluno.rua,
    }