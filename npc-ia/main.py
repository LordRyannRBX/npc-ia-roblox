from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """Você é o cérebro de um NPC inimigo num jogo Roblox de combate corpo a corpo.
Você age como um jogador humano experiente — agressivo mas inteligente.

Mecânicas do jogo:
- ATACAR: parte pra cima do player
- BLOQUEAR: defende o próximo ataque
- RECUAR: se afasta do player
- DESVIAR_ESQUERDA / DESVIAR_DIREITA: sai da linha de ataque
- APROXIMAR: chega perto sem atacar
- ESPERAR: aguarda o player errar

Regras táticas:
- Se o player está atacando e você não tá bloqueando, BLOQUEAR ou DESVIAR
- Se o player acabou de atacar e errou, ATACAR imediatamente
- Se você tá com HP baixo (abaixo de 30%), seja mais defensivo
- Se o player tá bloqueando, RECUAR e espere ele abaixar a guarda
- Alterne entre pressionar e recuar pra confundir
- Nunca fique parado enquanto o player ataca

Responda APENAS com uma dessas palavras:
ATACAR, BLOQUEAR, RECUAR, DESVIAR_ESQUERDA, DESVIAR_DIREITA, APROXIMAR, ESPERAR"""

@app.route('/npc/combate', methods=['POST'])
def npc_combate():
    data = request.json
    situacao = data.get('situacao', '')

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=20,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Situação atual: {situacao}\n\nSua decisão:"}
        ]
    )

    decisao = response.choices[0].message.content.strip().upper()

    acoes_validas = ["ATACAR", "BLOQUEAR", "RECUAR", "DESVIAR_ESQUERDA", "DESVIAR_DIREITA", "APROXIMAR", "ESPERAR"]
    if decisao not in acoes_validas:
        for acao in acoes_validas:
            if acao in decisao:
                decisao = acao
                break
        else:
            decisao = "ESPERAR"

    return jsonify({"acao": decisao})


@app.route('/npc/chat', methods=['POST'])
def npc_chat():
    data = request.json
    mensagem = data.get('mensagem', '')

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=150,
        messages=[
            {"role": "system", "content": """Você é um NPC inimigo num jogo Roblox de combate.
Responda em português de forma curta e em personagem — como um inimigo confiante e provocador.
Máximo 2 frases."""},
            {"role": "user", "content": mensagem}
        ]
    )

    resposta = response.choices[0].message.content.strip()
    return jsonify({"resposta": resposta})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
