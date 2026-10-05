# 🔐 SecureLab

O **SecureLab** é uma aplicação Web para registro e acompanhamento simplificado de amostras laboratoriais, desenvolvida como projeto acadêmico para a disciplina de **Projeto Aplicado**.

O projeto foi construído com foco na aplicação prática dos conceitos de:

- **Secure by Design**
- **Secure by Default**
- Segurança de aplicações Web
- Controle de acesso
- Proteção de credenciais
- Segurança de infraestrutura
- Versionamento com Git
- Implantação automatizada com CI/CD

A aplicação foi desenvolvida em Python utilizando Flask e permite que um usuário autenticado cadastre, consulte, altere e exclua registros de amostras laboratoriais.

---

# 🌐 Aplicação em produção

A aplicação está atualmente publicada em uma máquina virtual Linux no Google Cloud.

Endereço:

```text
https://35.208.74.160
```

O acesso HTTP é automaticamente redirecionado para HTTPS.

---

# 🎯 Objetivo do projeto

O objetivo do SecureLab é demonstrar o desenvolvimento e a implantação de uma aplicação Web funcional incorporando práticas de segurança durante todo o ciclo de vida do software.

O fluxo básico da aplicação é:

```text
Login
  ↓
Dashboard
  ↓
Cadastrar amostra
  ↓
Persistir no SQLite
  ↓
Consultar amostras
  ↓
Editar status e observações
  ↓
Excluir amostra
```

O fluxo de desenvolvimento e implantação é:

```text
Desenvolvimento local
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
 Google Cloud VM
        │
        ▼
      Nginx
        │
        ▼
     Gunicorn
        │
        ▼
      Flask
        │
        ▼
      SQLite
```

---

# 🧪 Funcionalidades

O SecureLab possui atualmente:

- Login de usuário;
- Autenticação utilizando senha armazenada como hash;
- Dashboard protegido;
- Cadastro de amostras laboratoriais;
- Listagem de amostras cadastradas;
- Persistência utilizando SQLite;
- Alteração do status da amostra;
- Alteração de observações;
- Exclusão de amostras;
- Página de confirmação antes da exclusão;
- Logout seguro;
- Controle de sessão;
- Expiração da sessão;
- Proteção CSRF;
- Cabeçalhos HTTP de segurança;
- Interface Web responsiva simples.

---

# 🧫 Estrutura de uma amostra

Cada registro contém:

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

Os possíveis status são:

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
- Gunicorn

## Banco de dados

- SQLite

## Frontend

- HTML5
- CSS3
- Jinja2

## Versionamento

- Git
- GitHub

## Infraestrutura

- Google Cloud Compute Engine
- Debian GNU/Linux 13 (trixie)
- Nginx
- Gunicorn
- UFW
- Fail2Ban
- SSH
- systemd

## Segurança TLS

- HTTPS
- TLS 1.2
- TLS 1.3
- Let's Encrypt
- Certbot
- Certificado TLS para endereço IP
- Renovação automática do certificado

## CI/CD

- GitHub Actions
- GitHub Secrets
- SSH
- Deploy automático após push na branch `main`

---

# 📁 Estrutura do projeto

```text
securelab/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── nova_amostra.html
│   ├── editar_amostra.html
│   └── confirmar_exclusao.html
│
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

Os seguintes arquivos são locais e não são enviados ao GitHub:

```text
.env
.venv/
securelab.db
__pycache__/
*.pyc
```

---

# 🗄️ Banco de dados

A aplicação utiliza **SQLite**.

O banco é criado automaticamente:

```text
securelab.db
```

A tabela principal é:

```text
amostras
```

Estrutura:

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

O arquivo `securelab.db` não é versionado pelo Git.

Isso permite que o banco existente no servidor de produção não seja sobrescrito pelos deploys realizados através do GitHub Actions.

---

# 🔑 Variáveis de ambiente

Informações sensíveis não ficam armazenadas diretamente no código-fonte.

A aplicação utiliza:

```text
SECRET_KEY
APP_USERNAME
APP_PASSWORD_HASH
APP_ENV
```

No servidor de produção:

```env
SECRET_KEY=chave_secreta
APP_USERNAME=usuario
APP_PASSWORD_HASH=hash_da_senha
APP_ENV=production
```

O arquivo:

```text
.env
```

está incluído no `.gitignore`.

Em produção, sua permissão foi restringida utilizando:

```bash
chmod 600 .env
```

Dessa forma, apenas o proprietário do arquivo pode ler ou alterá-lo.

---

# 🔒 Segurança da aplicação

O SecureLab implementa controles associados a diferentes categorias do **OWASP Top 10:2025**.

As principais categorias abordadas são:

```text
A01:2025 - Broken Access Control
A02:2025 - Security Misconfiguration
A05:2025 - Injection
A07:2025 - Authentication Failures
```

---

# 🛡️ A01:2025 - Broken Access Control

Rotas internas da aplicação exigem autenticação.

Antes de permitir acesso, a aplicação verifica:

```python
if not session.get("authenticated"):
    return redirect(url_for("login"))
```

Esse controle é aplicado em rotas como:

```text
/dashboard
/amostras/nova
/amostras/<id>/editar
/amostras/<id>/excluir
```

Assim, um usuário não autenticado não consegue acessar diretamente as funcionalidades de gerenciamento das amostras.

---

# 🛡️ Proteção contra CSRF

Operações que alteram o estado da aplicação utilizam proteção contra **Cross-Site Request Forgery**.

A proteção é habilitada através de:

```python
csrf = CSRFProtect(app)
```

Os formulários possuem token CSRF:

```html
<input
    type="hidden"
    name="csrf_token"
    value="{{ csrf_token() }}"
>
```

A proteção é utilizada em:

- Login;
- Cadastro de amostras;
- Edição de amostras;
- Exclusão;
- Logout.

O logout utiliza uma requisição POST:

```python
@app.route("/logout", methods=["POST"])
```

---

# ⚙️ A02:2025 - Security Misconfiguration

Foram aplicadas diversas configurações para reduzir riscos relacionados a configurações inseguras.

O modo de depuração permanece desabilitado:

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

Implementação:

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

Esses controles auxiliam na mitigação de:

- Clickjacking;
- MIME sniffing;
- Carregamento de conteúdo não autorizado;
- Determinados vetores de injeção de conteúdo;
- Vazamento desnecessário de informações.

---

# 💉 A05:2025 - Injection

As operações SQLite utilizam **queries parametrizadas**.

Entradas fornecidas pelo usuário não são concatenadas diretamente ao comando SQL.

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

Consulta parametrizada:

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

Exclusão:

```python
cursor.execute(
    """
    DELETE FROM amostras
    WHERE id = ?
    """,
    (amostra_id,)
)
```

Essa abordagem reduz o risco de **SQL Injection**.

---

# 👤 A07:2025 - Authentication Failures

As credenciais não são inseridas diretamente no código-fonte.

O usuário é obtido através de:

```python
os.getenv("APP_USERNAME")
```

O hash:

```python
os.getenv("APP_PASSWORD_HASH")
```

A validação utiliza:

```python
check_password_hash(password_hash, password)
```

A aplicação não precisa armazenar a senha original.

---

# 🔐 Hash da senha

A senha é transformada em hash utilizando o Werkzeug.

Exemplo para gerar um hash:

```powershell
python -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('Digite a senha: ')))"
```

A senha em texto puro não deve ser armazenada:

- no código;
- no GitHub;
- no workflow;
- em commits;
- em arquivos públicos.

---

# 🍪 Segurança da sessão

A aplicação utiliza:

```python
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
```

## HttpOnly

Impede que JavaScript executado no navegador acesse diretamente o cookie de sessão.

## SameSite

Reduz o envio do cookie em determinados contextos entre sites diferentes.

---

# 🔐 Cookie Secure em produção

No ambiente de produção também é utilizado:

```python
app.config["SESSION_COOKIE_SECURE"] = (
    os.getenv("APP_ENV") == "production"
)
```

No servidor:

```env
APP_ENV=production
```

Portanto, o navegador envia o cookie de sessão apenas através de conexões HTTPS.

---

# ⏱️ Expiração da sessão

A duração máxima da sessão é:

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

# 🗑️ Exclusão segura de amostras

O fluxo de exclusão possui confirmação:

```text
Dashboard
    ↓
Excluir
    ↓
Página de confirmação
    ↓
POST
    ↓
Token CSRF
    ↓
DELETE parametrizado
```

A exclusão efetiva utiliza:

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

O `.gitignore` impede o versionamento de arquivos sensíveis ou locais:

```gitignore
.env
.venv/
securelab.db
__pycache__/
*.pyc
```

Dessa forma, informações como:

- Chaves;
- Credenciais;
- Hashes;
- Variáveis de ambiente;
- Banco local;
- Arquivos temporários;

não são publicadas no GitHub.

---

# 💻 Execução local

## 1. Clonar o repositório

```powershell
git clone https://github.com/aloisioalmeidaa/securelab.git
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

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Instalar dependências

```powershell
pip install -r requirements.txt
```

---

## 5. Criar `.env`

Exemplo:

```env
SECRET_KEY=sua_chave
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

Durante o ambiente local deve ser utilizado sempre o mesmo hostname para que o cookie de sessão seja preservado.

---

# ☁️ Infraestrutura de produção

A aplicação está hospedada no **Google Cloud Compute Engine**.

Configuração utilizada:

```text
VM: securelab-vm
Sistema operacional: Debian GNU/Linux 13 (trixie)
Família: E2
Tipo: e2-micro
Região: us-central1
Disco: Persistent Disk Standard
Tamanho: 10 GB
IP externo: estático
```

O IP público foi reservado como:

```text
securelab-ip
```

Endereço:

```text
35.208.74.160
```

---

# 🏗️ Arquitetura de produção

```text
Internet
    │
    ▼
Firewall Google Cloud
    │
    ▼
UFW
    │
    ▼
Nginx :80 / :443
    │
    ▼
Gunicorn :8000
    │
    ▼
Flask
    │
    ▼
SQLite
```

O Gunicorn escuta apenas localmente:

```text
127.0.0.1:8000
```

Portanto, ele não fica diretamente exposto à Internet.

---

# 🔥 Firewall

Foi utilizado o UFW.

Política:

```text
Entrada: deny
Saída: allow
```

Portas liberadas:

```text
22/tcp      SSH
80/tcp      HTTP
443/tcp     HTTPS
```

Perfis utilizados:

```text
OpenSSH
Nginx Full
```

Verificação:

```bash
sudo ufw status verbose
```

---

# 🔑 SSH

O acesso administrativo utiliza autenticação baseada em chave SSH.

Foi verificado que:

```text
pubkeyauthentication yes
passwordauthentication no
```

Para o CI/CD também foi criada uma chave SSH exclusiva:

```text
github-actions-securelab
```

A chave privada fica armazenada exclusivamente em um GitHub Secret.

---

# 🛡️ Fail2Ban

O Fail2Ban protege o SSH contra tentativas repetidas de autenticação.

Configuração:

```ini
[sshd]
enabled = true
port = ssh
maxretry = 4
bantime = 24h
findtime = 10m
```

Validação:

```bash
sudo fail2ban-client get sshd maxretry
```

Resultado:

```text
4
```

Validação do tempo de banimento:

```bash
sudo fail2ban-client get sshd bantime
```

Resultado:

```text
86400
```

Ou seja:

```text
86400 segundos = 24 horas
```

---

# 🚀 Gunicorn

O servidor Flask de desenvolvimento não é utilizado diretamente em produção.

O ambiente utiliza Gunicorn:

```text
Nginx
   ↓
Gunicorn
   ↓
Flask
```

Execução:

```bash
gunicorn --workers 1 --bind 127.0.0.1:8000 app:app
```

O processo é gerenciado pelo systemd através do serviço:

```text
securelab.service
```

Verificação:

```bash
sudo systemctl status securelab
```

---

# 🌐 Nginx

O Nginx funciona como reverse proxy.

Fluxo:

```text
Cliente
   ↓
HTTPS :443
   ↓
Nginx
   ↓
127.0.0.1:8000
   ↓
Gunicorn
```

Também é responsável por:

- TLS;
- Redirecionamento HTTP → HTTPS;
- Proxy reverso;
- Exposição pública da aplicação.

---

# 🔐 HTTPS

O ambiente utiliza certificado TLS emitido pelo **Let's Encrypt** diretamente para o endereço IP público:

```text
35.208.74.160
```

Os arquivos do certificado ficam em:

```text
/etc/letsencrypt/live/35.208.74.160/fullchain.pem
/etc/letsencrypt/live/35.208.74.160/privkey.pem
```

Protocolos habilitados no Nginx:

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
```

---

# 🔁 Redirecionamento HTTP → HTTPS

A porta HTTP permanece disponível apenas para:

- Redirecionamento para HTTPS;
- Desafio ACME do Let's Encrypt.

Fluxo:

```text
http://35.208.74.160
          ↓
301 Redirect
          ↓
https://35.208.74.160
```

---

# ♻️ Renovação automática do certificado

O certificado é renovado automaticamente utilizando Certbot e systemd.

Serviço:

```text
certbot-renew.service
```

Timer:

```text
certbot-renew.timer
```

O timer verifica a renovação três vezes ao dia:

```text
00:00
08:00
16:00
```

Após uma renovação bem-sucedida:

```bash
systemctl reload nginx
```

é executado automaticamente.

A renovação foi validada através de:

```bash
sudo /opt/certbot/bin/certbot renew --dry-run
```

Resultado:

```text
Congratulations, all simulated renewals succeeded!
```

---

# 🔎 Validação SSL/TLS

A configuração TLS foi analisada externamente.

## SSL Certificate Checker

Destino testado:

```text
35.208.74.160:443
```

Principais resultados:

```text
Certificate Trusted: Yes
Name Matches Domain: Yes
Issuer: Let's Encrypt
Certificate Chain: Valid / Complete
Supported TLS Versions: TLS 1.2, TLS 1.3
Algorithm / Key Type: EC 256 bits
OCSP/CRL Revocation: Good, not revoked
Certificate Transparency: Compliant
```

O teste confirmou:

- Certificado confiável;
- Identidade correspondente;
- Cadeia de certificação completa;
- TLS 1.2 disponível;
- TLS 1.3 disponível;
- Certificado não revogado.

---

# 🔐 Validação PQC / Quantum Readiness

O servidor também foi analisado através do **DigiCert TLS Quantum Readiness Checker**.

Destino:

```text
35.208.74.160
```

Resultado:

```text
PASS - TLS 1.3 enabled
PASS - Quantum-safe key exchange
```

O teste confirmou que:

- TLS 1.3 está habilitado;
- O servidor possui suporte a troca de chaves quantum-safe.

Com isso, os requisitos de validação TLS e prontidão pós-quântica definidos para o projeto foram atendidos.

---

# 🔄 CI/CD

O SecureLab utiliza **GitHub Actions** para implantação automatizada.

Arquivo:

```text
.github/workflows/deploy.yml
```

O workflow é disparado quando há:

```text
push → main
```

Fluxo:

```text
Desenvolvedor
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
securelab-vm
     │
     ├── git pull
     ├── pip install
     ├── systemctl restart securelab
     └── systemctl is-active securelab
```

---

# 🔑 GitHub Secrets

Informações sensíveis utilizadas pela pipeline são armazenadas como GitHub Secrets.

Secrets utilizados:

```text
SSH_PRIVATE_KEY
SERVER_HOST
SERVER_USER
```

Nenhuma chave SSH privada ou credencial do servidor está armazenada diretamente no workflow.

---

# 🔒 Privilégio mínimo no deploy

O usuário utilizado pelo GitHub Actions não recebeu acesso `sudo` irrestrito.

Foi configurada uma regra específica permitindo apenas:

```text
systemctl restart securelab
systemctl is-active --quiet securelab
```

Isso aplica o princípio do menor privilégio ao processo de implantação.

---

# ✅ Teste do CI/CD

O workflow foi executado com sucesso no GitHub Actions.

Resultado:

```text
Status: Success
```

Durante o deploy automático foram realizadas as operações:

```text
SSH na VM
git pull
instalação/verificação das dependências
restart do SecureLab
verificação do serviço
```

Após o deploy, a aplicação permaneceu acessível e funcional.

---

# 🧪 Testes funcionais

Foram validados:

## Login

```text
Credenciais válidas
        ↓
Dashboard
```

## Login inválido

```text
Usuário ou senha inválidos.
```

## Controle de acesso

Acesso direto ao dashboard sem sessão:

```text
/dashboard
```

Resultado:

```text
Redirecionamento para login
```

## Cadastro

```text
Nova amostra
      ↓
Validação
      ↓
SQLite
      ↓
Dashboard
```

## Edição

O usuário pode alterar:

```text
Status
Observação
```

## Exclusão

```text
Excluir
   ↓
Confirmação
   ↓
POST + CSRF
   ↓
DELETE parametrizado
```

## Logout

```text
Sessão autenticada
      ↓
POST /logout
      ↓
session.clear()
      ↓
Login
```

---

# 🔎 Verificação dos cabeçalhos HTTP

Os cabeçalhos foram testados utilizando:

```bash
curl -I http://127.0.0.1:8000
```

Foram observados:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy
```

O cookie apresentou:

```text
HttpOnly
SameSite=Lax
```

Em produção também é utilizado:

```text
Secure
```

---

# ✅ Checklist final

## Aplicação

- [x] Aplicação Web funcional
- [x] Tela de login
- [x] Área interna protegida
- [x] Cadastro de amostras
- [x] Persistência SQLite
- [x] Listagem de amostras
- [x] Atualização de status
- [x] Atualização de observações
- [x] Exclusão
- [x] Confirmação antes da exclusão
- [x] Logout
- [x] Interface HTML/CSS

## Segurança

- [x] Senha armazenada como hash
- [x] Variáveis de ambiente
- [x] `.gitignore`
- [x] CSRF
- [x] Controle de sessão
- [x] Expiração da sessão
- [x] Cookie HttpOnly
- [x] Cookie SameSite
- [x] Cookie Secure
- [x] Cabeçalhos HTTP de segurança
- [x] Queries parametrizadas
- [x] Segredos fora do repositório

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
- [x] Código versionado
- [x] GitHub Secrets
- [x] Workflow CI/CD

## Infraestrutura

- [x] Google Cloud Compute Engine
- [x] Debian GNU/Linux
- [x] IP público
- [x] IP estático
- [x] SSH com chave
- [x] UFW
- [x] Fail2Ban
- [x] Nginx
- [x] Gunicorn
- [x] systemd
- [x] Princípio do menor privilégio

## HTTPS

- [x] Certificado TLS
- [x] Let's Encrypt
- [x] Certbot
- [x] HTTPS
- [x] TLS 1.2
- [x] TLS 1.3
- [x] Redirecionamento HTTP → HTTPS
- [x] Cookie Secure
- [x] Renovação automática
- [x] Teste externo do certificado
- [x] Certificate Trusted
- [x] Certificate Chain completa

## Pós-quantum / PQC

- [x] DigiCert TLS Quantum Readiness Checker
- [x] TLS 1.3 enabled
- [x] Quantum-safe key exchange
- [x] Resultado PASS

## CI/CD

- [x] GitHub Actions
- [x] GitHub Secrets
- [x] Chave SSH exclusiva
- [x] Deploy automático
- [x] Deploy após push para `main`
- [x] Reinício automático do serviço
- [x] Validação do serviço após deploy
- [x] Workflow testado com sucesso

---

# 📊 Status do projeto

```text
Aplicação Web                 ✓
Autenticação                  ✓
Banco SQLite                  ✓
Cadastro de amostras          ✓
Consulta de amostras          ✓
Edição de amostras            ✓
Exclusão de amostras          ✓
OWASP                         ✓
Git/GitHub                    ✓
Servidor Linux                ✓
SSH seguro                    ✓
Firewall                      ✓
Fail2Ban                      ✓
Gunicorn                      ✓
Nginx                         ✓
HTTPS                         ✓
Let's Encrypt                 ✓
Renovação automática          ✓
TLS 1.3                       ✓
PQC / Quantum-safe            ✓
GitHub Actions                ✓
CI/CD                         ✓
Deploy automático             ✓
```

**Status geral: concluído.**

---

# 📚 Referências técnicas

## OWASP

OWASP Top 10:2025

```text
https://top10.owasp.org/2025/
```

OWASP Cheat Sheet Series - Session Management

```text
https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
```

OWASP Cheat Sheet Series - Cross-Site Request Forgery Prevention

```text
https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
```

OWASP Cheat Sheet Series - HTTP Headers

```text
https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
```

## Flask

```text
https://flask.palletsprojects.com/
```

## Werkzeug

```text
https://werkzeug.palletsprojects.com/
```

## Python SQLite

```text
https://docs.python.org/3/library/sqlite3.html
```

## Nginx

```text
https://nginx.org/
```

## Gunicorn

```text
https://gunicorn.org/
```

## Let's Encrypt

```text
https://letsencrypt.org/
```

## Certbot

```text
https://certbot.eff.org/
```

## Google Cloud

```text
https://cloud.google.com/compute
```

## DigiCert

```text
https://www.digicert.com/pqc-checker
```

---

# 👨‍💻 Autor

**Aloisio Almeida**

Projeto acadêmico desenvolvido para disciplina de pós-graduação.

---

# 📌 Repositório

```text
https://github.com/aloisioalmeidaa/securelab
```

# 🌐 Produção

```text
https://35.208.74.160
```