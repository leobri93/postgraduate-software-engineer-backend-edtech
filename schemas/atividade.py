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

class ListagemAtividades(BaseModel):
    """Schema para listar atividades.
    """
    alunos: list[Atividade]

    class Config:
        from_attributes = True

def apresentar_atividade(atividade) -> dict:
    """Função auxiliar para apresentar os dados de uma atividade.
    """
    return {
        "id_atividade": atividade.id_atividade,
        "id_aluno": atividade.id_aluno,
        "data_inicio": str(atividade.data_inicio),
        "hora_inicio": str(atividade.hora_inicio),
        "duracao": atividade.duracao,
        "status": atividade.status
    }

def apresentar_atividade_listagem(atividades: list) -> dict:
    """Função auxiliar para apresentar a listagem de atividades.
    """
    result = []
    for atividade in atividades:
        result.append({
            "id_atividade": atividade.id_atividade,
            "id_aluno": atividade.id_aluno,
            "data_inicio": str(atividade.data_inicio),
            "hora_inicio": str(atividade.hora_inicio),
            "duracao": atividade.duracao,
            "status": atividade.status
        })
    return {"atividades": result}