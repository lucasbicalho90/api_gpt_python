from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Cria um objeto cliente da OpenAI usando a chave da API carregada do arquivo .env
# Chama o método de completions.create no cliente para enviar uma série de mensagens e obter uma resposta
resposta = cliente.chat.completions.create(
    messages=[
        {
            'role': "system",  # Define o papel como "system" para a primeira mensagem
            "content": "Listar apenas os nomes dos produtos, sem considerar descrição."  # Conteúdo da mensagem do sistema
        },
        {
            "role": "user",  # Define o papel como "usuário" para a segunda mensagem
            "content": "Liste 3 Produtos sustentáveis"  # Conteúdo da mensagem do usuário
        }
    ],
    model="gpt-4"  # Especifica o modelo da OpenAI a ser utilizado, neste caso, gpt-4
)
print(resposta.choices[0].message.content)