from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

def analisar_transacao(lista_de_transacoes):
    print("1. Executando a análise de transação")

    prompt_sistema = """Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um das outras transações.
    
        Adote o formato de resposta abaixo para compor sua resposta.
        
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """


    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        
        },
        {

            "role":"user",
            "content":f"Considere o CSV abaixo, onde cada linha é uma trasação diferente: {lista_de_transacoes}. Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)"
        }
    ]

    #Comunicação com a openAI
    resposta = client.chat.completions.create(
        messages = lista_mensagens,
        model = modelo,
        temperature=0
    )


    #Utilizar a resposta acima para interpretar os elementos que foram gerados no formato .json pelo chat GPT
    conteudo = resposta.choices[0].message.content.replace("'",'"') #replace converte as aspas simples geradas pelo chat GPT na resposta e converte para aspas duplas (padrão utilizado em arquivos .json)
    print("\Conteúdo:", conteudo) #Print para entender a resposta gerada
    json_resultado = json.loads(conteudo) #converter o conteúdo para formato de json
    print("\nJSON:", json_resultado)
    return json_resultado

nome_do_arquivo = "E:/Lucas/ESTUDOS/PROGRAMAÇÃO/OpenAI Playground/GPT e Python criando API - Alura/curso_1_openai/dados/transacoes.csv"
lista_de_transacoes = carrega(nome_do_arquivo)
transacoes_analisadas = analisar_transacao(lista_de_transacoes)

def gerar_parecer(transacao):
    print("2. Gerando um parecer para cada transação",transacao["id"])

    prompt_sistema = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude".
    Indique no parecer uma justidicatica para quevocê identifique uma farude.
    Transação : {transacao}

    ## Formato Saída 
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horário": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localização": "cidade - estado (País)",
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """

    lista_mensagens = [
        {
            "role": "user",
            "content": prompt_sistema
        }
    ]

    #Comunicação com a openAI
    resposta = client.chat.completions.create(
        messages = lista_mensagens,
        model = modelo,
        temperature=0.5
    )

    conteudo = resposta.choices[0].message.content
    print("Finalizou a geração de parecer")
    return conteudo
    
def gerar_recomendacao(parecer):
    print("3. Gerando recomendações")

    prompt_sistema = f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da transação {parecer}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificalçao Manual".
    Elas devem ser escritas no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável.
    """

    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        }
    ]

    resposta = client.chat.completions.create(
        messages = lista_mensagens,
        model = modelo,
    )

    conteudo = resposta.choices[0].message.content
    print("Fim da geração de recomendação")
    return conteudo

#Percorrer as transacoes analisadas e gerar uma nota somente para as que tiveram um status de fralde

for uma_transacao in transacoes_analisadas["transacoes"]:
    if uma_transacao["status"]  == "Possível Fraude":
        um_parecer = gerar_parecer(uma_transacao)
        print(um_parecer)
        recomendacao = gerar_recomendacao(um_parecer)
        id_trasacao = uma_transacao["id"]
        produto_transacao = uma_transacao["nome_produto"]
        status_transacao = uma_transacao["status"]
        salva(f"transacao-{id_trasacao}-{produto_transacao}-{status_transacao}.txt",recomendacao)