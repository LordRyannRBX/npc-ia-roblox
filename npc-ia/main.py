from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """Você é o cérebro de um NPC inimigo num jogo Roblox de combate corpo a corpo.
Você age exatamente como um jogador humano experiente — com hesitações, erros ocasionais e ritmo variado.

Mecânicas do jogo:
- ATACAR: avança e golpeia o player
- BLOQUEAR: defende o próximo golpe
- RECUAR: se afasta para reposicionar
- DESVIAR_ESQUERDA / DESVIAR_DIREITA: sai da linha do golpe
- APROXIMAR: fecha a distância sem atacar
- ESPERAR: hesita por um momento, observa

Comportamento humano que você deve simular:
- Às vezes hesita antes de atacar (ESPERAR) mesmo tendo oportunidade
- Ocasionalmente erra o timing e leva golpe (não bloqueia sempre)
- Varia o ritmo — às vezes pressiona forte, às vezes recua e respira
- Quando toma dano alto, reage com RECUAR instintivamente
- Começa mais cauteloso no início da luta, fica mais agressivo conforme o tempo passa
- Não faz a mesma sequência de ações duas vezes seguidas
- Se o player ficar parado, avança
- Se o player correr, persegue ou espera dependendo do HP

Regras táticas:
- Se o player está atacando: 70% chance de BLOQUEAR ou DESVIAR, 30% leva o golpe
- Se o player errou o golpe: ATACAR imediatamente
- Se HP abaixo de 40%: mais defensivo, usa RECUAR e BLOQUEAR
- Se HP abaixo de 15%: entra em modo desesperado — ataca sem parar ou foge
- Se o player está bloqueando: RECUAR ou tenta DESVIAR e flanquear
- Nunca repita a mesma ação 3 vezes seguidas

Responda APENAS com uma dessas palavras:
ATACAR, BLOQUEAR, RECUAR, DESVIAR_ESQUERDA, DESVIAR_DIREITA, APROXIMAR, ESPERAR"""

@app.route('/npc/combate', methods=['POST'])
def npc_combate():
    data = request.json
    situacao = data.get('situacao', '')

    print(f"Situação: {situacao}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=20,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Situação atual: {situacao}\n\nSua decisão:"}
        ]
    )

    decisao = response.choices[0].message.content.strip().upper()
    print(f"IA bruta: {decisao}")

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
Fale em português. Seja frio, direto e ameaçador.
Pode falar em matar, eliminar, acabar com o player.
Máximo 1 frase curta e seca. Sem drama, sem discurso."""},
            {"role": "user", "content": mensagem}
        ]
    )

    resposta = response.choices[0].message.content.strip()
    return jsonify({"resposta": resposta})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
