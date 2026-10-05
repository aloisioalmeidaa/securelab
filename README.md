# 🔐 SecureLab

Projeto desenvolvido para a disciplina de **Projeto Aplicado**, com foco na aplicação prática dos princípios de **Secure by Design** e **Secure by Default** durante o desenvolvimento e a implantação de uma aplicação Web.

O **SecureLab** é uma aplicação Web simples desenvolvida em Python utilizando o framework Flask. O sistema possui autenticação de usuário, gerenciamento de sessão, área restrita e logout seguro.

O projeto foi propositalmente mantido simples para permitir maior foco nas práticas de segurança, versionamento, infraestrutura e implantação contínua.

---

# 📌 Objetivo

O objetivo deste projeto é demonstrar um fluxo de desenvolvimento semelhante ao utilizado em ambientes reais:

```text
Ambiente de Desenvolvimento
          ↓
        GitHub
          ↓
    GitHub Actions
          ↓
 Servidor em Nuvem
          ↓
    Nginx + HTTPS
          ↓
       SecureLab
```

Além da aplicação Web, o projeto contempla:

- Controle de versão com Git;
- Repositório público no GitHub;
- Proteção de credenciais;
- Controles baseados no OWASP Top 10:2025;
- Servidor Linux em nuvem;
- Hardening básico do servidor;
- HTTPS;
- Implantação automatizada utilizando CI/CD.

---

# 🖥️ Funcionalidades da aplicação

Atualmente a aplicação possui:

- Tela de Login;
- Autenticação utilizando usuário e senha;
- Senha armazenada na forma de hash;
- Dashboard protegido;
- Controle de sessão;
- Expiração da sessão após 30 minutos;
- Logout utilizando requisição POST;
- Proteção contra CSRF;
- Credenciais armazenadas fora do código-fonte;
- Cabeçalhos HTTP de segurança;
- Interface Web responsiva simples.

---

# 🛠️ Tecnologias utilizadas

## Aplicação

- Python
- Flask
- Flask-WTF
- Werkzeug
- python-dotenv
- HTML5
- CSS3

## Versionamento

- Git
- GitHub

## Infraestrutura

Planejado para o ambiente de produção:

- Ubuntu Server ou Debian
- Nginx
- Fail2Ban
- SSH
- Certbot
- Let's Encrypt

## CI/CD

Planejado:

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
│   └── dashboard.html
│
└── static/
    └── style.css
```

O arquivo `.env` existe apenas no ambiente local ou de produção e **não é armazenado no repositório GitHub**.

---

# 🔑 Configuração das credenciais

As credenciais da aplicação não ficam diretamente no código-fonte.

São utilizadas variáveis de ambiente:

```text
SECRET_KEY
APP_USERNAME
APP_PASSWORD_HASH
```

Exemplo de estrutura do arquivo `.env`:

```env
SECRET_KEY=sua_chave_secreta
APP_USERNAME=seu_usuario
APP_PASSWORD_HASH=hash_da_senha
```

> O arquivo `.env` não deve ser enviado para o GitHub.

A senha em texto puro também não é armazenada pela aplicação.

---

# 🔒 Segurança da aplicação

O projeto utiliza controles baseados no **OWASP Top 10:2025**.

Foram selecionadas e mitigadas, no mínimo, as seguintes categorias:

1. **A01:2025 - Broken Access Control**
2. **A02:2025 - Security Misconfiguration**
3. **A07:2025 - Authentication Failures**

---

# 🛡️ A01:2025 - Broken Access Control

O controle de acesso impede que usuários não autenticados acessem diretamente áreas protegidas da aplicação.

O dashboard está disponível na rota:

```text
/dashboard
```

Antes de exibir a página, a aplicação verifica se existe uma sessão autenticada.

Exemplo implementado:

```python
if not session.get("authenticated"):
    return redirect(url_for("login"))
```

Portanto, mesmo que um usuário tente acessar diretamente:

```text
http://servidor/dashboard
```

sem ter realizado login, será redirecionado para a tela de autenticação.

## Proteção contra CSRF

Os formulários da aplicação também utilizam tokens CSRF.

Exemplo:

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

A proteção é habilitada no Flask através de:

```python
csrf = CSRFProtect(app)
```

Essa proteção é aplicada tanto ao formulário de login quanto ao processo de logout.

O OWASP Top 10:2025 inclui falhas de controle de acesso e também associa CSRF a essa categoria.

---

# ⚙️ A02:2025 - Security Misconfiguration

Foram aplicadas configurações destinadas a reduzir a exposição causada por configurações inseguras.

## Debug desativado

O servidor Flask é iniciado localmente com:

```python
app.run(debug=False)
```

Isso evita a exposição do debugger do Flask.

---

## Cabeçalhos HTTP de segurança

A aplicação adiciona automaticamente cabeçalhos de segurança às respostas HTTP.

Foram configurados:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy
```

Exemplo da implementação:

```python
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'"
    )
    return response
```

Esses cabeçalhos auxiliam na redução de riscos relacionados a:

- Clickjacking;
- MIME sniffing;
- Carregamento de recursos não autorizados;
- Injeção de conteúdo;
- Vazamento desnecessário de informações de referência.

---

# 👤 A07:2025 - Authentication Failures

A aplicação possui controles destinados à proteção do processo de autenticação.

## Hash da senha

A senha não é armazenada em texto puro.

O hash é criado utilizando os mecanismos disponibilizados pelo Werkzeug.

Na autenticação, a senha informada pelo usuário é comparada ao hash utilizando:

```python
check_password_hash()
```

Exemplo:

```python
check_password_hash(password_hash, password)
```

Dessa forma, a aplicação não precisa armazenar a senha original.

---

# 🍪 Segurança da sessão

A aplicação configura propriedades adicionais para o cookie de sessão:

```python
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
```

## HttpOnly

O atributo:

```text
HttpOnly
```

impede que JavaScript executado no navegador acesse diretamente o cookie de sessão.

## SameSite

O atributo:

```text
SameSite=Lax
```

reduz o envio do cookie em determinados contextos entre sites diferentes, funcionando como uma camada adicional de proteção contra CSRF.

---

# ⏱️ Expiração da sessão

A sessão autenticada possui tempo máximo configurado de:

```text
30 minutos
```

Implementação:

```python
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
```

Após autenticação:

```python
session.permanent = True
```

Isso evita que uma sessão permaneça válida indefinidamente.

---

# 🚪 Logout seguro

O logout não é realizado por uma requisição GET.

A aplicação utiliza:

```python
@app.route("/logout", methods=["POST"])
```

O formulário também contém proteção CSRF:

```html
<form method="POST" action="/logout">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <button type="submit">Logout</button>
</form>
```

Ao realizar logout:

```python
session.clear()
```

remove os dados da sessão autenticada.

---

# 🔐 Proteção de informações sensíveis

O arquivo `.gitignore` impede que informações sensíveis e arquivos locais sejam enviados ao GitHub.

Configuração utilizada:

```gitignore
# Credenciais e segredos
.env

# Ambiente virtual Python
.venv/

# Arquivos temporários do Python
__pycache__/
*.pyc
```

Assim, arquivos contendo:

- Senhas;
- Hashes;
- Chaves;
- Tokens;
- Variáveis de ambiente;

não são versionados no repositório público.

---

# 💻 Execução local

## 1. Clonar o projeto

```powershell
git clone https://github.com/aloisioalmeidaa/securelab.git
```

Entrar na pasta:

```powershell
cd securelab
```

---

## 2. Criar o ambiente virtual

No Windows:

```powershell
py -m venv .venv
```

---

## 3. Ativar o ambiente virtual

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Instalar as dependências

```powershell
pip install -r requirements.txt
```

---

## 5. Configurar as variáveis de ambiente

Criar um arquivo:

```text
.env
```

Adicionar:

```env
SECRET_KEY=sua_chave_secreta
APP_USERNAME=seu_usuario
APP_PASSWORD_HASH=hash_da_senha
```

Para gerar uma chave secreta:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Para gerar o hash de uma senha:

```powershell
python -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('Digite a senha: ')))"
```

---

## 6. Executar a aplicação

```powershell
python app.py
```

A aplicação ficará disponível localmente em:

```text
http://127.0.0.1:5000
```

---

# 🧪 Testes funcionais

Os seguintes testes podem ser realizados manualmente.

## Login correto

Informar credenciais válidas.

Resultado esperado:

```text
Login → Dashboard
```

---

## Login incorreto

Informar usuário ou senha incorretos.

Resultado esperado:

```text
Usuário ou senha inválidos.
```

A aplicação permanece na página de login.

---

## Acesso não autorizado

Sem estar autenticado, acessar diretamente:

```text
/dashboard
```

Resultado esperado:

```text
Redirecionamento para a página de login.
```

---

## Logout

Após login, utilizar o botão:

```text
Logout
```

Resultado esperado:

```text
Sessão encerrada → Login
```

---

# 🔎 Verificação dos cabeçalhos HTTP

Durante o desenvolvimento local, os cabeçalhos podem ser verificados utilizando:

```powershell
curl.exe -I http://127.0.0.1:5000
```

Exemplo de resultado:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: ...
```

O cookie de sessão também apresenta:

```text
HttpOnly
SameSite=Lax
```

---

# ☁️ Infraestrutura de produção

A aplicação será implantada em uma máquina virtual Linux utilizando:

```text
Ubuntu Server ou Debian
```

A arquitetura prevista é:

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
Aplicação Flask
```

O servidor Flask utilizado durante o desenvolvimento não será exposto diretamente à Internet.

---

# 🔥 Firewall e princípio do menor privilégio

Na infraestrutura de produção serão expostas somente as portas necessárias.

Exemplo:

```text
22  → SSH
80  → HTTP
443 → HTTPS
```

A porta SSH será utilizada somente para administração e implantação.

O acesso SSH utilizará autenticação por chave em vez de senha.

---

# 🛡️ Fail2Ban

O servidor será configurado com Fail2Ban para proteção do serviço SSH.

Configuração requerida pelo projeto:

```text
Tolerância: 4 tentativas
Banimento: 24 horas
```

Esse controle será aplicado durante a implantação da infraestrutura.

---

# 🔐 HTTPS

A aplicação em produção utilizará HTTPS.

A configuração prevista utilizará:

```text
Nginx
Certbot
Let's Encrypt
```

O tráfego HTTP será redirecionado automaticamente para HTTPS.

Após a ativação do HTTPS também será habilitada a configuração:

```python
SESSION_COOKIE_SECURE = True
```

Dessa maneira, o cookie de sessão será transmitido apenas utilizando uma conexão HTTPS.

---

# 🔄 CI/CD

O processo de implantação será automatizado utilizando:

```text
GitHub Actions
```

O fluxo esperado será:

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
Servidor em Nuvem
      │
      ▼
Atualização da aplicação
```

A pipeline será executada automaticamente após:

```bash
git push origin main
```

---

# 🔑 GitHub Secrets

As credenciais necessárias para a pipeline não serão armazenadas diretamente no arquivo de workflow.

Serão utilizadas variáveis armazenadas em:

```text
GitHub Secrets
```

Exemplos:

```text
SERVER_HOST
SERVER_USER
SSH_PRIVATE_KEY
```

Dessa forma, informações sensíveis não ficam expostas no repositório.

---

# ✅ Checklist da entrega

## Aplicação

- [x] Aplicação Web funcional
- [x] Tela de Login
- [x] Página interna protegida
- [x] Logout
- [x] Interface HTML/CSS
- [x] Proteção CSRF
- [x] Controle de sessão
- [x] Senha armazenada como hash
- [x] Cabeçalhos HTTP de segurança

## GitHub

- [x] Repositório público
- [x] `.gitignore`
- [x] Credenciais fora do repositório
- [x] Histórico de commits
- [x] README

## OWASP Top 10:2025

- [x] A01 - Broken Access Control
- [x] A02 - Security Misconfiguration
- [x] A07 - Authentication Failures

## Infraestrutura

- [ ] Servidor Linux em nuvem
- [ ] SSH utilizando chave
- [ ] Firewall configurado
- [ ] Fail2Ban configurado
- [ ] Nginx configurado

## HTTPS

- [ ] Certificado TLS
- [ ] Certbot / Let's Encrypt
- [ ] Redirecionamento HTTP → HTTPS
- [ ] `SESSION_COOKIE_SECURE`
- [ ] Teste SSL/TLS exigido pela disciplina

## CI/CD

- [ ] GitHub Actions
- [ ] GitHub Secrets
- [ ] Deploy automático
- [ ] Deploy após push para `main`

---

# 📚 Referências

## OWASP

OWASP Top 10:2025  
https://top10.owasp.org/2025/

OWASP Top 10:2025 - Broken Access Control  
https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/

OWASP Cheat Sheet Series - Session Management  
https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

OWASP Cheat Sheet Series - Cross-Site Request Forgery Prevention  
https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

OWASP Cheat Sheet Series - HTTP Headers  
https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html

## Flask

Flask Documentation  
https://flask.palletsprojects.com/

## Werkzeug

Werkzeug Documentation  
https://werkzeug.palletsprojects.com/

---

# 📖 Status do projeto

O projeto encontra-se em desenvolvimento.

A aplicação Web e os controles iniciais de segurança já estão implementados.

As próximas etapas são:

```text
1. Provisionar servidor Linux em nuvem
2. Configurar SSH
3. Configurar firewall
4. Configurar Fail2Ban
5. Instalar e configurar Nginx
6. Publicar a aplicação
7. Configurar HTTPS
8. Executar os testes SSL/TLS
9. Criar pipeline GitHub Actions
10. Validar o deploy automático
```

---

## Autor

**Aloisio Almeida**

Projeto desenvolvido como atividade acadêmica de pós-graduação.