from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/npc', methods=['POST'])
def npc_decision():
    data = request.json
    situacao = data.get('situacao', '')

    prompt = f"""Você é o cérebro de um NPC inimigo num jogo Roblox.
Responda APENAS com uma dessas palavras: ATACAR, FUGIR, PATRULHAR

Situação atual: {situacao}

Decisão:"""

    response = model.generate_content(prompt)
    decisao = response.text.strip().upper()

    if decisao not in ["ATACAR", "FUGIR", "PATRULHAR"]:
        decisao = "PATRULHAR"

    return jsonify({"acao": decisao})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
