"""
Copa do Mundo 2026 — Dados dos grupos e lista completa de seleções.

Grupos A–L com 4 seleções cada (sorteio de dezembro/2025).
TODAS_SELECOES: lista flat para uso nos palpites de mata-mata.
"""

GRUPOS: dict[str, list[str]] = {
    "A": ["🇲🇽 México", "🇿🇦 África do Sul", "🇰🇷 Coreia do Sul", "🇨🇿 Rep. Tcheca"],
    "B": ["🇨🇦 Canadá", "🇧🇦 Bósnia", "🇶🇦 Qatar", "🇨🇭 Suíça"],
    "C": ["🇧🇷 Brasil", "🇲🇦 Marrocos", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia"],
    "D": ["🇺🇸 EUA", "🇵🇾 Paraguai", "🇦🇺 Austrália", "🇹🇷 Turquia"],
    "E": ["🇩🇪 Alemanha", "🇨🇼 Curaçao", "🇨🇮 Costa do Marfim", "🇪🇨 Equador"],
    "F": ["🇳🇱 Holanda", "🇯🇵 Japão", "🇸🇪 Suécia", "🇹🇳 Tunísia"],
    "G": ["🇧🇪 Bélgica", "🇪🇬 Egito", "🇮🇷 Irã", "🇳🇿 Nova Zelândia"],
    "H": ["🇪🇸 Espanha", "🇨🇻 Cabo Verde", "🇸🇦 Arábia Saudita", "🇺🇾 Uruguai"],
    "I": ["🇫🇷 França", "🇸🇳 Senegal", "🇮🇶 Iraque", "🇳🇴 Noruega"],
    "J": ["🇦🇷 Argentina", "🇩🇿 Argélia", "🇦🇹 Áustria", "🇯🇴 Jordânia"],
    "K": ["🇵🇹 Portugal", "🇨🇩 RD Congo", "🇺🇿 Uzbequistão", "🇨🇴 Colômbia"],
    "L": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇭🇷 Croácia", "🇬🇭 Gana", "🇵🇦 Panamá"],
}

# Lista flat com todas as 48 seleções (para os selectboxes do mata-mata)
TODAS_SELECOES: list[str] = sorted(
    [time for times in GRUPOS.values() for time in times],
    key=lambda x: x.split(" ", 1)[1] if " " in x else x,  # ordena pelo nome sem emoji
)
