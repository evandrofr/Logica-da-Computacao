from sys import argv

if __name__ == "__main__":
    '''
    Primeiro loop tem o objetivo de separar os números e sinais, colocando-os em uma lista de operações no formato:
    [10, "+", 213, "-" 934]
    Sendo os números inteiros e os sinais strings.
    Isso é feito atraves de verificação individuais dos caracteres. Caso seja um digito é colocado em uma lista
    temporária até que se encontre um caractere não digito. Quando isso ocorre somasse os números da lista temporária
    considerando suas posições (multiplicando por 10**n) e então colocando-os na lista de operações.
    Quando um sinal é encontrado, ele é colocado diretamente na lista de operações.
    '''

    string = argv[1] # Pegar argumentos da chamada do programa
    lista_operacao = []
    temp = []
    for char in string:
        if char.isdigit():
            temp += [char]
        else:
            num = 0
            for idx, alg in enumerate(temp):
                num += int(alg)*10**(len(temp) - idx - 1)
            if temp != []:    
                lista_operacao += [num]
                temp = []
            if char == "+":
                lista_operacao += ["+"]
            if char == "-":
                lista_operacao += ["-"]

    # if final para considerar o último digito do último número.            
    if char.isdigit():
        num = 0
        for idx, alg in enumerate(temp):
            num += int(alg)*10**(len(temp) - idx - 1)
        lista_operacao += [num]
        temp = []
    print("Lista de operações: ", lista_operacao)



    '''
    Verificação feita em cima da lista de operações. Procurasse números seguidos separados apenas por espaço
    ou sinais na mesma situação. Também verificasse se não há sinais em lugares inadequados (começo e final da
    expressão)
    '''


    if type(lista_operacao[0]) == str or type(lista_operacao[-1]) == str:
        print("Error. Sinal em local inadequado.")
        quit()

    for index, item in enumerate(lista_operacao):
        if index < len(lista_operacao) - 1: # Verificação feita para evitar que não se estore o index da lista
            if isinstance(item, int):    
                if isinstance(lista_operacao[index + 1], int):
                    print("Error. Não entendo dois numeros seguidos.")
                    quit()
            if type(item) == str:
                if type(lista_operacao[index + 1]) == str:
                    print("Error. Não entendo dois sinais seguidos.")
                    quit()


    '''
    Loop para efetuar as operações de fato.
    Loop parte do pressuposto que a lista_operacao já está no formato correto, tendo os sinais nas posições impares
    e os números em posições pares.
    '''

    soma = lista_operacao[0]
    i = 1
    while i < len(lista_operacao):
        if lista_operacao[i] == '+':
            soma += lista_operacao[i+1]
        elif lista_operacao[i] == '-':
            soma -= lista_operacao[i+1]
        i += 2

    print("Resultado: ", soma)







