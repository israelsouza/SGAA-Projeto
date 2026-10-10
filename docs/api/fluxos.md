# Fluxos e convenções da API

O que a API do SGAA espera além do que o Swagger mostra: as convenções comuns a todas as rotas, a ordem das chamadas em cada fluxo e os limites dos códigos de verificação.

A referência de cada rota (entrada, saída, campos e status) é o Swagger, em `/docs`, gerado a partir do código e sempre atualizado. Para acessá-lo localmente, ver [Iniciar Servidor Local](../../api/docs/primeiros_passos/iniciar_servidor_local.md).

- [Convenções](#convenções)
- [Fluxos](#fluxos)
- [Limites dos códigos](#limites-dos-códigos)

---

## Convenções

- Corpos de requisição e resposta em JSON.
- Campos desconhecidos no corpo são rejeitados com `422`.
- Rotas autenticadas exigem o cabeçalho `Authorization: Bearer <token>`.

### Tokens

| Token | Como obter | Onde vale |
| --- | --- | --- |
| Token de acesso (`access_token`) | Login ou conclusão do primeiro acesso | Rotas autenticadas. Algumas exigem usuário do tipo `professor`. |
| `token_primeiro_acesso` | Validação do código de primeiro acesso | Apenas no envio do formulário de primeiro acesso |

### Formato dos erros

| Status | Corpo | Quando |
| --- | --- | --- |
| `422` | `{"detail": [{"type": "...", "loc": ["body", "campo"], "msg": "..."}]}` | Corpo inválido. `loc` indica o campo; o valor enviado nunca é devolvido. |
| Demais | `{"detail": "mensagem"}` | Erros de regra de negócio, autenticação e permissão. |

Erros comuns a todas as rotas autenticadas:

| Status | `detail` | Quando |
| --- | --- | --- |
| `401` | `Não autenticado` | Token ausente, malformado, expirado, invalidado ou do tipo errado para a rota. |
| `403` | `Sem permissão para esta ação` | Token válido, mas o tipo de usuário não pode usar a rota. |

---

## Fluxos

### Login

`POST /auth/login` devolve o token de acesso.

- A resposta de erro é idêntica para e-mail inexistente, senha errada, conta sem senha e conta bloqueada.
- Após 5 senhas erradas seguidas, a conta fica bloqueada por 15 minutos.
- `POST /auth/sair-de-todos` invalida todos os tokens do usuário, inclusive o usado na chamada.

### Primeiro acesso do aluno

| Passo | Quem | Rota | Resultado |
| --- | --- | --- | --- |
| 0 | Professor | `POST /usuarios/alunos` | Conta criada sem senha; aluno recebe um código por e-mail (vale 72 h). |
| 1 | Aluno | `POST /auth/primeiro-acesso/codigo` | Opcional: pede um código novo (vale 15 min) se o do convite expirou ou foi usado. |
| 2 | Aluno | `POST /auth/primeiro-acesso/validar-codigo` | Código consumido; devolve `token_primeiro_acesso` (vale 30 min). |
| 3 | Aluno | `POST /auth/primeiro-acesso/aluno` | Perfil e senha gravados; devolve o `access_token` (já entra logado). |

Enquanto o passo 3 não é concluído, a conta não tem senha: o login falha e a redefinição de senha não atende esse e-mail.

- **Passo 0**: se o envio do e-mail falhar (`502`), o cadastro é desfeito; basta repetir a chamada. O e-mail de um usuário removido continua reservado e gera `409`.
- **Passo 1**: responde `202` com a mesma mensagem exista ou não o e-mail. O código só é enviado para contas que ainda não concluíram o primeiro acesso.
- **Passo 2**: o código é consumido nessa chamada. Se o token expirar antes do envio do formulário, é preciso pedir um código novo. O `usuario.tipo` da resposta indica qual formulário exibir; hoje só existe o do aluno.
- **Passo 3**: a API calcula pela data de nascimento se o aluno tem responsável; não existe campo para informar isso. Para menor de 18, CPF e telefone são os do responsável. Um `409` (CPF já cadastrado) não invalida o token: basta corrigir e reenviar. Depois de concluído, o `token_primeiro_acesso` deixa de valer.

### Redefinição de senha

| Passo | Rota | Resultado |
| --- | --- | --- |
| 1 | `POST /auth/esqueci-senha` | Código enviado por e-mail (vale 15 min). |
| 2 | `POST /auth/redefinir-senha` | Senha trocada; todos os tokens anteriores deixam de valer. |

Só atende contas que já concluíram o primeiro acesso.

- **Passo 1**: responde `202` com a mesma mensagem exista ou não o e-mail, e mesmo que o envio falhe.
- **Passo 2**: a senha não pode ser igual ao e-mail. Em caso de sucesso, o bloqueio de login é removido.

---

## Limites dos códigos

Valem para o primeiro acesso e para a redefinição de senha.

| Regra | Valor |
| --- | --- |
| Formato | 6 dígitos |
| Validade | 15 minutos (72 horas no código do convite) |
| Tentativas erradas por código | 5; depois disso o código deixa de valer |
| Intervalo mínimo entre pedidos | 60 segundos |
| Pedidos por hora | 5 |
| Código anterior | Deixa de valer quando um novo é emitido |

Pedidos acima do limite recebem a resposta normal (`202`), mas nenhum e-mail é enviado.
