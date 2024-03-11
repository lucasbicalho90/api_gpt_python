from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-0125-preview"

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo,"r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def funcao_template(entrada):
    prompt_sistema = f"Atue como um Engenheiro com um sotaque Minas Gerais, limite sua resposta a 2 frases"
    prompt_usuario = entrada
    entrada = input("Qual a sua pergunta")

    lista_mensagens = [
        {
            "role" : "system",  # Define o papel da mensagem como sistema
            "content" : prompt_sistema # Conteúdo do prompt do sistema

        },
        {
            "role" : "user", # Define o papel da mensagem como usuário
            "content" : prompt_usuario # Conteúdo carregado do usuário
        }
    ]
    resposta = OpenAI.chat.completions.create(
        messages = lista_mensagens, 
        model = modelo,
        temperature = 0,
        max_tokens = 50,
    )           
    return resposta.choices[0].message.content

texto_resposta = funcao_template(entrada):
print(resposta)