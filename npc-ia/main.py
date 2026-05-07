from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/npc', methods=['POST'])
def npc_decision():
    data = request.json
    situacao = data.get('situacao', '')

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": f"""Você é o cérebro de um NPC inimigo num jogo Roblox.
Responda APENAS com uma dessas palavras: ATACAR, FUGIR, PATRULHAR

Situação atual: {situacao}

Decisão:"""
        }]
    )

    decisao = response.choices[0].message.content.strip().upper()

    if decisao not in ["ATACAR", "FUGIR", "PATRULHAR"]:
        decisao = "PATRULHAR"

    return jsonify({"acao": decisao})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
