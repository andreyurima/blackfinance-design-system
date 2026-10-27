from conversa import limpar_texto, montar_mensagens

BOT = "UBOT"
NOMES = {"UANDRE": "André", "UGAB": "Gabriel"}


def nome_de(user_id):
    return NOMES.get(user_id, user_id)


def test_tira_mencao_ao_agente_e_nomeia_as_outras():
    texto = limpar_texto("<@UBOT> pergunta pro <@UGAB>", BOT, nome_de)
    assert texto == "pergunta pro @Gabriel"


def test_thread_vira_turnos_alternados():
    replies = [
        {"user": "UANDRE", "text": "<@UBOT> oi"},
        {"user": BOT, "bot_id": "B1", "text": "Oi, André!"},
        {"user": "UGAB", "text": "eu também"},
        {"user": "UANDRE", "text": "<@UBOT> resume"},
    ]
    assert montar_mensagens(replies, BOT, nome_de) == [
        {"role": "user", "content": "André: oi"},
        {"role": "assistant", "content": "Oi, André!"},
        {"role": "user", "content": "Gabriel: eu também\n\nAndré: resume"},
    ]


def test_ignora_entrada_no_canal_e_mencao_vazia():
    replies = [
        {"user": "UGAB", "subtype": "channel_join", "text": "entrou"},
        {"user": "UANDRE", "text": "<@UBOT>"},
    ]
    assert montar_mensagens(replies, BOT, nome_de) == []


def test_nao_comeca_nem_termina_com_o_agente():
    replies = [
        {"user": BOT, "text": "Bom dia!"},
        {"user": "UANDRE", "text": "<@UBOT> e aí"},
        {"user": BOT, "text": "Respondido."},
    ]
    assert montar_mensagens(replies, BOT, nome_de) == [
        {"role": "user", "content": "André: e aí"},
    ]
