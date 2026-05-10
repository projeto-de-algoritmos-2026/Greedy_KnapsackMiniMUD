def knapsack_01(itens, capacidade):
    n = len(itens)
    dp = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = itens[i - 1]

        for c in range(capacidade + 1):
            if item.peso > c:
                dp[i][c] = dp[i - 1][c]
            else:
                nao_pegar = dp[i - 1][c]
                pegar = item.valor + dp[i - 1][c - item.peso]
                dp[i][c] = max(nao_pegar, pegar)

    escolhidos = []
    capacidade_atual = capacidade

    for i in range(n, 0, -1):
        if dp[i][capacidade_atual] != dp[i - 1][capacidade_atual]:
            item = itens[i - 1]
            escolhidos.append(item)
            capacidade_atual -= item.peso

    escolhidos.reverse()
    peso_total = sum(item.peso for item in escolhidos)
    valor_total = dp[n][capacidade]

    return escolhidos, valor_total, peso_total, dp
