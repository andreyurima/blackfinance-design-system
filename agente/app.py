"""Agente do Black Finance no Slack (Socket Mode)."""

import logging
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from conversa import montar_mensagens

PASTA = Path(__file__).parent
load_dotenv(PASTA / ".env")

MODELO = os.environ.get("AGENTE_MODELO", "claude-opus-5-5")
ESFORCO = os.environ.get("AGENTE_ESFORCO", "medium")
PROMPT = (PASTA / "prompt.md").read_text(encoding="utf-8")

logging.basicConfig(level=logging.INFO)
app = App(token=os.environ["SLACK_BOT_TOKEN"])
claude = anthropic.Anthropic()
BOT_USER_ID = app.client.auth_test()["user_id"]
nomes = {}


def nome_de(client, user_id):
    if user_id not in nomes:
        try:
            perfil = client.users_info(user=user_id)["user"]["profile"]
            nome = perfil.get("display_name") or perfil.get("real_name") or user_id
        except Exception:
            nome = user_id
        nomes[user_id] = nome.split()[0]
    return nomes[user_id]


def perguntar_ao_claude(mensagens):
    resposta = claude.beta.messages.create(
        model=MODELO,
        max_tokens=16000,
        system=PROMPT,
        messages=mensagens,
        thinking={"type": "adaptive"},
        output_config={"effort": ESFORCO},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if resposta.stop_reason == "refusal":
        return "Não consigo ajudar com esse pedido."
    texto = "".join(b.text for b in resposta.content if b.type == "text").strip()
    return texto or "Não consegui responder agora. Tenta de novo?"


def responder(client, channel, ts, thread_ts, logger):
    client.reactions_add(channel=channel, timestamp=ts, name="eyes")
    try:
        replies = client.conversations_replies(channel=channel, ts=thread_ts, limit=100)["messages"]
        mensagens = montar_mensagens(replies, BOT_USER_ID, lambda u: nome_de(client, u))
        texto = perguntar_ao_claude(mensagens) if mensagens else "Oi! Em que posso ajudar?"
    except anthropic.APIError as erro:
        logger.exception("Erro no Claude: %s", erro)
        texto = "Deu erro do meu lado. Tenta de novo em alguns minutos."
    client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=texto)
    client.reactions_remove(channel=channel, timestamp=ts, name="eyes")


@app.event("app_mention")
def na_mencao(event, client, logger):
    responder(client, event["channel"], event["ts"], event.get("thread_ts") or event["ts"], logger)


@app.event("message")
def na_dm(event, client, logger):
    if event.get("channel_type") != "im" or event.get("subtype") or event.get("bot_id"):
        return
    responder(client, event["channel"], event["ts"], event.get("thread_ts") or event["ts"], logger)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
