# ⚽ Bolão Copa do Mundo 2026

Aplicativo web para participar do bolão da Copa do Mundo 2026.
Desenvolvido com **Python + Streamlit + Supabase**.

## Funcionalidades

- Cadastro de participante (nome, e-mail, telefone)
- Seleção do 1º e 2º colocado de cada um dos **12 grupos** (A–L)
- 8 melhores terceiros sorteados automaticamente
- Dados de contato protegidos por RLS no Supabase (email/telefone nunca acessíveis pela chave pública)

## Rodando Localmente

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais

Crie o arquivo `.streamlit/secrets.toml` (ele já está no `.gitignore`):

```toml
SUPABASE_URL = "https://mqwsumsacxdcrabpvfxa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xd3N1bXNhY3hkY3JhYnB2ZnhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA5NjU4NDIsImV4cCI6MjA5NjU0MTg0Mn0.HZm5Y3LksXHywS3VKb_hgPj0WdtpMh8lJMY3O-g0d3Y"
```

> **Por que a legacy anon JWT key?** A biblioteca `supabase-py` extrai a role `anon`
> diretamente do JWT. A publishable key (`sb_publishable_...`) não é um JWT e não
> carrega essa informação, fazendo as políticas RLS falharem.

### 3. Rodar o app

O `streamlit` pode não estar no PATH no Windows. Use um dos comandos abaixo:

```powershell
# Opção 1 — sempre funciona
& "C:/Python314/python.exe" -m streamlit run app.py

# Opção 2 — atalho incluído no projeto
.\rodar.ps1
```

Acesse em `http://localhost:8501`

---

## Deploy no Streamlit Cloud

1. **Faça push** deste repositório para o GitHub

2. **Acesse** [share.streamlit.io](https://share.streamlit.io) e conecte o repositório

3. Configure o arquivo principal como `app.py`

4. **Adicione os secrets** em **Settings → Secrets**:

```toml
SUPABASE_URL = "https://mqwsumsacxdcrabpvfxa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1xd3N1bXNhY3hkY3JhYnB2ZnhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA5NjU4NDIsImV4cCI6MjA5NjU0MTg0Mn0.HZm5Y3LksXHywS3VKb_hgPj0WdtpMh8lJMY3O-g0d3Y"
```

5. Clique em **Deploy** ✅

> **Importante:** O arquivo `.streamlit/secrets.toml` está no `.gitignore`
> e **nunca deve ser commitado**. As credenciais ficam apenas no painel do Streamlit Cloud.

---

## Estrutura do Projeto

```
BOLÃO/
├── app.py              # App principal (entry point)
├── copa_data.py        # Times e grupos da Copa 2026
├── db.py               # Cliente Supabase + operações
├── requirements.txt    # Dependências
├── .gitignore
├── README.md
└── .streamlit/
    ├── config.toml     # Tema visual (dark mode, verde Copa)
    └── secrets.toml    # Credenciais locais (gitignored)
```

## Banco de Dados (Supabase)

Duas tabelas com RLS configurado:

| Tabela | Dados | Acesso público |
|--------|-------|----------------|
| `participantes` | nome, palpites | ✅ INSERT e SELECT |
| `contatos` | email, telefone | ✅ INSERT · ❌ SELECT |

Email e telefone **nunca são expostos** via API pública.
