# Owl Know

A coruja do Black Finance no Slack. Responde quando alguém a menciona num canal ou manda DM, sempre na thread, usando o Claude. O jeito de responder está em `prompt.md`.

## Ligar

1. Em api.slack.com/apps > Owl > App Manifest, colar o `manifest.yaml` e salvar. Depois, Install App > Reinstall to Workspace.
2. Copiar `.env.example` para `.env` nesta pasta e colar os três tokens.
3. Dar dois cliques em `iniciar.bat` (Windows, precisa do Python 3.10 ou mais novo, de python.org). Na primeira vez ele instala tudo. Enquanto a janela estiver aberta, o Owl responde.

No Mac ou Linux: `python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python app.py`.

## Ajustes

- `OWL_MODEL` no `.env` troca o modelo (padrão `claude-opus-5-5`).
- `OWL_EFFORT` troca o esforço (`low`, `medium`, `high`; padrão `medium`).

## Testes

`pip install pytest && pytest` nesta pasta.
