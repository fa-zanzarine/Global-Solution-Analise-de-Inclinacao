LIMITE_INCLINACAO = 4.0
DISTANCIA_MAXIMA = 200.0


def altitude(x):
    return x**3 / 1_440_000 - x**2 / 3_200 + 0.03 * x + 750


def derivada(x):
    return x**2 / 480_000 - x / 1_600 + 0.03


def segunda_derivada(x):
    return x / 240_000 - 1 / 1_600


def integral_derivada(a, b):
    return altitude(b) - altitude(a)


def encontrar_pontos_criticos():
    a = 1 / 480_000
    b = -1 / 1_600
    c = 0.03
    delta = b**2 - 4 * a * c

    if delta < 0:
        return []

    raiz = delta**0.5
    return sorted([(-b - raiz) / (2 * a), (-b + raiz) / (2 * a)])


def classificar_ponto_critico(x):
    valor = segunda_derivada(x)
    if valor < 0:
        return "máximo local"
    if valor > 0:
        return "mínimo local"
    return "inconclusivo pela segunda derivada"


def integral_subidas(a, b, pontos_criticos):
    divisores = [a] + [p for p in pontos_criticos if a < p < b] + [b]
    divisores.sort()

    subida = 0.0
    for inicio, fim in zip(divisores, divisores[1:]):
        subida += max(0.0, altitude(fim) - altitude(inicio))
    return subida


def limite_numerico(x, h):
    return (altitude(x + h) - altitude(x)) / h


def interpretar_derivada(x):
    taxa = derivada(x)
    if taxa > 0:
        sentido = "a rua está subindo"
    elif taxa < 0:
        sentido = "a rua está descendo"
    else:
        sentido = "a altitude está momentaneamente constante"

    print(
        f"Em x = {x:.0f} m: f'(x) = {taxa:.6f} m/m "
        f"({taxa * 100:.4f}%). Isso significa que {sentido}; "
        f"a altitude varia aproximadamente {taxa:.4f} m "
        "a cada 1 m percorrido horizontalmente."
    )


def verificar_rota():
    posicoes = [0, 100, 180, 300]
    posicoes_paradas = [180]
    escadas = []  # Exemplo: inserir o índice do trecho se houver escada.
    dados_conhecidos = True
    compativel = True

    print("\\n===== VERIFICAÇÃO SIMPLIFICADA DA ROTA =====")

    for indice, (inicio, fim) in enumerate(zip(posicoes, posicoes[1:])):
        distancia = fim - inicio
        inclinacao = (altitude(fim) - altitude(inicio)) / distancia * 100

        print(
            f"Trecho {indice + 1}: {inicio:.0f}–{fim:.0f} m | "
            f"{distancia:.0f} m | inclinação média: {inclinacao:.4f}%"
        )

        if not dados_conhecidos:
            print("  Dados desconhecidos: trecho descartado.")
            compativel = False

        if indice in escadas:
            print("  Trecho com escada: trecho descartado.")
            compativel = False

        if abs(inclinacao) > LIMITE_INCLINACAO:
            print("  Inclinação acima do limite.")
            compativel = False
        else:
            print("  Inclinação média dentro do limite.")

    pontos_descanso = [0] + sorted(posicoes_paradas) + [posicoes[-1]]
    maior_intervalo = 0

    for inicio, fim in zip(pontos_descanso, pontos_descanso[1:]):
        intervalo = fim - inicio
        maior_intervalo = max(maior_intervalo, intervalo)
        if intervalo > DISTANCIA_MAXIMA:
            print(f"Intervalo sem descanso de {intervalo:.0f} m: acima do limite.")
            compativel = False

    print(f"Maior distância entre pausas: {maior_intervalo:.0f} m")
    print(
        "RESULTADO: rota compatível com os critérios simulados."
        if compativel else
        "RESULTADO: rota incompatível com os critérios simulados."
    )
    return compativel


def executar_analise():
    inicio, fim = 0.0, 300.0
    print("=" * 60)
    print("GUIA-ME — ANÁLISE MATEMÁTICA DA ALTITUDE")
    print("=" * 60)
    print("f(x) = x³/1.440.000 - x²/3.200 + 0,03x + 750")
    print(f"Intervalo: {inicio:.0f} a {fim:.0f} m")
    print(f"Limite de inclinação: {LIMITE_INCLINACAO}%")
    print(f"Distância máxima sem descanso: {DISTANCIA_MAXIMA:.0f} m")

    # 1. Derivada em três pontos
    print("===== 1. DERIVADA EM TRÊS PONTOS =====")
    for ponto in [30, 150, 270]:
        interpretar_derivada(ponto)

    # 2. Pontos críticos
    print("===== 2. PONTOS CRÍTICOS =====")
    criticos = encontrar_pontos_criticos()
    for ponto in criticos:
        print(
            f"x = {ponto:.2f} m | altitude = {altitude(ponto):.4f} m | "
            f"classificação: {classificar_ponto_critico(ponto)}"
        )

    # 3. Integral definida
    print("===== 3. INTEGRAL DEFINIDA =====")
    variacao = integral_derivada(inicio, fim)
    print(f"Integral de f'(x) de 0 a 300 = {variacao:.4f} m")
    if variacao > 0:
        texto = "acima"
    elif variacao < 0:
        texto = "abaixo"
    else:
        texto = "na mesma altura que"
    print(f"A altitude final está {abs(variacao):.4f} m {texto} a inicial.")

    subida = integral_subidas(inicio, fim, criticos)
    print(f"Subida acumulada (somente trechos ascendentes) = {subida:.4f} m")

    # 4. Limite
    print("===== 4. LIMITE RELACIONADO À DERIVADA =====")
    ponto = 30.0
    print(f"Valor teórico f'({ponto:.0f}) = {derivada(ponto):.8f} m/m")
    print("Aproximações de [f(x+h) - f(x)] / h:")
    for h in [1, 0.1, 0.01, 0.001]:
        print(f"  h = {h:<6} -> {limite_numerico(ponto, h):.8f} m/m")

    # 5. Decisão e limitação
    print("===== 5. DECISÃO PARA O GUIA-ME =====")
    print(
        "A derivada é o indicador mais diretamente útil para comparar "
        "a inclinação do trecho com o limite do perfil de mobilidade."
    )
    print(
        "Beneficiados: pessoas idosas ou com mobilidade reduzida. "
        "Aplicação: regra do motor de rotas e resumo na tela da rota."
    )
    print(
        "Limitação: função e dados simulados; o modelo não representa "
        "calçadas, obstáculos, piso, travessias, clima ou todas as "
        "condições individuais."
    )

    verificar_rota()

    print("===== RESUMO =====")
    print(f"Altitude inicial: {altitude(inicio):.4f} m")
    print(f"Altitude final: {altitude(fim):.4f} m")
    print(f"Variação líquida: {variacao:.4f} m")
    print(f"Subida acumulada: {subida:.4f} m")


def gerar_grafico():
    
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Instale matplotlib: python -m pip install matplotlib")
        return

    xs = list(range(301))
    ys = [altitude(x) for x in xs]
    criticos = encontrar_pontos_criticos()

    plt.figure(figsize=(9, 5))
    plt.plot(xs, ys, label="Altitude f(x)", linewidth=2)

    for ponto in criticos:
        plt.scatter(ponto, altitude(ponto), s=65)
        plt.annotate(
            f"{classificar_ponto_critico(ponto)}\\n"
            f"({ponto:.0f} m, {altitude(ponto):.2f} m)",
            (ponto, altitude(ponto)),
            xytext=(8, 10),
            textcoords="offset points"
        )

    for ponto in [30, 150, 270]:
        plt.scatter(ponto, altitude(ponto), marker="x", s=55)

    plt.title("Guia-me — Perfil matemático de altitude")
    plt.xlabel("Distância percorrida (m)")
    plt.ylabel("Altitude (m)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafico_altitude_guia_me.png", dpi=180)
    plt.show()
    print("Gráfico salvo: grafico_altitude_guia_me.png")


if __name__ == "__main__":
    executar_analise()
    gerar_grafico()
