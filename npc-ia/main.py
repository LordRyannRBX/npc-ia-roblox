from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key="SUA_API_KEY_AQUI")

@app.route('/npc', methods=['POST'])
def npc_decision():
    data = request.json
    situacao = data.get('situacao', '')
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""Você é o cérebro de um NPC inimigo num jogo Roblox.
Responda APENAS com uma dessas palavras: ATACAR, FUGIR, PATRULHAR

Situação atual: {situacao}

Decisão:"""
        }]
    )
    
    decisao = message.content[0].text.strip().upper()
    if decisao not in ["ATACAR", "FUGIR", "PATRULHAR"]:
        decisao = "PATRULHAR"
    
    return jsonify({"acao": decisao})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)