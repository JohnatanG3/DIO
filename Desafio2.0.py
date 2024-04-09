import textwrap

def menu():
    menu = """
    $$$$$$$$$$$$$$$$ MENU $$$$$$$$$$$$$$$$

     [D]\t - DEPOSITAR
     [S]\t - SACAR
     [E]\t - EXTRATO
     [NC]\t - NOVA CONTA
     [LC]\t - LISTAR CONTAS
     [NU]\t - NOVO USUÁRIO
     [Q]\t - SAIR

    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    OPÇÃO =>: """
    return input(textwrap.dedent(menu)).lower()

def depositar(saldo, valor, extrato_str):
    if valor > 0:
        saldo += valor
        extrato_str += f"Depósito:\t R$ {valor:.2f}\n"
        print("\n$$$ DEPÓSITO REALIZADO COM SUCESSO! $$$")    
    else:
        print("### Operação falhou! O valor informado é inválido! ###")
    return saldo, extrato_str

def sacar(*, saldo, valor, extrato_str, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n### Operação falhou! Você não tem saldo suficiente! ###")
    elif excedeu_limite:
        print("\n### Operação falhou! O valor do saque excede o limite! ###")
    elif excedeu_saques:
        print("\n### Operação falhou! Número máximo de saques excedido! ###")
    elif valor > 0:
        saldo -= valor
        extrato_str += f"Saque:\t\t R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n$$$ SAQUE REALIZADO COM SUCESSO! $$$")
    else:
        print("\n### Operação falhou! O valor informado é inválido! ###")

    return saldo, extrato_str

def extrato(saldo, /, *, extrato_str):
    print("\n$$$$$$$$$$$$$$$$ EXTRATO $$$$$$$$$$$$$$$$")
    print("NÃO FORAM REALIZADAS MOVIMENTAÇÕES!" if not extrato_str else extrato_str)
    print(f"\nSaldo:\t\t R$ {saldo:.2f}")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (SOMENTE NÚMEROS): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n### JÁ EXISTE USUÁRIO COM ESSE CPF! ###")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD-MM-AAAA): ")
    endereco = input("Informe o endereço (Logradouro, N° - Bairro - Cidade/Silga Estado: )")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("\n$$$ USUÁRIO CRIADO COM SUCESSO! $$$")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário (SOMENTE NÚMEROS): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n$$$ CONTA CRIADA COM SUCESSO! $$$")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n### USUÁRIO NÃO ENCONTRADO! FLUXO DE CRIAÇÃO DE CONTA ENCERRADO! ###")

def listar_contas(contas):  # Alterada a assinatura da função para aceitar contas como argumento
    for conta in contas:
        linha = f"""\
            Agência:\t {conta['agencia']}
            C/C:\t\t {conta['numero_conta']}
            Titular:\t {conta['usuario']['nome']}
        """
        print("$" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato_str = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input("Informe o Valor do Depósito: "))
            saldo, extrato_str = depositar(saldo, valor, extrato_str)

        elif opcao == 's':
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato_str = sacar(
                saldo = saldo,
                valor = valor,
                extrato_str = extrato_str,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )
        
        elif opcao == 'e':
            extrato(saldo, extrato_str=extrato_str)
        
        elif opcao == 'nu':
            criar_usuario(usuarios)
        
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == 'lc':
            listar_contas(contas)
        
        elif opcao == 'q':
            break

        else:
            print("Operação inválida, por favor selecione a operação desejada!")

main()
