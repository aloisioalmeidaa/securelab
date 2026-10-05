# 🔐 SecureLab

O **SecureLab** é uma aplicação Web para registro e acompanhamento simplificado de amostras laboratoriais.

O projeto foi desenvolvido para a disciplina de **Projeto Aplicado**, com foco na implementação prática dos conceitos de **Secure by Design**, **Secure by Default**, segurança de aplicações Web, controle de versão e implantação automatizada.

A aplicação foi desenvolvida em Python utilizando o framework Flask e permite que um usuário autenticado cadastre, consulte, atualize e exclua amostras laboratoriais.

---

# 🎯 Objetivo do projeto

O objetivo do SecureLab é demonstrar o desenvolvimento de uma aplicação Web simples, porém funcional, incorporando práticas de segurança desde as primeiras etapas do desenvolvimento.

O sistema permite realizar o acompanhamento básico do ciclo de uma amostra laboratorial:

```text
Login
  ↓
Dashboard
  ↓
Cadastrar amostra
  ↓
Armazenar no banco SQLite
  ↓
Consultar amostras
  ↓
Atualizar status e observação
  ↓
Excluir amostra
```

Além das funcionalidades da aplicação, o projeto contempla:

- Controle de versão com Git;
- Repositório público no GitHub;
- Proteção de credenciais;
- Banco de dados SQLite;
- Proteção contra CSRF;
- Controle de acesso;
- Gerenciamento de sessão;
- Cabeçalhos HTTP de segurança;
- Mitigações relacionadas ao OWASP Top 10:2025;
- Futuro deploy em servidor Linux;
- HTTPS;
- Hardening do servidor;
- CI/CD utilizando GitHub Actions.

---

# 🧪 Funcionalidades

O SecureLab atualmente possui:

- Login de usuário;
- Dashboard protegido por autenticação;
- Cadastro de amostras;
- Listagem das amostras cadastradas;
- Persistência de dados em SQLite;
- Atualização do status da amostra;
- Atualização das observações;
- Exclusão de amostras;
- Página de confirmação antes da exclusão;
- Logout seguro;
- Sessão com tempo de expiração;
- Proteção CSRF;
- Cabeçalhos HTTP de segurança;
- Senhas armazenadas utilizando hash;
- Credenciais fora do código-fonte.

---

# 🧫 Dados armazenados para cada amostra

Cada amostra contém:

```text
ID
Identificador
Tipo
Data
Status
Observação
```

Exemplo:

```text
Identificador: AMO-001
Tipo: Soro
Data: 2026-10-05
Status: Em análise
Observação: Amostra recebida para análise.
```

Os possíveis status atualmente são:

```text
Recebida
Em análise
Finalizada
```

---

# 🛠️ Tecnologias utilizadas

## Backend

- Python
- Flask
- Flask-WTF
- Werkzeug
- python-dotenv

## Banco de dados

- SQLite

## Frontend

- HTML5
- CSS3
- Jinja2

## Versionamento

- Git
- GitHub

## Infraestrutura planejada

- Linux Ubuntu ou Debian
- Nginx
- SSH
- UFW
- Fail2Ban
- Certbot
- Let's Encrypt

## CI/CD planejado

- GitHub Actions
- GitHub Secrets

---

# 📁 Estrutura do projeto

```text
securelab/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── nova_amostra.html
│   ├── editar_amostra.html
│   └── confirmar_exclusao.html
│
└── static/
    └── style.css
```

Os seguintes arquivos locais não são enviados ao GitHub:

```text
.env
.venv/
securelab.db
__pycache__/
```

---

# 🗄️ Banco de dados

A aplicação utiliza SQLite.

O banco é criado automaticamente com o nome:

```text
securelab.db
```

A tabela utilizada é:

```text
amostras
```

Sua estrutura é:

```sql
CREATE TABLE IF NOT EXISTS amostras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identificador TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL,
    data TEXT NOT NULL,
    status TEXT NOT NULL,
    observacao TEXT
)
```

O arquivo do banco não é enviado para o GitHub.

---

# 🔑 Variáveis de ambiente

Informações sensíveis não ficam diretamente no código-fonte.

A aplicação utiliza as seguintes variáveis:

```text
SECRET_KEY
APP_USERNAME
APP_PASSWORD_HASH
```

Elas são armazenadas localmente no arquivo:

```text
.env
```

Exemplo de estrutura:

```env
SECRET_KEY=sua_chave_secreta
APP_USERNAME=seu_usuario
APP_PASSWORD_HASH=hash_da_senha
```

O arquivo `.env` está listado no `.gitignore` e não é enviado para o repositório público.

---

# 🔒 Segurança

O projeto implementa controles associados ao **OWASP Top 10:2025**.

As principais categorias abordadas atualmente são:

```text
A01:2025 - Broken Access Control
A02:2025 - Security Misconfiguration
A05:2025 - Injection
A07:2025 - Authentication Failures
```

---

# 🛡️ A01:2025 - Broken Access Control

As páginas internas da aplicação só podem ser acessadas depois da autenticação.

Antes de permitir acesso às rotas protegidas, é realizada a verificação:

```python
if not session.get("authenticated"):
    return redirect(url_for("login"))
```

Esse controle é aplicado em funcionalidades como:

```text
/dashboard
/amostras/nova
/amostras/<id>/editar
/amostras/<id>/excluir
```

Dessa forma, usuários não autenticados não podem acessar diretamente as funcionalidades de gerenciamento de amostras.

---

# 🛡️ Proteção CSRF

Os formulários que alteram o estado da aplicação são protegidos com tokens CSRF.

A proteção é habilitada por:

```python
csrf = CSRFProtect(app)
```

Os formulários possuem um token:

```html
<input
    type="hidden"
    name="csrf_token"
    value="{{ csrf_token() }}"
>
```

A proteção é utilizada nas operações de:

- Login;
- Cadastro de amostra;
- Edição da amostra;
- Exclusão da amostra;
- Logout.

---

# ⚙️ A02:2025 - Security Misconfiguration

Foram implementadas configurações destinadas a reduzir riscos causados por configurações inseguras.

O modo debug do Flask permanece desabilitado:

```python
app.run(debug=False)
```

Também foram adicionados cabeçalhos HTTP de segurança:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy
```

A implementação é realizada por:

```python
@app.after_request
def add_security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'"
    )

    return response
```

Esses controles auxiliam na redução de riscos como:

- Clickjacking;
- MIME sniffing;
- Carregamento de conteúdo não autorizado;
- Exposição desnecessária de informações.

---

# 💉 A05:2025 - Injection

As consultas ao banco de dados utilizam parâmetros em vez de concatenar entradas fornecidas pelo usuário diretamente ao SQL.

Exemplo de inserção:

```python
cursor.execute(
    """
    INSERT INTO amostras
    (identificador, tipo, data, status, observacao)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        identificador,
        tipo,
        data,
        status,
        observacao
    )
)
```

Exemplo de consulta:

```python
cursor.execute(
    """
    SELECT *
    FROM amostras
    WHERE id = ?
    """,
    (amostra_id,)
)
```

Exemplo de exclusão:

```python
cursor.execute(
    """
    DELETE FROM amostras
    WHERE id = ?
    """,
    (amostra_id,)
)
```

O valor informado pelo usuário não é incorporado diretamente ao comando SQL.

Essa abordagem reduz o risco de ataques de SQL Injection.

---

# 👤 A07:2025 - Authentication Failures

As credenciais não são inseridas diretamente no código-fonte.

O usuário é carregado através de:

```python
os.getenv("APP_USERNAME")
```

O hash da senha é carregado por:

```python
os.getenv("APP_PASSWORD_HASH")
```

A senha original não é armazenada pela aplicação.

A validação é realizada utilizando:

```python
check_password_hash(password_hash, password)
```

---

# 🔐 Hash da senha

A senha é transformada em um hash utilizando recursos disponibilizados pelo Werkzeug.

Para gerar um hash localmente:

```powershell
python -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('Digite a senha: ')))"
```

A senha em texto puro não deve ser armazenada no código-fonte nem enviada ao GitHub.

---

# 🍪 Segurança da sessão

O SecureLab utiliza configurações adicionais para o cookie de sessão:

```python
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
```

## HttpOnly

O atributo `HttpOnly` impede que scripts executados no navegador acessem diretamente o cookie da sessão.

## SameSite

O atributo `SameSite=Lax` limita o envio do cookie em determinados contextos originados por outros sites.

---

# ⏱️ Expiração da sessão

A sessão possui duração máxima configurada de:

```text
30 minutos
```

Configuração:

```python
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
```

Após autenticação:

```python
session.permanent = True
```

---

# 🚪 Logout

O logout utiliza uma requisição HTTP POST:

```python
@app.route("/logout", methods=["POST"])
```

O formulário de logout possui proteção CSRF.

Após o logout:

```python
session.clear()
```

remove as informações da sessão.

---

# 🗑️ Exclusão segura de amostras

A exclusão de uma amostra exige uma etapa de confirmação.

O fluxo é:

```text
Dashboard
    ↓
Excluir
    ↓
Página de confirmação
    ↓
POST + CSRF
    ↓
Exclusão no SQLite
```

A exclusão efetiva utiliza uma consulta parametrizada:

```python
cursor.execute(
    """
    DELETE FROM amostras
    WHERE id = ?
    """,
    (amostra_id,)
)
```

---

# 🔐 Proteção de arquivos sensíveis

O `.gitignore` impede o envio de arquivos locais e sensíveis ao GitHub.

Exemplo:

```gitignore
.env
.venv/
securelab.db
__pycache__/
*.pyc
```

Assim, informações como:

- Chaves;
- Hashes;
- Variáveis de ambiente;
- Banco de dados local;
- Arquivos temporários;

não são incluídas no repositório público.

---

# 💻 Execução local

## 1. Clonar o projeto

```powershell
git clone REPOSITORIO_DO_PROJETO
```

Entrar na pasta:

```powershell
cd securelab
```

---

## 2. Criar ambiente virtual

```powershell
py -m venv .venv
```

---

## 3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Instalar dependências

```powershell
pip install -r requirements.txt
```

---

## 5. Criar o arquivo `.env`

Criar:

```text
.env
```

Com:

```env
SECRET_KEY=sua_chave_secreta
APP_USERNAME=seu_usuario
APP_PASSWORD_HASH=hash_da_senha
```

---

## 6. Gerar uma SECRET_KEY

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 7. Executar

```powershell
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

Durante os testes locais deve ser utilizado sempre o mesmo host para preservar corretamente o cookie de sessão.

---

# 🧪 Testes funcionais

## Login válido

Resultado esperado:

```text
Login
  ↓
Dashboard
```

---

## Login inválido

Resultado esperado:

```text
Usuário ou senha inválidos.
```

---

## Acesso ao dashboard sem autenticação

Tentar acessar:

```text
/dashboard
```

Resultado esperado:

```text
Redirecionamento para Login
```

---

## Cadastro de amostra

Resultado esperado:

```text
Nova amostra
  ↓
Validação
  ↓
SQLite
  ↓
Dashboard
```

---

## Edição

O usuário pode alterar:

```text
Status
Observação
```

A alteração é persistida no SQLite.

---

## Exclusão

Resultado esperado:

```text
Excluir
  ↓
Confirmação
  ↓
POST protegido por CSRF
  ↓
Registro removido
```

---

# 🔎 Verificação dos cabeçalhos HTTP

Os cabeçalhos podem ser verificados localmente com:

```powershell
curl.exe -I http://127.0.0.1:5000
```

Entre os cabeçalhos esperados estão:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy
```

O cookie de sessão deve apresentar:

```text
HttpOnly
SameSite=Lax
```

---

# ☁️ Arquitetura planejada para produção

A arquitetura final prevista é:

```text
                 Internet
                    │
                    ▼
                  HTTPS
                    │
                    ▼
                  Nginx
                    │
                    ▼
                SecureLab
                 Flask
                    │
                    ▼
                  SQLite
```

O servidor de desenvolvimento fornecido pelo Flask não será exposto diretamente à Internet.

---

# 🔥 Firewall

Na infraestrutura de produção serão liberadas somente as portas necessárias.

```text
22  → SSH
80  → HTTP
443 → HTTPS
```

O princípio utilizado será o de menor privilégio.

---

# 🔑 SSH

O acesso administrativo ao servidor deverá utilizar autenticação por chave SSH.

O login por senha deverá ser restringido quando a infraestrutura estiver devidamente configurada.

---

# 🛡️ Fail2Ban

O servidor será protegido utilizando Fail2Ban.

Configuração planejada de acordo com os requisitos da disciplina:

```text
Máximo de tentativas: 4
Tempo de banimento: 24 horas
```

---

# 🔐 HTTPS

A aplicação em produção utilizará:

```text
Nginx
Certbot
Let's Encrypt
```

O tráfego HTTP deverá ser redirecionado para HTTPS.

Quando HTTPS estiver configurado, também será habilitado:

```python
app.config["SESSION_COOKIE_SECURE"] = True
```

Isso fará com que o cookie de sessão seja enviado somente por conexões HTTPS.

---

# 🔄 CI/CD

O deploy será automatizado utilizando GitHub Actions.

Fluxo planejado:

```text
Desenvolvimento
      │
      │ git push
      ▼
    GitHub
      │
      ▼
GitHub Actions
      │
      │ SSH
      ▼
Servidor Linux
      │
      ▼
Atualização da aplicação
```

---

# 🔑 GitHub Secrets

As credenciais utilizadas pelo pipeline não serão armazenadas diretamente no workflow.

Serão utilizados GitHub Secrets para informações como:

```text
SERVER_HOST
SERVER_USER
SSH_PRIVATE_KEY
```

---

# ✅ Checklist do projeto

## Aplicação

- [x] Login
- [x] Dashboard protegido
- [x] Cadastro de amostras
- [x] Persistência em SQLite
- [x] Listagem de amostras
- [x] Atualização de status
- [x] Atualização de observações
- [x] Exclusão de amostras
- [x] Confirmação antes da exclusão
- [x] Logout
- [x] Interface HTML/CSS

## Segurança

- [x] Hash de senha
- [x] Variáveis de ambiente
- [x] `.gitignore`
- [x] Proteção CSRF
- [x] Sessão autenticada
- [x] Expiração da sessão
- [x] Cookie HttpOnly
- [x] SameSite
- [x] Cabeçalhos HTTP de segurança
- [x] Consultas SQL parametrizadas

## OWASP Top 10:2025

- [x] A01 - Broken Access Control
- [x] A02 - Security Misconfiguration
- [x] A05 - Injection
- [x] A07 - Authentication Failures

## GitHub

- [x] Repositório público
- [x] Histórico de commits
- [x] `.gitignore`
- [x] README
- [x] Código-fonte versionado
- [x] Segredos fora do repositório

## Infraestrutura

- [ ] Servidor Linux em nuvem
- [ ] SSH com chave
- [ ] Firewall
- [ ] Fail2Ban
- [ ] Nginx
- [ ] Servidor WSGI de produção

## HTTPS

- [ ] Certificado TLS
- [ ] Let's Encrypt
- [ ] Certbot
- [ ] Redirecionamento HTTP para HTTPS
- [ ] Cookie Secure
- [ ] Teste SSL/TLS

## CI/CD

- [ ] GitHub Actions
- [ ] GitHub Secrets
- [ ] Deploy automático
- [ ] Deploy após push para main

---

# 📚 Referências

Foram utilizadas como principais referências técnicas:

- OWASP Top 10:2025;
- OWASP Cheat Sheet Series - Session Management;
- OWASP Cheat Sheet Series - Cross-Site Request Forgery Prevention;
- OWASP Cheat Sheet Series - HTTP Headers;
- Flask Documentation;
- Werkzeug Documentation;
- Python sqlite3 Documentation.

---

# 📊 Status atual

Atualmente estão concluídas as etapas de:

```text
Aplicação Web
        ✓
Autenticação
        ✓
Banco SQLite
        ✓
Cadastro
        ✓
Consulta
        ✓
Edição
        ✓
Exclusão
        ✓
Controles de segurança
        ✓
Git/GitHub
        ✓
```

As próximas etapas são:

```text
1. Preparar a aplicação para produção
2. Criar servidor Linux em nuvem
3. Configurar acesso SSH
4. Configurar firewall
5. Configurar Fail2Ban
6. Configurar servidor WSGI
7. Configurar Nginx
8. Publicar o SecureLab
9. Configurar HTTPS
10. Criar pipeline GitHub Actions
11. Configurar GitHub Secrets
12. Validar deploy automático
```

---

# 👨‍💻 Autor

**Aloisio Almeida**

Projeto acadêmico desenvolvido para disciplina de pós-graduação.