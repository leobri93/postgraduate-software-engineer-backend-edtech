from flask import abort
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from http import HTTPStatus
from schemas import aluno, atividade
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from model import aluno as aluno_model
from model import atividade as atividade_model
from datetime import datetime
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
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = OpenAPI(
    __name__,
    info=Info(
        title="API EdTech",
        version="1.0.0",
        description="API para cadastro de alunos e atividades",
    )
)

aluno_tag = Tag(name="Aluno", description="Adição, remoção e listagem de alunos")
atividade_tag = Tag(name="Atividade", description="Listagem de atividades")

def verify_date_format(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
# Rotas de Aluno
@app.post('/alunos', tags=[aluno_tag], responses={"200": aluno.Aluno})
def create_aluno(aluno_data: aluno.NovoAluno):
    """
    Cadastra um novo aluno.
    """
    session = LocalSession()

    query_aluno = select(aluno_model.AlunoDB).where(aluno_model.AlunoDB.email == aluno_data.email)
    db_aluno = session.execute(query_aluno).scalar_one_or_none()
    if db_aluno:
            abort(HTTPStatus.BAD_REQUEST, description="Email já cadastrado.")
    
    if (aluno_data.data_nascimento > datetime.now().date() or 
        aluno_data.data_nascimento < datetime(1900, 1, 1).date() or 
        verify_date_format(str(aluno_data.data_nascimento)) is False):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, description="Data de nascimento inválida.")
    
    new_aluno = aluno_model.AlunoDB(
        nome=aluno_data.nome,
        email=aluno_data.email,
        data_nascimento=aluno_data.data_nascimento,
        data_cadastro=datetime.now()
    )
    
    session.add(new_aluno)
    session.commit()
    return new_aluno

@app.delete('/alunos/{id_aluno}', tags=[aluno_tag], responses={"200": aluno.AlunoDelSchema})
def delete_aluno(id_aluno: int):
    """
    Remove um aluno pelo ID.
    """
    session = LocalSession()

    query_aluno = select(aluno_model.AlunoDB).where(aluno_model.AlunoDB.id_aluno == id_aluno)
    aluno = session.execute(query_aluno).scalar_one_or_none()
    if not aluno:
        abort(HTTPStatus.NOT_FOUND, description="Nenhum aluno encontrado para o ID fornecido.")
    
    session.delete(aluno)
    session.commit()
    return "Aluno excluido com sucesso!"

@app.get('/alunos', tags=[aluno_tag], responses={"200" : aluno.ListagemAlunos})
def list_alunos():
    """
    Lista todos os alunos cadastrados.
    """
    session = LocalSession()

    query_aluno = select(aluno_model.AlunoDB).order_by(aluno_model.AlunoDB.data_cadastro.desc())
    alunos = session.execute(query_aluno).scalars().all()
    return alunos

#Rota de atividade
@app.get("/atividades/{id_aluno}", tags=[atividade_tag], responses={"200": atividade.ListagemAtividades})
def get_atividades_aluno(id_aluno: int):
    """
    Retorna o histórico de todas as atividades de um aluno.
    """
    session = LocalSession()

    query_aluno = select(aluno_model.AlunoDB).filter(aluno_model.AlunoDB.id_aluno == id_aluno)
    aluno = session.execute(query_aluno).scalar_one_or_none()

    if not aluno:
        abort(HTTPStatus.NOT_FOUND, description="Nenhum aluno encontrado para o ID fornecido.")

    query_atividades = select(atividade_model.AtividadeDB).filter(atividade_model.AtividadeDB.id_aluno == id_aluno).order_by(atividade_model.AtividadeDB.data_inicio.desc(), atividade_model.AtividadeDB.hora_inicio.desc())
    atividades = session.execute(query_atividades).scalars().all()

    if not atividades:
        abort(HTTPStatus.NOT_FOUND, detail="Nenhuma atividade encontrada para o aluno.")

    response_atividades = []
    for atividade in atividades:
        response_atividades.append(
            atividade.AtividadeHistorico(
                id_atividade=atividade.id_atividade,
                data_inicio=atividade.data_inicio,
                hora_inicio=atividade.hora_inicio,
                duracao=atividade.duracao,
                status=atividade.status
            )
        )
    return response_atividades

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)