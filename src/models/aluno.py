from pydantic import BaseModel


class DadosAluno(BaseModel):
    """Dados do aluno (para boletos educacionais)"""

    nome: str
    matricula: str
    curso: str
    turno: str
    codigo: str
