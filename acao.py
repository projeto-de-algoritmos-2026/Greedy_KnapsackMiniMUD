from dataclasses import dataclass


@dataclass(frozen=True)
class Acao:
    nome: str
    custo_mana: int
    dano: int
    descricao: str
