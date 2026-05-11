def knapsack_01_acoes(acoes, mana_disponivel, vida_alvo=None):
    n = len(acoes)
    dp = [[0 for _ in range(mana_disponivel + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        acao = acoes[i - 1]

        for mana in range(mana_disponivel + 1):
            if acao.custo_mana > mana:
                dp[i][mana] = dp[i - 1][mana]
            else:
                nao_usar = dp[i - 1][mana]
                usar = acao.dano + dp[i - 1][mana - acao.custo_mana]
                dp[i][mana] = max(nao_usar, usar)

            if vida_alvo is not None:
                dp[i][mana] = min(dp[i][mana], vida_alvo)

    melhor_dano = max(dp[n])
    melhor_mana = next(mana for mana, dano in enumerate(dp[n]) if dano == melhor_dano)
    escolhidas = []
    mana_atual = melhor_mana

    for i in range(n, 0, -1):
        if dp[i][mana_atual] != dp[i - 1][mana_atual]:
            acao = acoes[i - 1]
            escolhidas.append(acao)
            mana_atual -= acao.custo_mana

    escolhidas.reverse()
    mana_total = sum(acao.custo_mana for acao in escolhidas)

    return escolhidas, melhor_dano, mana_total, dp
