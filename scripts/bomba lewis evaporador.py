from turbomachine import TurbomachineAnalyzer

if __name__ == "__main__":

    print("======================================================")
    print("  ANÁLISE CINEMÁTICA E DE ENERGIA - BOMBA LEWIS VL750 ")
    print("======================================================\n")

    # Premissas do Projeto (Carga manométrica de ~10,11 m)
    D = 0.93  # Diâmetro externo do rotor (descarga da bomba) [m]
    d = 0.60  # Diâmetro interno do cubo do rotor (hub) [m]
    Q_base = 2.2222  # Vazão volumétrica de projeto (8.000 m³/h) [m³/s]
    alpha_4 = 90.0  # Ângulo de entrada do fluxo (axial puro, sem componente tangencial) [graus]
    beta_5 = 8.87  # Ângulo construtivo da pá na saída (ajustado para H = 10.11 m) [graus]
    N = 975.0  # Velocidade de rotação nominal [rpm]

    # Criando o analisador com os dados do problema
    analyzer = TurbomachineAnalyzer(
        D=D,
        d=d,
        N=N,
        Q=Q_base,
        alpha_4=alpha_4,
        beta_5=beta_5
    )

    # Exibindo resultados numéricos de forma estruturada no terminal
    print("--- GEOMETRIA GLOBAL ---")
    for k, v in analyzer.get_geometry().items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\n--- SEÇÃO 4 (ENTRADA DO IMPELIDOR) ---")
    for k, v in analyzer.get_section4().items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\n--- SEÇÃO 5 (SAÍDA DO IMPELIDOR) ---")
    for k, v in analyzer.get_section5().items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\n--- TRANSFERÊNCIA DE ENERGIA (TEOREMA DE EULER) ---")
    for k, v in analyzer.get_energy_transfer().items():
        print(f"  {k}: {v:.4f}")

    print("\n======================================================")
    print(" Gerando e salvando os gráficos dos Triângulos de Velocidade...")

    # Plotar e exibir os triângulos de velocidade
    # O método plot_velocity_triangles já salvará a imagem na pasta correta (out/)
    analyzer.plot_velocity_triangles(show=True)