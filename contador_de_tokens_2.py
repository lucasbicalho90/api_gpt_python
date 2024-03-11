import tiktoken # A importância desse código é para saber precificar a aplicação e definir a monetização

resposta_modelo = input("Defina o modelo: gpt-4 out gpt-3.5-turbo: ")
print(resposta_modelo)
modelo = resposta_modelo
coficador = tiktoken.encoding_for_model(modelo)
lista_tokens = coficador.encode("Você é um categorizador de produtos.")

def calcular_custo(modelo, tokens):
    if modelo == "gpt-4":
        custo_por_1000_tokens = 0.03  # Altere conforme necessário
    elif modelo == "gpt-3.5-turbo":
        custo_por_1000_tokens = 0.0005  # Altere conforme necessário
    else:
        custo_por_1000_tokens = 0  # Modelo não suportado
    return (tokens / 1000) * custo_por_1000_tokens

print("lista de Tokens:", lista_tokens)
print("Quantos Tokens temos: ", len(lista_tokens))
custo = calcular_custo(modelo,len(lista_tokens))
print(f"O Custo para {modelo} é de ${custo}")

