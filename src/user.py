from pydantic import BaseModel

class User(BaseModel):
    id: str
    nome: str
    idade: int
    score: int
    ativo: bool
    pais: str
    equipe: dict
    logs: list[dict]