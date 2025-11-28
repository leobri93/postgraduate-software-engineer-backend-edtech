from flask import abort, redirect
from flask_openapi3.openapi import OpenAPI
from flask_openapi3.models.info import Info
from flask_openapi3.models.tag import Tag
from flask_cors import CORS
from http import HTTPStatus
from schemas import aluno as alunoSchema
from schemas import atividade as atividadeSchema
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from model import models, Session
from datetime import datetime
import requests


app = OpenAPI(
    __name__,
    info=Info(
        title="API EdTech",
        version="1.0.0",
        description="API para cadastro de alunos e atividades",
    )
)
CORS(app)

aluno_tag = Tag(name="Aluno", description="Adição, remoção e listagem de alunos")
atividade_tag = Tag(name="Atividade", description="Listagem de atividades")
home_tag = Tag(name="Documentação", description="Seleção de documentação")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

def verify_date_format(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
# Rotas de Aluno
@app.post('/alunos', tags=[aluno_tag], responses={"200": alunoSchema.Aluno})
def create_aluno(form: alunoSchema.NovoAluno):
    """
    Cadastra um novo aluno.
    """
    session = Session()

    cep_raw = form.cep
    cep_digits = ''.join(filter(str.isdigit, str(cep_raw)))
    if len(cep_digits) != 8:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, description="CEP inválido. Deve conter 8 dígitos.")

    # Consulta a BrasilAPI para obter estado, cidade e rua
    estado = None
    cidade = None
    rua = None
    try:
        resp = requests.get(f"https://brasilapi.com.br/api/cep/v2/{cep_digits}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            estado = data.get('state')
            cidade = data.get('city')
            rua = data.get('street') or data.get('logradouro')
    except requests.RequestException:
        estado = ""
        cidade = ""
        rua = ""

    query_aluno = select(models.AlunoDB).where(models.AlunoDB.email == form.email)
    db_aluno = session.execute(query_aluno).scalar_one_or_none()
    if db_aluno:
            abort(HTTPStatus.BAD_REQUEST, description="Email já cadastrado.")
    
    if (form.data_nascimento > datetime.now().date() or 
        form.data_nascimento < datetime(1900, 1, 1).date() or 
        verify_date_format(str(form.data_nascimento)) is False):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, description="Data de nascimento inválida.")
    
    new_aluno = models.AlunoDB(
        nome=form.nome,
        email=form.email,
        data_nascimento=form.data_nascimento,
        data_cadastro=datetime.now(),
        cep=cep_digits,
        estado=estado,
        cidade=cidade,
        rua=rua
    )
    
    session.add(new_aluno)
    session.commit()
    return alunoSchema.apresentar_aluno(new_aluno), 200

@app.delete('/alunos', tags=[aluno_tag], responses={"200": alunoSchema.AlunoDelSchema})
def delete_aluno(query: alunoSchema.AlunoBuscaSchema):
    """
    Remove um aluno pelo ID.
    """
    session = Session()

    query_aluno = select(models.AlunoDB).where(models.AlunoDB.id_aluno == query.id_aluno)
    aluno = session.execute(query_aluno).scalar_one_or_none()

    if not aluno:
        abort(HTTPStatus.NOT_FOUND, description="Nenhum aluno encontrado para o ID fornecido.")
    
    session.delete(aluno)
    session.commit()
    return {"message": "Aluno removido com sucesso.", "id_aluno": query.id_aluno}

@app.get('/alunos', tags=[aluno_tag], responses={"200" : alunoSchema.ListagemAlunos})
def list_alunos():
    """
    Lista todos os alunos cadastrados.
    """
    session = Session()

    alunos = session.query(models.AlunoDB).all()
    if not alunos:
        return {"alunos": []}, 200
    return alunoSchema.apresentar_aluno_listagem(alunos), 200

#Rota de atividade
@app.post("/atividades", tags=[atividade_tag], responses={"200": atividadeSchema.Atividade})
def create_atividade(query: alunoSchema.AlunoBuscaSchema):
    """
    Inicia uma nova atividade para um aluno através de seu ID.
    """
    session = Session()

    query_aluno = select(models.AlunoDB).filter(models.AlunoDB.id_aluno == query.id_aluno)
    aluno = session.execute(query_aluno).scalar_one_or_none()

    if not aluno:
        abort(HTTPStatus.NOT_FOUND, description="Nenhum aluno encontrado para o ID fornecido.")
    
    new_atividade = models.AtividadeDB(
        id_aluno=query.id_aluno,
        data_inicio=datetime.now().date(),
        hora_inicio=datetime.now().time(),
        duracao=0, # Duração inicial é 0, será atualizada posteriormente
        status="iniciada"  # Status inicial da atividade
    )
    
    session.add(new_atividade)
    session.commit()
    
    return atividadeSchema.apresentar_atividade(new_atividade), 200

@app.get("/atividades", tags=[atividade_tag], responses={"200": atividadeSchema.ListagemAtividades})
def get_atividades_aluno(query: alunoSchema.AlunoBuscaSchema):
    """
    Retorna o histórico de todas as atividades de um aluno através de seu ID.
    """
    session = Session()

    query_aluno = select(models.AlunoDB).filter(models.AlunoDB.id_aluno == query.id_aluno)
    aluno = session.execute(query_aluno).scalar_one_or_none()

    if not aluno:
        abort(HTTPStatus.NOT_FOUND, description="Nenhum aluno encontrado para o ID fornecido.")

    query_atividades = select(models.AtividadeDB).filter(models.AtividadeDB.id_aluno == query.id_aluno)
    atividades = session.execute(query_atividades).scalars().all()

    if not atividades:
        abort(HTTPStatus.NOT_FOUND, description="Nenhuma atividade encontrada para o aluno.")

    response_atividades = []
    for atividade in atividades:
        response_atividades.append(
            atividadeSchema.Atividade(
                id_atividade=atividade.id_atividade,
                id_aluno=atividade.id_aluno,
                data_inicio=atividade.data_inicio,
                hora_inicio=atividade.hora_inicio,
                duracao=atividade.duracao,
                status=atividade.status
            )
        )
    return atividadeSchema.apresentar_atividade_listagem(response_atividades), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)