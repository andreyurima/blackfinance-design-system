"""Transforma uma thread do Slack na conversa que vai para o Claude."""

import re

MENCAO = re.compile(r"<@([UW][A-Z0-9]+)>")


def limpar_texto(texto, bot_user_id, nome_de):
    """Tira a menção ao agente e troca as outras menções pelo nome da pessoa."""
    texto = texto.replace(f"<@{bot_user_id}>", "")
    texto = MENCAO.sub(lambda m: "@" + nome_de(m.group(1)), texto)
    return texto.strip()


def montar_mensagens(replies, bot_user_id, nome_de):
    """Converte as mensagens da thread em turnos user/assistant alternados.

    O que o agente escreveu vira assistant; o resto vira user, com o nome de quem
    escreveu na frente. Turnos seguidos do mesmo papel são juntados.
    """
    turnos = []
    for msg in replies:
        if msg.get("subtype") not in (None, "bot_message", "thread_broadcast"):
            continue
        if msg.get("user") == bot_user_id:
            papel = "assistant"
            texto = (msg.get("text") or "").strip()
        else:
            papel = "user"
            texto = limpar_texto(msg.get("text") or "", bot_user_id, nome_de)
            if not texto:
                continue
            autor = nome_de(msg["user"]) if msg.get("user") else msg.get("username", "bot")
            texto = f"{autor}: {texto}"
        if not texto:
            continue
        if turnos and turnos[-1]["role"] == papel:
            turnos[-1]["content"] += "\n\n" + texto
        else:
            turnos.append({"role": papel, "content": texto})

    while turnos and turnos[0]["role"] == "assistant":
        turnos.pop(0)
    while turnos and turnos[-1]["role"] == "assistant":
        turnos.pop()
    return turnos
