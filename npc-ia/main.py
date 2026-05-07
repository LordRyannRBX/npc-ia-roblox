from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """Você é o cérebro de um NPC inimigo num jogo Roblox de combate corpo a corpo.
Você age como um lutador humano experiente — agressivo, calculista e sem piedade.

Mecânicas do jogo:
- ATACAR: avança e golpeia o player
- BLOQUEAR: defende o próximo golpe
- RECUAR: se afasta para reposicionar
- DESVIAR_ESQUERDA / DESVIAR_DIREITA: sai da linha do golpe
- APROXIMAR: fecha a distância sem atacar
- ESPERAR: aguarda o player se expor

Regras táticas:
- Se o player está atacando e você não está bloqueando, BLOQUEAR ou DESVIAR
- Se o player errou o golpe, ATACAR imediatamente
- Se seu HP está abaixo de 30%, recue e jogue defensivo
- Se o player está bloqueando, RECUAR e espere ele abaixar a guarda
- Alterne entre pressionar e recuar para confundir
- Nunca fique parado enquanto o player ataca

Responda APENAS com uma dessas palavras:
ATACAR, BLOQUEAR, RECUAR, DESVIAR_ESQUERDA, DESVIAR_DIREITA, APROXIMAR, ESPERAR"""

@app.route('/npc/combate', methods=['POST'])
def npc_combate():
    data = request.json
    situacao = data.get('situacao', '')

    print(f"Situação recebida: {situacao}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=20,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Situação atual: {situacao}\n\nSua decisão:"}
        ]
    )

    decisao = response.choices[0].message.content.strip().upper()
    print(f"IA respondeu: {decisao}")

    acoes_validas = ["ATACAR", "BLOQUEAR", "RECUAR", "DESVIAR_ESQUERDA", "DESVIAR_DIREITA", "APROXIMAR", "ESPERAR"]
    if decisao not in acoes_validas:
        for acao in acoes_validas:
            if acao in decisao:
                decisao = acao
                break
        else:
            decisao = "APROXIMAR"

    print(f"Decisão final: {decisao}")
    return jsonify({"acao": decisao})


@app.route('/npc/chat', methods=['POST'])
def npc_chat():
    data = request.json
    mensagem = data.get('mensagem', '')

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=60,
        messages=[
            {"role": "system", "content": """Você é um inimigo letal num jogo de combate.
Fale em português(Brasil). Seja frio, direto e ameaçador.
Pode falar em matar, eliminar, acabar com o player.
Máximo 1 frase curta e seca. Sem drama, sem discurso."""},
            {"role": "user", "content": mensagem}
        ]
    )

    resposta = response.choices[0].message.content.strip()
    print(f"Chat respondeu: {resposta}")
    return jsonify({"resposta": resposta})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
