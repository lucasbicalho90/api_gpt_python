from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

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

def analisador_sentimentos(produto):
    prompt_sistema = f"""
        Você é um analisador de sentimentos de avaliações de produtos.
        Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
        depois atribua qual o sentimento geral para o produto.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Nome do Produto:
        Resumo das Avaliações:
        Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """
    prompt_usuario = carrega(f"E:/Lucas/ESTUDOS/PROGRAMAÇÃO/OpenAI Playground/GPT e Python criando API - Alura/curso_1_openai/dados/avaliacoes-{produto}.txt") 
    print(f"Iniciou a análise de sentimentos do produto {produto}")

    # Prepara uma lista de mensagens para enviar à API, incluindo o prompt do sistema e do usuário
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

    try: # Tentatica para solicitar completions à API da OpenAI usando as mensagens preparadas e o modelo escolhido
        resposta = cliente.chat.completions.create(
            messages = lista_mensagens, 
            model = modelo
        )

        # Imprime o conteúdo da resposta gerada pelo modelo
        texto_resposta = resposta.choices[0].message.content
        salva(f"E:/Lucas/ESTUDOS/PROGRAMAÇÃO/OpenAI Playground/GPT e Python criando API - Alura/curso_1_openai/dados/analise-{produto}.txt", texto_resposta)
    except openai.AuthenticationError as e:
        print(f"Erro de Autenticação: {e}")
    except openai.APIError as e:
        print(f"Erro de API: {e}")

lista_de_produtos = ["Camisetas de algodão orgânico", "Jeans feitos com materiais reciclados", "Maquiagem mineral"]
for um_produto in lista_de_produtos:
    analisador_sentimentos(um_produto)
print("Análise de sentimentos concluída para os produtos: " + ", ".join(lista_de_produtos))

