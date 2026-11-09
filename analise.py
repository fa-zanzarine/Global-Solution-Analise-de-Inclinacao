# Perfil de mobilidade do idoso
limite_inclinacao = 4.0  # Porcentagem maxima
distancia_maxima = 200   # Metros sem descansar

# Dados simulados dos trechos da rota
trechos = [
    {"distancia": 100, "alt_inicio": 750, "alt_fim": 753,
     "escada": False, "dados": True},

    {"distancia": 80, "alt_inicio": 753, "alt_fim": 756,
     "escada": False, "dados": True},

    {"distancia": 120, "alt_inicio": 756, "alt_fim": 759,
     "escada": False, "dados": True}
]

# Posicoes das paradas de descanso
paradas = [180]

distancia_total = 0
subida_acumulada = 0
rota_compativel = True

print("===== ANALISE DO GUIA-ME =====")

# Analise de cada trecho
for i, trecho in enumerate(trechos):

    distancia = trecho["distancia"]
    variacao_altitude = trecho["alt_fim"] - trecho["alt_inicio"]

    distancia_total += distancia

    print(f"\nTrecho {i + 1}")

    # Verificar se existem dados confiaveis
    if not trecho["dados"]:
        print("Dados desconhecidos. Trecho descartado.")
        rota_compativel = False
        continue

    # Regra: nao permitir escadas
    if trecho["escada"]:
        print("Trecho possui escada.")
        rota_compativel = False

    # Calculo aproximado da derivada (inclinacao)
    inclinacao = (variacao_altitude / distancia) * 100

    print(f"Inclinacao: {inclinacao:.2f}%")

    # Verificar limite de inclinacao
    if abs(inclinacao) > limite_inclinacao:
        print("Inclinacao acima do limite!")
        rota_compativel = False
    else:
        print("Inclinacao compativel.")

    # Integral aproximada: acumular apenas subidas
    subida_acumulada += max(0, variacao_altitude)

# Verificar distancia entre paradas
pontos_descanso = [0] + sorted(paradas) + [distancia_total]

for i in range(len(pontos_descanso) - 1):

    distancia = pontos_descanso[i + 1] - pontos_descanso[i]

    if distancia > distancia_maxima:
        print("\nDistancia entre paradas acima do limite!")
        rota_compativel = False

# Resultado final
print("\n===== RESULTADO FINAL =====")

print(f"Distancia total: {distancia_total} metros")
print(f"Subida acumulada: {subida_acumulada} metros")

if rota_compativel:
    print("Rota compativel com o perfil cadastrado!")
else:
    print("Rota nao compativel com o perfil cadastrado!")