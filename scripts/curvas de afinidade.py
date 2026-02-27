from turbomachine import TurbomachineAnalyzer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# GERAÇÃO DAS CURVAS DE DESEMPENHO (LEIS DE AFINIDADE)
# ==========================================

# 1. Instanciar o analisador com os dados de projeto da Lewis VL750
analyzer = TurbomachineAnalyzer(
    D=0.93,
    d=0.60,
    N=975.0,
    Q=2.2222,
    alpha_4=90.0,
    beta_5=8.87
)

# 2. Obter os valores de referência dinamicamente do objeto
rho = 1020.0  # Densidade da salmoura a 80°C em kg/m³

dados_geo = analyzer.get_geometry()
dados_energia = analyzer.get_energy_transfer()

N_ref = dados_geo["N_rpm"]
Q_ref = dados_geo["Q"]
H_ref = dados_energia["delta_head_equivalent_m"]

# Potência Hidráulica = rho * Q * Trabalho_Especifico (convertido para kW)
E_especifica = dados_energia["delta_E_specific_J_per_kg"]
P_ref = (rho * Q_ref * E_especifica) / 1000.0

print(f"Valores de Referência Obtidos do Analisador:")
print(f"N: {N_ref} RPM | Q: {Q_ref:.4f} m³/s | H: {H_ref:.2f} m | P: {P_ref:.1f} kW\n")

# 3. Aplicação das Leis de Afinidade
rpm_range = np.linspace(600, 975, 8)
vazoes = []
heads = []
powers = []

for N_atual in rpm_range:
    Q_novo = Q_ref * (N_atual / N_ref)
    H_novo = H_ref * (N_atual / N_ref) ** 2
    P_novo = P_ref * (N_atual / N_ref) ** 3

    vazoes.append(Q_novo)
    heads.append(H_novo)
    powers.append(P_novo)

# 4. Plotando o Gráfico Profissional (Dois Eixos Y em Dark Mode)
plt.style.use('dark_background')  # Ativa o tema escuro
fig, ax1 = plt.subplots(figsize=(10, 5))

# Eixo Y esquerdo (Altura Manométrica)
color1 = '#5dade2'  # Azul claro otimizado para fundo escuro
ax1.set_xlabel('Rotação [RPM]', fontweight='bold')
ax1.set_ylabel('Altura Manométrica [m]', color=color1, fontweight='bold')
line1 = ax1.plot(rpm_range, heads, label='Altura Manométrica [m]', marker='o', color=color1, linewidth=2)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle='--', alpha=0.3)

# Eixo Y direito (Potência Hidráulica)
ax2 = ax1.twinx()
color2 = '#e74c3c'  # Vermelho otimizado para fundo escuro
ax2.set_ylabel('Potência Hidráulica [kW]', color=color2, fontweight='bold')
line2 = ax2.plot(rpm_range, powers, label='Potência Hidráulica [kW]', marker='s', color=color2, linewidth=2)
ax2.tick_params(axis='y', labelcolor=color2)

# Unindo as legendas num lugar visível
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', framealpha=0.1)

plt.title('Curvas de Desempenho vs Rotação (Leis de Afinidade - Lewis VL750)', fontsize=13, pad=15)
fig.tight_layout()

# Salvando a imagem na pasta 'out' para seguir a estrutura do seu projeto
plt.savefig('../out/curva_de_desempenho_vs_rotacao.png', dpi=300)
plt.show()

# Imprimindo a tabela de dados no terminal para registro
df_afinidade = pd.DataFrame({
    "RPM": np.round(rpm_range, 1),
    "Vazão [m³/s]": np.round(vazoes, 2),
    "Altura Manométrica [m]": np.round(heads, 2),
    "Potência Hidr. [kW]": np.round(powers, 1)
})
print("Tabela de Leis de Afinidade:")
print(df_afinidade.to_string(index=False))
