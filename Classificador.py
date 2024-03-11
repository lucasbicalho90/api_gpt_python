# Importa as bibliotecas necessárias para interagir com a API da OpenAI e gerenciar variáveis de ambiente
from openai import OpenAI
from dotenv import load_dotenv
import os
# Importação biblioteca de codificação de tokens
import tiktoken

# Carrega as variáveis de ambiente do arquivo .env para que possam ser usadas no código
load_dotenv()

# Cria um cliente da OpenAI usando a chave de API armazenada nas variáveis de ambiente
cliente = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
# Define o modelo da GPT a ser usado
modelo = "gpt-4"

# Cria um codificador específico para quantificar o número de tokens para cada modelo
codificador = tiktoken.encoding_for_model(modelo)

# Define uma função para carregar os dados de um arquivo
def carrega(caminho_do_arquivo):
    try:
        # Tenta abrir o arquivo especificado em modo de leitura
        with open(caminho_do_arquivo, "r") as arquivo:
            dados = arquivo.read()  # Lê o conteúdo do arquivo
            return dados  # Retorna o conteúdo lido
    except IOError as e:
        # Caso ocorra um erro de entrada/saída (como arquivo não encontrado), imprime o erro
        print(f"Erro: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

# Define o prompt do sistema que será usado para instruir o modelo sobre o que fazer
prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

# Carrega o conteúdo do usuário a partir de um arquivo CSV
prompt_usuario = carrega("curso_1_openai\dados\lista_de_compras_100_clientes.csv")

# Codifica o prompt combinado (sistema + usuário) em tokens, usando o codificador específico do modelo
lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
# Calcula o número de tokens resultante da codificação
numero_de_tokens = len(lista_de_tokens)
# Define o número de tokens que esperamos produzir como saída
tamanho_esperado_saida = 2048

# Se o número total de tokens (entrada + saída esperada) exceder o limite do modelo, muda para um modelo diferente
if numero_de_tokens >= 4096 - tamanho_esperado_saida:
    modelo = "gpt-4-0125-preview"

# Imprime o modelo escolhido após a verificação do limite de tokens
print(f"Modelo escolhido: {modelo}")

# Prepara uma lista de mensagens para enviar à API, incluindo o prompt do sistema e do usuário
lista_mensagens = [
    {
        "role" : "system",  # Define o papel da mensagem como sistema
        "content" : prompt_sistema  # Conteúdo do prompt do sistema
    },
    {
        "role": "user",  # Define o papel da mensagem como usuário
        "content" : prompt_usuario  # Conteúdo carregado do usuário
    }
]

# Solicita completions à API da OpenAI usando as mensagens preparadas e o modelo escolhido
resposta = cliente.chat.completions.create(
    messages=lista_mensagens, 
    model=modelo
)

#Salva um arquivo com as respostas geradas.
texto_resposta = resposta.choices[0].message.content
salva(f"E:/Lucas/ESTUDOS/PROGRAMAÇÃO/OpenAI Playground/GPT e Python criando API - Alura/curso_1_openai/dados/Classificador_Cliente_2.txt", texto_resposta)

# Imprime o conteúdo da resposta gerada pelo modelo
print(texto_resposta)