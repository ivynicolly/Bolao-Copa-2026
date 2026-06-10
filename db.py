"""
Supabase client e operações de banco de dados.

Arquitetura simplificada: tabela única `participantes`.
- nome, telefone, email, palpites (JSONB) ficam todos numa linha.
- RLS permite INSERT e SELECT para anon/authenticated.
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_client() -> Client:
    """
    Cria e cacheia o cliente Supabase (uma instância por sessão do servidor).
    """
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


def salvar_palpite(nome: str, telefone: str, email: str, palpites: dict) -> dict:
    """
    Salva todos os dados do participante em uma única tabela.
    O campo `palpites` é um JSONB com a estrutura:
    {
        "grupos": { "A": {"primeiro": "...", "segundo": "..."}, ... },
        "quartas": ["sel1", "sel2", ..., "sel8"],
        "semi": ["sel1", ..., "sel4"],
        "final": ["sel1", "sel2"],
        "campeao": "sel1"
    }
    """
    client = get_client()
    result = (
        client.table("participantes")
        .insert({
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "palpites": palpites,
        })
        .execute()
    )
    return result.data[0]


def get_participantes() -> list[dict]:
    """
    Retorna lista de participantes (sem dados sensíveis, só nome e data).
    """
    client = get_client()
    result = (
        client.table("participantes")
        .select("nome, created_at")
        .order("created_at", desc=True)
        .execute()
    )
    return result.data
