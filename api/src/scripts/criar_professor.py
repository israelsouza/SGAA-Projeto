"""Cria a conta da professora. Uso: poetry run python -m src.scripts.criar_professor"""

import sys
from getpass import getpass

from pydantic import TypeAdapter, ValidationError
from sqlalchemy.orm import Session

from src.core.database import obter_engine
from src.core.security import hash_senha
from src.models.usuario import TipoUsuario
from src.schemas.tipos import Email, NomeCompleto, NovaSenha
from src.services.usuario_service import EmailJaCadastrado, criar_usuario


def main() -> int:
    try:
        nome_completo = TypeAdapter(NomeCompleto).validate_python(
            input("Nome completo: ")
        )
        email = TypeAdapter(Email).validate_python(input("E-mail: "))
        senha = TypeAdapter(NovaSenha).validate_python(getpass("Senha: "))
    except ValidationError as erro:
        print("Dado inválido: " + "; ".join(item["msg"] for item in erro.errors()))
        return 1
    if getpass("Confirme a senha: ") != senha.get_secret_value():
        print("As senhas não conferem.")
        return 1

    with Session(obter_engine()) as sessao:
        try:
            usuario = criar_usuario(
                sessao,
                nome_completo=nome_completo,
                email=email,
                tipo=TipoUsuario.PROFESSOR,
                senha_hash=hash_senha(senha.get_secret_value()),
            )
        except EmailJaCadastrado:
            print("Já existe um usuário com esse e-mail.")
            return 1
        sessao.commit()
        print(f"Professor(a) criado(a) com id {usuario.id}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
