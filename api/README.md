## Comandos importantes

Gera o arquivo `requirements.txt` a partir do `poetry.lock`. Para que não inclua as dependencias de desenvolvimento, é necessário ter a flag `--only main` no final do comando.


`poetry export -f requirements.txt --output requirements.txt --without-hashes --only main`


OBS: caso o comando apresente erro, pode ser necessário instalar o plugin de export com `poetry self add poetry-plugin-export`





## todo

- configuração para deploy na vercel [1]

- configuração para conexão com o banco de dados

- travar versão das dependências

- separação de ambiente de homologação e produção

- manual para
    - instalar, configurar
    - rodar localmente

- arquivo separado com comandos mais utilizados

- possível script para automatizar alguns fluxos de comandos

- linter e formatador de código

- testes automatizados


## todo geral

- CI com GH Actions [1]

- Regras branch [1]

- configs pra fazer a api rodar um hello word [1]


[1] a ser visto nesse sábado em conjunto
