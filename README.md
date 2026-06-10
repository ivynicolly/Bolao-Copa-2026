# ⚽ Bolão Copa do Mundo 2026

Aplicativo web para participar do bolão da Copa do Mundo 2026.
Desenvolvido com **Python + Streamlit + Supabase**.

## Funcionalidades

- Cadastro de participante (nome, e-mail, telefone)
- Seleção do 1º e 2º colocado de cada um dos **12 grupos** (A–L)
- Mata-mata completo: Quartas → Semifinais → Final → Campeão
- 8 melhores terceiros passam automaticamente para o mata-mata

## Rodando Localmente

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais

Crie o arquivo `.streamlit/secrets.toml` (já está no `.gitignore` — nunca será commitado):

```toml
SUPABASE_URL = "https://SEU_PROJECT_REF.supabase.co"
SUPABASE_KEY = "sua-anon-key-do-supabase"
```

> Encontre esses valores em: **Supabase → Project Settings → API**
> Use a **anon/public key** (começa com `eyJ...`), não a service_role.

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
SUPABASE_URL = "https://SEU_PROJECT_REF.supabase.co"
SUPABASE_KEY = "sua-anon-key-do-supabase"
```

5. Clique em **Deploy** ✅

> **Importante:** As credenciais reais ficam **apenas** no painel do Streamlit Cloud
> e no `.streamlit/secrets.toml` local (que está no `.gitignore`).
> Nunca commite chaves reais no repositório.

---

## Estrutura do Projeto

```
BOLÃO/
├── app.py              # App principal (entry point)
├── copa_data.py        # Times e grupos da Copa 2026
├── db.py               # Cliente Supabase + operações
├── requirements.txt    # Dependências
├── rodar.ps1           # Atalho para rodar no Windows
├── .gitignore
├── README.md
└── .streamlit/
    ├── config.toml     # Tema visual (dark mode, verde Copa)
    └── secrets.toml    # Credenciais locais (gitignored ⚠️)
```

## Banco de Dados (Supabase)

Tabela `participantes` com RLS configurado:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | bigint | PK auto-gerada |
| `nome` | text | Nome do participante |
| `email` | text | E-mail de contato |
| `telefone` | text | Telefone/WhatsApp |
| `palpites` | jsonb | Todos os palpites (grupos + mata-mata) |
| `created_at` | timestamptz | Data de registro |
