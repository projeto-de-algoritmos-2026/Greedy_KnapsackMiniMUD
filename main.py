import os
import random

from acao import Acao
from knapsack import knapsack_01_acoes


MANA_DISPONIVEL = 18
LARGURA = 78
VIDA_CLOUD = 9
VIDA_MAX_CLOUD = 100
MANA_CLOUD = 18
MANA_MAX_CLOUD = 30
VIDA_SEPHIROTH = 21
VIDA_MAX_SEPHIROTH = 100
MANA_SEPHIROTH = 6
MANA_MAX_SEPHIROTH = 50
QUANTIDADE_GOLPES_VISIVEIS = 5

GOLPES_BASE = [
    ("Ataque com Espada", 4, 5, "Corte básico para abrir a guarda inimiga."),
    ("Braver", 8, 10, "Golpe pesado e direto com grande impacto."),
    ("Blade Beam", 9, 11, "Uma onda de energia lançada pela lâmina."),
    ("Cross Slash", 12, 14, "Sequência de cortes cruzados em alta pressão."),
    ("Climhazzard", 14, 16, "Investida ascendente com dano concentrado."),
    ("Finishing Touch", 16, 18, "Golpe amplo para encerrar a abertura."),
    ("Meteorain", 18, 20, "Sequência intensa de impactos sucessivos."),
    ("Omnislash", 21, 21, "Sequência máxima, poderosa, mas cara em mana."),
    ("Sonic Break", 7, 8, "Corte veloz para encaixar dano com pouca mana."),
    ("Blade Burst", 10, 12, "Explosão curta de energia concentrada na lâmina."),
]


def linha(char="="):
    return char * LARGURA


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def titulo(texto, subtitulo=None):
    print(linha("="))
    print(f"|| {texto.center(LARGURA - 6)} ||")
    print(linha("="))
    if subtitulo:
        print(f">> {subtitulo}")
        print(linha("-"))


def caixa(texto):
    print("+" + "-" * (LARGURA - 2) + "+")
    for trecho in texto.splitlines():
        print("| " + trecho[: LARGURA - 4].ljust(LARGURA - 4) + " |")
    print("+" + "-" * (LARGURA - 2) + "+")


def barra_status(atual, maximo, largura=18):
    preenchido = round((atual / maximo) * largura) if maximo else 0
    preenchido = min(preenchido, largura)
    return "[" + "#" * preenchido + "." * (largura - preenchido) + f"] {atual}/{maximo}"


def pausar():
    input("\n>> Pressione Enter para continuar...")


def criar_catalogo_variado(gerador):
    catalogo = []

    for nome, mana_base, dano_base, descricao in GOLPES_BASE:
        custo_mana = max(4, min(24, mana_base + gerador.randint(-2, 2)))
        dano = max(4, min(26, dano_base + gerador.randint(-2, 4)))
        catalogo.append(Acao(nome, custo_mana, dano, descricao))

    return catalogo


def criar_acoes_da_rodada(seed=None):
    gerador = random.Random(seed)

    for _ in range(300):
        catalogo = criar_catalogo_variado(gerador)
        acoes_visiveis = gerador.sample(catalogo, QUANTIDADE_GOLPES_VISIVEIS)
        escolhidas, dano_total, _ = knapsack_01_acoes(acoes_visiveis, MANA_DISPONIVEL)

        if dano_total >= VIDA_SEPHIROTH and len(escolhidas) > 1:
            return catalogo, acoes_visiveis

    catalogo = [
        Acao("Ataque com Espada", 4, 5, "Corte básico para abrir a guarda inimiga."),
        Acao("Braver", 8, 10, "Golpe pesado e direto com grande impacto."),
        Acao("Blade Beam", 9, 11, "Uma onda de energia lançada pela lâmina."),
        Acao("Cross Slash", 12, 14, "Sequência de cortes cruzados em alta pressão."),
        Acao("Climhazzard", 14, 16, "Investida ascendente com dano concentrado."),
        Acao("Finishing Touch", 16, 18, "Golpe amplo para encerrar a abertura."),
        Acao("Meteorain", 18, 20, "Sequência intensa de impactos sucessivos."),
        Acao("Omnislash", 24, 21, "Sequência máxima, poderosa, mas cara em mana."),
        Acao("Sonic Break", 7, 8, "Corte veloz para encaixar dano com pouca mana."),
        Acao("Blade Burst", 10, 12, "Explosão curta de energia concentrada na lâmina."),
    ]
    return catalogo, [catalogo[1], catalogo[2], catalogo[3], catalogo[8], catalogo[9]]


def exibir_introducao():
    limpar_tela()
    titulo("KNAPSACK COMBAT MUD", "Turno crítico: Cloud vs Sephiroth")
    print(r"                         .       .")
    print(r"            CLOUD       /|\     /|\       SEPHIROTH")
    print(r"              @        /_|_\   /_|_\          |")
    print(r"             /|\         |       |           /|\ ")
    print(r"             / \        / \     / \          / \ ")
    print(r"        ____________________________________________________")
    print(r"       /___________________________________________________/|")
    print(r"      |___________________________________________________| |")
    print(r"      |___________________________________________________|/")
    print()
    caixa(
        "Cloud segura a espada com as duas mãos.\n"
        "Sephiroth avança sem pressa, obrigando cada decisão a ter peso.\n\n"
        "Cloud está com pouca vida, mas ainda possui 18 pontos de mana.\n"
        "Sephiroth tem apenas 21 pontos de vida restantes."
    )
    exibir_barras_de_status()
    pausar()


def exibir_barras_de_status():
    print("\nBarras de status")
    print("+------------+-----------------------------------------------------------+")
    print(f"| Cloud      | Vida {barra_status(VIDA_CLOUD, VIDA_MAX_CLOUD):<49}|")
    print(f"|            | Mana {barra_status(MANA_CLOUD, MANA_MAX_CLOUD):<49}|")
    print("+------------+-----------------------------------------------------------+")
    print(f"| Sephiroth  | Vida {barra_status(VIDA_SEPHIROTH, VIDA_MAX_SEPHIROTH):<49}|")
    print(f"|            | Mana {barra_status(MANA_SEPHIROTH, MANA_MAX_SEPHIROTH):<49}|")
    print("+------------+-----------------------------------------------------------+")


def exibir_acoes(acoes_disponiveis):
    limpar_tela()
    titulo("HABILIDADES OFENSIVAS", "5 golpes sorteados do catálogo desta rodada")
    print("+----+------------------------+------------+-------+")
    print("| #  | Habilidade             | Mana       | Dano  |")
    print("+----+------------------------+------------+-------+")
    for indice, acao in enumerate(acoes_disponiveis, start=1):
        print(f"| {indice:<2} | {acao.nome[:22]:<22} | {acao.custo_mana:^10} | {acao.dano:^5} |")
    print("+----+------------------------+------------+-------+")
    print("\nOs valores variam a cada execução. Cada habilidade só pode ser usada uma vez.")
    pausar()


def exibir_tabela_acoes(titulo_tabela, acoes):
    print(f"\n{titulo_tabela}")
    print("+----+--------------------------+--------+------+")
    print("| #  | Habilidade               | Mana   | Dano |")
    print("+----+--------------------------+--------+------+")
    for indice, acao in enumerate(acoes, start=1):
        print(f"| {indice:<2} | {acao.nome[:24]:<24} | {acao.custo_mana:^6} | {acao.dano:^4} |")
    print("+----+--------------------------+--------+------+")


def exibir_resumo_analise(mana_total, dano_bruto):
    print("\nResumo")
    print("+-------------------+---------+")
    print("| Mana total usada  | " + f"{mana_total} / {MANA_DISPONIVEL}".ljust(7) + " |")
    print("| Dano bruto causado| " + str(dano_bruto).ljust(7) + " |")
    print("+-------------------+---------+")


def exibir_objetivo_analise():
    print("OBJETIVO")
    caixa(
        "Causar o maior dano bruto possível com as habilidades disponíveis,\n"
        "sem ultrapassar a mana atual do Cloud.\n"
        "Se houver empate de dano, a análise prefere a opção que gasta menos mana."
    )


def exibir_barras_analise():
    print("\nRecursos analisados")
    print("+------------------------------+------------------------------+")
    print("| Mana do Cloud                | Vida de Sephiroth            |")
    print("+------------------------------+------------------------------+")
    print(f"| {barra_status(MANA_CLOUD, MANA_MAX_CLOUD):<28} | {barra_status(VIDA_SEPHIROTH, VIDA_MAX_SEPHIROTH):<28} |")
    print("+------------------------------+------------------------------+")


def obter_execucao(estado):
    if estado["execucao"] is None:
        escolhidas, dano_total, mana_total = knapsack_01_acoes(
            estado["acoes_disponiveis"],
            MANA_DISPONIVEL,
        )
        estado["execucao"] = {
            "escolhidas": escolhidas,
            "dano_total": dano_total,
            "dano_bruto": sum(acao.dano for acao in escolhidas),
            "mana_total": mana_total,
        }

    return estado["execucao"]


def executar_analise(estado):
    limpar_tela()
    execucao = obter_execucao(estado)
    escolhidas = execucao["escolhidas"]

    titulo("ANÁLISE COM 0/1 KNAPSACK")
    exibir_objetivo_analise()
    exibir_barras_analise()
    print("\nA análise usa apenas os 5 golpes disponíveis nesta execução.")

    exibir_tabela_acoes("Melhor combinação encontrada", escolhidas)
    exibir_resumo_analise(execucao["mana_total"], execucao["dano_bruto"])

    print("\nConclusão:")
    print(
        "Entre os golpes disponíveis nesta rodada, essa sequência é a que mais\n"
        "causa dano dentro da mana atual do Cloud. Se o dano passar da vida de\n"
        "Sephiroth, o excedente aparece apenas como overkill; a decisão ainda é\n"
        "a melhor ofensiva segundo o critério definido para esta rodada."
    )
    pausar()
    aplicar_resultado_no_combate(execucao)


def aplicar_resultado_no_combate(execucao):
    limpar_tela()
    titulo("RETORNO AO COMBATE")

    vida_sephiroth = VIDA_SEPHIROTH
    mana_cloud = MANA_CLOUD

    print("Status antes da sequência")
    print("+-----------+-------------+------------+")
    print("| Lutador   | Vida        | Mana       |")
    print("+-----------+-------------+------------+")
    print(f"| Cloud     | {f'{VIDA_CLOUD}/{VIDA_MAX_CLOUD}':<11} | {f'{mana_cloud}/{MANA_MAX_CLOUD}':<10} |")
    print(f"| Sephiroth | {f'{vida_sephiroth}/{VIDA_MAX_SEPHIROTH}':<11} | {f'{MANA_SEPHIROTH}/{MANA_MAX_SEPHIROTH}':<10} |")
    print("+-----------+-------------+------------+")
    print("\nSequência aplicada")
    print("+----------------------+--------------------------+------------+---------------+")
    print("| Habilidade           | Efeito                   | Mana Cloud | Sephiroth HP  |")
    print("+----------------------+--------------------------+------------+---------------+")

    for acao in execucao["escolhidas"]:
        mana_cloud = max(0, mana_cloud - acao.custo_mana)
        vida_sephiroth = max(0, vida_sephiroth - acao.dano)
        efeito = f"Causa {acao.dano} de dano."
        print(
            f"| {acao.nome[:20]:<20} | {efeito:<24} | "
            f"{f'{mana_cloud}/{MANA_MAX_CLOUD}':<10} | {f'{vida_sephiroth}/{VIDA_MAX_SEPHIROTH}':<13} |"
        )

    print("+----------------------+--------------------------+------------+---------------+")

    print("Sephiroth tenta avançar, mas a sequência encerra o confronto.")
    print("O dano escolhido pela análise foi suficiente para zerar sua vida.")
    print()
    titulo("VITÓRIA")
    print("Cloud vence este turno decisivo.")
    print("A demonstração mostra o Knapsack otimizando dano sob limite de mana.")
    pausar()


def exibir_menu():
    limpar_tela()
    titulo("MENU DO TURNO")
    print("Cloud precisa encerrar a luta antes que Sephiroth ataque novamente.")
    exibir_barras_de_status()
    print()
    print("[1] Ver habilidades ofensivas")
    print("[2] Executar análise com Knapsack")
    print("[0] Sair")
    return input("\n>> Escolha uma opção: ").strip()


def main():
    catalogo_rodada, acoes_disponiveis = criar_acoes_da_rodada()
    estado = {
        "catalogo_rodada": catalogo_rodada,
        "acoes_disponiveis": acoes_disponiveis,
        "execucao": None,
    }
    exibir_introducao()

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            exibir_acoes(estado["acoes_disponiveis"])
        elif opcao == "2":
            executar_analise(estado)
        elif opcao == "0":
            limpar_tela()
            titulo("FIM")
            print("Cloud respira fundo. A decisão do turno foi compreendida.")
            break
        else:
            limpar_tela()
            print("\nOpção inválida.")
            pausar()


if __name__ == "__main__":
    main()
