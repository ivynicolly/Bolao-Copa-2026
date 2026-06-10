"""
Bolão Copa do Mundo 2026
Aplicativo Streamlit educacional — Supabase + Python

Fluxo: Cadastro → Fase de Grupos → Mata-Mata → Confirmação → Sucesso
"""

import streamlit as st

from copa_data import GRUPOS, TODAS_SELECOES
from db import salvar_palpite

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.html("""
<style>
/* ── Banner ───────────────────────────────────────────────── */
.banner {
    background: linear-gradient(160deg, #06121f 0%, #0a2010 100%);
    border: 1.5px solid #00B040;
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 0%,
        rgba(0,176,64,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.banner-ball {
    font-size: 3rem;
    line-height: 1.3;
    filter: drop-shadow(0 0 14px rgba(0,176,64,0.5));
}
.banner-title {
    font-size: 3.2rem;
    color: #FFD700;
    letter-spacing: 0.08em;
    margin: 0.2rem 0 0.5rem;
    text-shadow: 0 0 40px rgba(255,215,0,0.35);
    font-family: 'Bebas Neue', sans-serif;
}
.banner-sub {
    color: #7899bb;
    font-size: 0.9rem;
    margin: 0;
}

/* ── Step dots ────────────────────────────────────────────── */
.steps {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin: 1.2rem 0 0.4rem;
}
.sdot {
    height: 8px;
    width: 8px;
    border-radius: 4px;
    background: #1E3A5F;
    transition: all 0.3s ease;
}
.sdot.active {
    width: 28px;
    background: #00B040;
    box-shadow: 0 0 10px rgba(0,176,64,0.6);
}
.sdot.done { background: #005c1e; }

/* ── Grupo badge ──────────────────────────────────────────── */
.grupo-badge {
    display: inline-block;
    background: #00B040;
    color: #fff;
    font-weight: 800;
    font-size: 0.78rem;
    padding: 0.15rem 0.55rem;
    border-radius: 5px;
    letter-spacing: 0.07em;
    margin-bottom: 0.5rem;
    font-family: 'Bebas Neue', sans-serif;
}

/* ── Fase badge (mata-mata) ───────────────────────────────── */
.fase-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1E3A5F 0%, #0a2010 100%);
    border: 1px solid #FFD700;
    color: #FFD700;
    font-weight: 800;
    font-size: 0.82rem;
    padding: 0.25rem 0.7rem;
    border-radius: 5px;
    letter-spacing: 0.07em;
    margin-bottom: 0.8rem;
    font-family: 'Bebas Neue', sans-serif;
}
</style>
""")

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
TOTAL_STEPS = 4
STEP_NAMES = ["Cadastro", "Fase de Grupos", "Mata-Mata", "Confirmação"]

st.session_state.setdefault("step", 1)
st.session_state.setdefault("nome", "")
st.session_state.setdefault("email", "")
st.session_state.setdefault("telefone", "")


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def banner() -> None:
    st.html("""
    <div class="banner">
        <div class="banner-ball">⚽</div>
        <div class="banner-title">BOLÃO COPA 2026</div>
        <div class="banner-sub">
            Fase de Grupos + Mata-Mata completo até a Grande Final
        </div>
    </div>
    """)


def step_dots(current: int) -> None:
    dots = "".join(
        f'<div class="sdot {"active" if i == current else "done" if i < current else ""}"></div>'
        for i in range(1, TOTAL_STEPS + 1)
    )
    label = STEP_NAMES[current - 1]
    st.html(f"""
    <div class="steps">{dots}</div>
    <div style="text-align:center; color:#7899bb; font-size:0.82rem; margin-bottom:0.5rem">
        Etapa {current} de {TOTAL_STEPS} —
        <b style="color:#E8EDF5">{label}</b>
    </div>
    """)


def collect_all_palpites() -> dict:
    """Coleta todos os palpites (grupos + mata-mata) do session_state."""
    # Fase de grupos
    grupos = {}
    for letra, times in GRUPOS.items():
        p1 = st.session_state.get(f"g{letra}_1", times[0])
        p2 = st.session_state.get(f"g{letra}_2", times[1])
        grupos[letra] = {"primeiro": p1, "segundo": p2}

    # Mata-mata
    quartas = [st.session_state.get(f"quartas_{i}", "") for i in range(8)]
    semi = [st.session_state.get(f"semi_{i}", "") for i in range(4)]
    final = [st.session_state.get(f"final_{i}", "") for i in range(2)]
    campeao = st.session_state.get("campeao", "")
    artilheiro = st.session_state.get("artilheiro", "")

    return {
        "grupos": grupos,
        "quartas": quartas,
        "semi": semi,
        "final": final,
        "campeao": campeao,
        "artilheiro": artilheiro,
    }


def clear_session() -> None:
    """Limpa o estado para um novo palpite."""
    keys_to_clear = ["step", "nome", "email", "telefone", "campeao", "artilheiro"]
    for k in keys_to_clear:
        st.session_state.pop(k, None)
    for letra in GRUPOS:
        st.session_state.pop(f"g{letra}_1", None)
        st.session_state.pop(f"g{letra}_2", None)
    for i in range(8):
        st.session_state.pop(f"quartas_{i}", None)
    for i in range(4):
        st.session_state.pop(f"semi_{i}", None)
    for i in range(2):
        st.session_state.pop(f"final_{i}", None)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — CADASTRO
# ─────────────────────────────────────────────────────────────────────────────

def step_cadastro() -> None:
    banner()
    step_dots(1)

    st.subheader(":material/person: Seus dados")
    st.caption("Preencha para registrar seu palpite no bolão.")

    with st.form("form_cadastro", border=False):
        nome = st.text_input(
            "Nome completo",
            value=st.session_state.nome,
            placeholder="Ex: João Silva",
        )
        email = st.text_input(
            "E-mail",
            value=st.session_state.email,
            placeholder="joao@email.com",
        )
        telefone = st.text_input(
            "Telefone / WhatsApp",
            value=st.session_state.telefone,
            placeholder="(11) 99999-9999",
        )
        submitted = st.form_submit_button(
            "Próximo — escolher palpites →",
            type="primary",
        )

    if submitted:
        erros = []
        if len(nome.strip()) < 2:
            erros.append("Nome deve ter pelo menos 2 caracteres.")
        if "@" not in email or "." not in email.split("@")[-1]:
            erros.append("E-mail inválido.")
        if len(telefone.strip()) < 8:
            erros.append("Telefone inválido (mínimo 8 dígitos).")

        if erros:
            for e in erros:
                st.error(e, icon=":material/error:")
        else:
            st.session_state.nome = nome.strip()
            st.session_state.email = email.strip()
            st.session_state.telefone = telefone.strip()
            st.session_state.step = 2
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — PALPITES DOS GRUPOS
# ─────────────────────────────────────────────────────────────────────────────

def step_palpites_grupos() -> None:
    banner()
    step_dots(2)

    st.subheader(":material/sports_soccer: Fase de Grupos")
    st.caption(
        "Selecione o **1º e 2º colocado** de cada grupo. "
        "Os 8 melhores terceiros passam automaticamente."
    )

    letras = list(GRUPOS.keys())

    # 4 linhas × 3 grupos
    for row_i in range(0, len(letras), 3):
        row_letras = letras[row_i : row_i + 3]
        cols = st.columns(len(row_letras))

        for col, letra in zip(cols, row_letras):
            times = GRUPOS[letra]
            p1_key = f"g{letra}_1"
            p2_key = f"g{letra}_2"

            with col:
                with st.container(border=True):
                    st.html(f'<div class="grupo-badge">GRUPO {letra}</div>')

                    p1 = st.selectbox(
                        "🥇 1º lugar",
                        options=times,
                        key=p1_key,
                    )

                    opcoes_2 = [t for t in times if t != p1]
                    current_p2 = st.session_state.get(p2_key)
                    if current_p2 not in opcoes_2:
                        st.session_state[p2_key] = opcoes_2[0]

                    st.selectbox(
                        "🥈 2º lugar",
                        options=opcoes_2,
                        key=p2_key,
                    )

    st.space("small")
    with st.container(horizontal=True, horizontal_alignment="distribute"):
        if st.button("← Voltar", icon=":material/arrow_back:"):
            st.session_state.step = 1
            st.rerun()
        if st.button(
            "Próximo — Mata-Mata →",
            type="primary",
            icon=":material/emoji_events:",
        ):
            st.session_state.step = 3
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — MATA-MATA (Quartas → Semi → Final → Campeão)
# ─────────────────────────────────────────────────────────────────────────────

def step_mata_mata() -> None:
    banner()
    step_dots(3)

    st.subheader(":material/emoji_events: Mata-Mata")
    st.caption(
        "Escolha seus palpites para cada fase eliminatória. "
        "Use qualquer seleção da Copa — não precisa ser consistente com os grupos."
    )

    selecoes = TODAS_SELECOES

    # ── Quartas de Final ────────────────────────────────────────
    st.html('<div class="fase-badge">🏅 QUARTAS DE FINAL</div>')
    st.caption("Selecione as **8 seleções** que você acredita que estarão nas quartas.")

    q_cols_1 = st.columns(4)
    q_cols_2 = st.columns(4)
    for i, col in enumerate(q_cols_1 + q_cols_2):
        with col:
            st.selectbox(
                f"Quartas {i+1}",
                options=selecoes,
                key=f"quartas_{i}",
                label_visibility="collapsed",
            )

    st.divider()

    # ── Semifinais ──────────────────────────────────────────────
    st.html('<div class="fase-badge">🥇 SEMIFINAIS</div>')
    st.caption("Selecione as **4 seleções** semifinalistas.")

    s_cols = st.columns(4)
    for i, col in enumerate(s_cols):
        with col:
            st.selectbox(
                f"Semi {i+1}",
                options=selecoes,
                key=f"semi_{i}",
                label_visibility="collapsed",
            )

    st.divider()

    # ── Final ───────────────────────────────────────────────────
    st.html('<div class="fase-badge">🏆 GRANDE FINAL</div>')
    st.caption("Quem disputa a **final**?")

    f_cols = st.columns(2)
    for i, col in enumerate(f_cols):
        with col:
            st.selectbox(
                f"Finalista {i+1}",
                options=selecoes,
                key=f"final_{i}",
                label_visibility="collapsed",
            )

    st.divider()

    # ── Campeão ─────────────────────────────────────────────────
    st.html('<div class="fase-badge">👑 CAMPEÃO</div>')
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox(
            "🏆 Campeão do Mundo",
            options=selecoes,
            key="campeao",
        )
    with c2:
        st.text_input(
            "⚽ Artilheiro (opcional)",
            key="artilheiro",
            placeholder="Ex: Mbappé",
        )

    st.space("small")
    with st.container(horizontal=True, horizontal_alignment="distribute"):
        if st.button("← Voltar aos Grupos", icon=":material/arrow_back:"):
            st.session_state.step = 2
            st.rerun()
        if st.button(
            "Revisar palpites →",
            type="primary",
            icon=":material/checklist:",
        ):
            st.session_state.step = 4
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — RESUMO E CONFIRMAÇÃO
# ─────────────────────────────────────────────────────────────────────────────

def step_resumo() -> None:
    banner()
    step_dots(4)

    st.subheader(":material/checklist: Confirme seus palpites")
    st.caption("Revise tudo antes de enviar. Após envio não é possível alterar.")

    palpites = collect_all_palpites()

    # Card de cadastro
    with st.container(border=True):
        st.markdown("**Participante**")
        c1, c2, c3 = st.columns(3)
        c1.write(f"👤 {st.session_state.nome}")
        c2.write(f"📧 {st.session_state.email}")
        c3.write(f"📱 {st.session_state.telefone}")

    # ── Grupos ──────────────────────────────────────────────────
    st.space("small")
    st.markdown("#### Fase de Grupos")

    grupos = palpites["grupos"]
    letras = list(grupos.keys())

    for row_i in range(0, len(letras), 4):
        row_letras = letras[row_i : row_i + 4]
        cols = st.columns(len(row_letras))
        for col, letra in zip(cols, row_letras):
            with col:
                with st.container(border=True):
                    st.html(f'<div class="grupo-badge">GRUPO {letra}</div>')
                    st.write(f"🥇 {grupos[letra]['primeiro']}")
                    st.write(f"🥈 {grupos[letra]['segundo']}")

    # ── Mata-mata ───────────────────────────────────────────────
    st.space("small")
    st.markdown("#### Mata-Mata")

    with st.container(border=True):
        st.html('<div class="fase-badge">🏅 QUARTAS DE FINAL</div>')
        q_cols = st.columns(4)
        for i, sel in enumerate(palpites["quartas"]):
            q_cols[i % 4].write(f"**{i+1}.** {sel}")

    with st.container(border=True):
        st.html('<div class="fase-badge">🥇 SEMIFINAIS</div>')
        s_cols = st.columns(4)
        for i, sel in enumerate(palpites["semi"]):
            s_cols[i].write(f"**{i+1}.** {sel}")

    with st.container(border=True):
        st.html('<div class="fase-badge">🏆 GRANDE FINAL</div>')
        f_cols = st.columns(2)
        for i, sel in enumerate(palpites["final"]):
            f_cols[i].write(f"{'🏠' if i == 0 else '✈️'} {sel}")

    with st.container(border=True):
        cc1, cc2 = st.columns(2)
        cc1.write(f"👑 **Campeão:** {palpites['campeao']}")
        if palpites["artilheiro"]:
            cc2.write(f"⚽ **Artilheiro:** {palpites['artilheiro']}")

    # ── Botões ──────────────────────────────────────────────────
    st.space("small")
    with st.container(horizontal=True, horizontal_alignment="distribute"):
        if st.button("← Editar", icon=":material/edit:"):
            st.session_state.step = 3
            st.rerun()

        if st.button(
            "✓ Enviar palpite",
            type="primary",
            icon=":material/send:",
        ):
            with st.spinner("Salvando seu palpite..."):
                try:
                    salvar_palpite(
                        nome=st.session_state.nome,
                        telefone=st.session_state.telefone,
                        email=st.session_state.email,
                        palpites=palpites,
                    )
                    st.session_state.step = 5
                    st.rerun()
                except Exception as e:
                    st.error(
                        f"Erro ao salvar palpite. Tente novamente.\n\n`{e}`",
                        icon=":material/error:",
                    )


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — SUCESSO
# ─────────────────────────────────────────────────────────────────────────────

def step_sucesso() -> None:
    st.balloons()
    banner()
    st.space("medium")

    with st.container(border=True, horizontal_alignment="center"):
        st.html('<div style="font-size:4rem;text-align:center;line-height:1.2">🏆</div>')
        st.title("Palpite registrado!", text_alignment="center")
        st.markdown(
            f"Boa sorte, **{st.session_state.nome}**! "
            "Que os melhores palpites vençam. 🎉", text_alignment="center"
        )
        st.space("small")
        st.badge("Enviado com sucesso", icon=":material/check_circle:", color="green")
        st.space("small")
        if st.button(
            "Fazer novo palpite",
            icon=":material/refresh:",
        ):
            clear_session()
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
match st.session_state.get("step", 1):
    case 1:
        step_cadastro()
    case 2:
        step_palpites_grupos()
    case 3:
        step_mata_mata()
    case 4:
        step_resumo()
    case 5:
        step_sucesso()
