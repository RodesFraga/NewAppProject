

import re
from flask import Flask, render_template, request, jsonify
import requests
import json
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = Flask(__name__)

# API_KEY = "" Não POSSO USAR A API NO GITHUB
API_URL = "https://api.openai.com/v1/chat/completions"
MODEL_ID = "gpt-3.5-turbo"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Carrega o modelo BERT para classificação
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Função para classificar se a pergunta é relacionada à Bíblia
# def is_bible_related_question(question):
#     inputs = tokenizer(question, return_tensors="pt")
#     outputs = model(**inputs)
#     logits = outputs.logits
#     predicted_label = torch.argmax(logits, dim=1).item()
#     return predicted_label == 1  

def is_bible_related_question(question):
    bible_keywords = ["jesus", "deus", "cristo", "evangelho", "fé", "religião", "espiritualidade", "oração", "bíblia", "pregação", "oratoria", "faça uma pregação", "crie uma pregação", "crie uma ilustração", "crie uma história", "o que a bíblia diz", "O que a teologia diz", "como preparar uma pregação", "liste", "tradição dos judeus", "povo jesus", "grego coine", "grego", "hebraico", "no original", "vocabulario", "dicionario biblico", "dicionario"]

    # Converte a pergunta para minúsculas para fazer uma comparação sem diferenciação de maiúsculas e minúsculas
    question_lower = question.lower()

    for keyword in bible_keywords:
        if keyword in question_lower:
            return True

    return False



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_question = request.form['question']

        if is_bible_related_question(user_question):
            body = {
                "model": MODEL_ID,
                "messages": [{"role": "user", "content": user_question}]
            }

            body_json = json.dumps(body)
            response = requests.post(API_URL, headers=headers, data=body_json)

            if response.status_code == 200:
                response_data = response.json()
                answer = response_data["choices"][0]["message"]["content"]
            else:
                print("Erro na requisição para OpenAI:")
                print(f"Código de status: {response.status_code}")
                print(f"Resposta: {response.text}")
                answer = "Desculpe, houve um erro ao processar sua pergunta."
        else:
            answer = "Desculpe, só posso responder perguntas relacionadas à Bíblia."

        return render_template('index.html', question=user_question, answer=answer)

    return render_template('index.html', question='', answer='')

if __name__ == '__main__':
    app.run(debug=True)
