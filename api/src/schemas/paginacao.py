from pydantic import BaseModel

TAMANHO_PADRAO = 20
TAMANHO_MAXIMO = 100
# Teto para o OFFSET não estourar o inteiro do PostgreSQL.
PAGINA_MAXIMA = 10_000


class Pagina[T](BaseModel):
    itens: list[T]
    total: int
