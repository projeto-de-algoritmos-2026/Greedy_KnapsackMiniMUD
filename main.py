from item import Item
from knapsack import knapsack_01


CAPACIDADE_TOTAL = 15
PESO_OCUPADO_INICIAL = 6

ITENS_MOCHILA = [
    Item("Mapa Rasgado", 2, 1),
    Item("Tocha Gasta", 1, 1),
    Item("Racao de Viagem", 3, 3),
]

ITENS_BAU_INICIAL = [
    Item("Espada Antiga", 4, 10),
    Item("Pocao Rara", 2, 6),
    Item("Armadura Pesada", 7, 14),
    Item("Anel Mistico", 1, 5),
    Item("Machado Sombrio", 5, 12),
    Item("Elmo de Ferro", 3, 7),
]


def pausar():
    input("\nPressione Enter para continuar...")


def capacidade_restante(mochila):
    return CAPACIDADE_TOTAL - sum(item.peso for item in mochila)


def exibir_introducao():
    print("=" * 64)
    print("KNAPSACK MUD: O Bau do Guardiao da Cripta")
    print("=" * 64)
    print(
        "\nVoce derrotou o Guardiao da Cripta. No silencio da sala final,\n"
        "um bau antigo se abre com armas, reliquias e tesouros. Sua mochila\n"
        "ja esta parcialmente cheia, entao sera preciso escolher com cuidado."
    )
    pausar()


def exibir_menu():
    print("\n" + "=" * 64)
    print("Menu")
    print("=" * 64)
    print("1. Ver mochila")
    print("2. Ver itens do bau")
    print("3. Recolher melhores itens usando Knapsack")
    print("4. Ver explicacao do algoritmo")
    print("5. Ver tabela dinamica gerada pelo algoritmo")
    print("6. Sair")
    return input("\nEscolha uma opcao: ").strip()


def exibir_itens(titulo, itens):
    print(f"\n{titulo}")
    print("-" * len(titulo))

    if not itens:
        print("Nenhum item.")
        return

    for indice, item in enumerate(itens, start=1):
        print(f"{indice}. {item.nome} | peso {item.peso} | valor {item.valor}")


def ver_mochila(mochila):
    peso_ocupado = sum(item.peso for item in mochila)
    restante = CAPACIDADE_TOTAL - peso_ocupado

    exibir_itens("Itens na mochila", mochila)
    print("\nCapacidade total:", CAPACIDADE_TOTAL)
    print("Peso ja ocupado:", peso_ocupado)
    print("Capacidade restante:", restante)
    pausar()


def ver_bau(itens_bau):
    exibir_itens("Itens no bau", itens_bau)
    pausar()


def recolher_melhores_itens(mochila, itens_bau, estado):
    restante = capacidade_restante(mochila)
    itens_candidatos = list(itens_bau)

    print("\nAntes da coleta:")
    print(f"Peso ocupado: {CAPACIDADE_TOTAL - restante}/{CAPACIDADE_TOTAL}")
    print(f"Espaco disponivel para o algoritmo: {restante}")

    escolhidos, valor_total, peso_total, dp = knapsack_01(itens_candidatos, restante)
    nomes_escolhidos = {item.nome for item in escolhidos}
    deixados = [item for item in itens_bau if item.nome not in nomes_escolhidos]

    mochila.extend(escolhidos)
    itens_bau[:] = deixados
    estado["ultima_execucao"] = {
        "capacidade": restante,
        "itens_candidatos": itens_candidatos,
        "itens_escolhidos": escolhidos,
        "valor_total": valor_total,
        "peso_total": peso_total,
        "dp": dp,
    }

    print("\nItens escolhidos pelo Knapsack:")
    exibir_itens("Coletados", escolhidos)
    exibir_itens("Deixados no bau", deixados)
    print(f"\nPeso total usado: {peso_total}/{restante}")
    print(f"Valor total obtido: {valor_total}")
    print(f"Peso da mochila depois: {sum(item.peso for item in mochila)}/{CAPACIDADE_TOTAL}")

    if escolhidos:
        print(
            "\nA escolha foi feita por otimizacao: o algoritmo comparou combinacoes\n"
            "possiveis, em vez de pegar apenas o item de maior valor individual."
        )
    else:
        print("\nNenhum item coube na capacidade restante.")

    pausar()


def explicar_algoritmo():
    print("\nExplicacao do 0/1 Knapsack")
    print("-" * 30)
    print(
        "O problema da mochila pergunta quais itens devem ser levados quando\n"
        "existe um limite de peso. Neste MUD, peso e o espaco que um item ocupa,\n"
        "valor e o beneficio do item, e capacidade e o peso maximo que ainda cabe.\n\n"
        "Nem todos os itens podem ser pegos porque a mochila ja tem objetos e o\n"
        "espaco restante e limitado. Como cada item do bau so pode ser escolhido\n"
        "uma vez, este e o problema 0/1 Knapsack.\n\n"
        "A programacao dinamica monta uma tabela dp[i][c], onde i representa os\n"
        "primeiros itens considerados e c representa uma capacidade possivel.\n"
        "Para cada item, a tabela decide entre nao pegar o item ou pegar o item,\n"
        "caso ele caiba. O maior valor entre essas duas escolhas fica gravado.\n\n"
        "Complexidade: O(n * W), onde n e o numero de itens e W e a capacidade."
    )
    pausar()


def imprimir_tabela_dp(estado, itens_bau):
    execucao = estado.get("ultima_execucao")

    if execucao is None:
        capacidade = CAPACIDADE_TOTAL - PESO_OCUPADO_INICIAL
        escolhidos, valor_total, peso_total, dp = knapsack_01(itens_bau, capacidade)
        execucao = {
            "capacidade": capacidade,
            "itens_candidatos": list(itens_bau),
            "itens_escolhidos": escolhidos,
            "valor_total": valor_total,
            "peso_total": peso_total,
            "dp": dp,
        }
        estado["ultima_execucao"] = execucao

    capacidade = execucao["capacidade"]
    itens = execucao["itens_candidatos"]
    dp = execucao["dp"]

    print("\nTabela dinamica dp[i][c]")
    print(f"Capacidade usada: {capacidade}")
    print("Cada linha considera mais um item do bau.\n")

    cabecalho = "Item".ljust(20) + "".join(str(c).rjust(4) for c in range(capacidade + 1))
    print(cabecalho)
    print("-" * len(cabecalho))

    for i, linha in enumerate(dp):
        nome = "0 itens" if i == 0 else itens[i - 1].nome[:19]
        valores = "".join(str(valor).rjust(4) for valor in linha)
        print(nome.ljust(20) + valores)

    print(f"\nCelula final dp[{len(itens)}][{capacidade}] = {dp[-1][-1]}")
    print("Itens reconstruidos:", ", ".join(item.nome for item in execucao["itens_escolhidos"]) or "nenhum")
    pausar()


def main():
    mochila = list(ITENS_MOCHILA)
    itens_bau = list(ITENS_BAU_INICIAL)
    estado = {"ultima_execucao": None}

    exibir_introducao()

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            ver_mochila(mochila)
        elif opcao == "2":
            ver_bau(itens_bau)
        elif opcao == "3":
            recolher_melhores_itens(mochila, itens_bau, estado)
        elif opcao == "4":
            explicar_algoritmo()
        elif opcao == "5":
            imprimir_tabela_dp(estado, itens_bau)
        elif opcao == "6":
            print("\nVoce deixa a cripta com os itens escolhidos. Fim.")
            break
        else:
            print("\nOpcao invalida.")
            pausar()


if __name__ == "__main__":
    main()
