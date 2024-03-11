import openai
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a chave de API globalmente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Modelo a ser utilizado (ajuste conforme necessário)
modelo = "text-davinci-003"

def carrega(nome_do_arquivo):
    # Função para carregar dados de um arquivo
    ...

def salva(nome_do_arquivo, conteudo):
    # Função para salvar dados em um arquivo
    ...

def funcao_template(entrada):
    prompt_sistema = "Atue como um Engenheiro com um sotaque Minas Gerais, limite sua resposta a 2 frases"
    prompt_usuario = entrada

    lista_mensagens = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": prompt_usuario}
    ]
    
    # Chamada correta à API para obter uma resposta de chat
    resposta = openai.ChatCompletion.create(
        model=modelo,
        messages=lista_mensagens,
        temperature=0,
        max_tokens=50,
    )
    return resposta.choices[0].message["content"]

# Solicita a entrada do usuário
entrada = input("Qual a sua pergunta? ")
# Obtém a resposta usando a função definida
resposta = funcao_template(entrada)
# Imprime a resposta
print(resposta)
