import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class TurbomachineAnalyzer:
    """
    Representa um analisador de geometria e desempenho de turbomáquinas.

    Esta classe fornece métodos para calcular e recuperar propriedades geométricas,
    componentes de velocidade e características de escoamento para seções específicas de uma
    turbomáquina. É destinada à análise da dinâmica de fluidos e aos parâmetros de projeto
    de bombas, turbinas e máquinas similares.

    Atributos
    ---------
    D : float
        Diâmetro externo da turbomáquina.
    d : float
        Diâmetro interno da turbomáquina.
    N : float
        Velocidade de rotação em rotações por minuto (RPM).
    Q : float
        Vazão volumétrica através da turbomáquina.
    alpha_4 : float
        Ângulo de incidência do escoamento (velocidade absoluta) na seção 4, em graus.
    beta_5 : float
        Ângulo de saída do escoamento (velocidade relativa) na seção 5, em graus.

    Métodos
    -------
    __init__(D, d, N, Q, alpha_4, beta_5)
        Inicializa o analisador com os parâmetros geométricos e operacionais fornecidos.

    get_geometry()
        Recupera e retorna as propriedades geométricas e operacionais como um dicionário.

    get_section4()
        Recupera os dados da seção 4 como um dicionário.

    get_section5()
        Recupera os dados da seção 5 como um dicionário.

    get_energy_transfer()
        Calcula a transferência de energia (Teorema de Euler).

    plot_velocity_triangles(show=True)
        Gera e plota os triângulos de velocidades da sucção e do recalque.
    """

    def __init__(self, D, d, N, Q, alpha_4, beta_5):
        self.D = float(D)
        self.d = float(d)
        self.N = float(N)
        self.Q = float(Q)
        self.alpha_4 = float(alpha_4)
        self.beta_5 = float(beta_5)

        self._compute_geometry()
        self._compute_section4()
        self._compute_section5()

    def _compute_geometry(self):
        """
        Calcula diversas propriedades geométricas e de desempenho.

        Este método calcula atributos geométricos como raio, raio médio, diâmetro
        e outros usando as dimensões de entrada e parâmetros operacionais do objeto.
        É essencial para determinar as características derivadas do sistema.

        Atributos calculados
        --------------------
        R : float
            Raio externo calculado como metade do diâmetro externo (D).
        r : float
            Raio interno calculado como metade do diâmetro interno (d).
        rm : float
            Raio médio calculado como a média geométrica entre R e r.
        dm : float
            Diâmetro médio calculado como o dobro do raio médio.
        U : float
            Velocidade periférica (tangencial) calculada usando o diâmetro médio
            e a velocidade de rotação (N).
        A : float
            Área da seção transversal determinada pelos diâmetros externo e interno.
        Cm : float
            Velocidade meridiana média calculada como a razão entre a vazão
            volumétrica (Q) e a área da seção transversal (A).
        """
        self.R = self.D / 2.0
        self.r = self.d / 2.0
        self.rm = (self.R + self.r) / 2.0
        self.dm = 2.0 * self.rm
        self.U = np.pi * self.dm * self.N / 60.0
        self.A = (np.pi / 4.0) * (self.D ** 2 - self.d ** 2)
        self.Cm = self.Q / self.A

    def _compute_section4(self):
        """
        Realiza os cálculos para os triângulos de velocidades e propriedades da seção de entrada (Estação 4).

        Este método inclui cálculos relevantes para o escoamento, como as componentes
        tangencial e meridiana da velocidade, velocidade absoluta, velocidade relativa e seus
        respectivos ângulos.

        Atributos calculados
        --------------------
        Cm4 : float
            Componente meridiana da velocidade na seção 4.
        Cu4 : float
            Componente tangencial da velocidade absoluta na seção 4. Calculada com base em `alpha_4`.
        C4 : float
            Magnitude (módulo) da velocidade absoluta na seção 4.
        Wu4 : float
            Componente tangencial da velocidade relativa à pá na seção 4.
        Wm4 : float
            Componente meridiana da velocidade relativa à pá na seção 4.
        W4 : float
            Magnitude (módulo) da velocidade relativa na seção 4.
        beta_4_calc : float
            Ângulo da velocidade relativa `W4` em relação à direção meridiana, em graus.
        """
        self.Cm4 = self.Cm

        # Se alpha for 90, entra reto (Cu = 0). Senão, calcula a componente tangencial.
        if np.isclose(self.alpha_4, 90.0):
            self.Cu4 = 0.0
        else:
            self.Cu4 = self.Cm4 / np.tan(np.radians(self.alpha_4))

        self.C4 = np.sqrt(self.Cm4 ** 2 + self.Cu4 ** 2)

        # Geometria do triângulo (W fecha C com U)
        self.Wu4 = self.U - self.Cu4
        self.Wm4 = self.Cm4
        self.W4 = np.sqrt(self.Wu4 ** 2 + self.Wm4 ** 2)

        self.beta_4_calc = np.degrees(np.arctan2(self.Wm4, self.Wu4))

    def _compute_section5(self):
        """
        Calcula as características do escoamento na seção de saída (Estação 5) do impelidor.

        Este método calcula diversos parâmetros do escoamento, como a velocidade meridiana,
        velocidade absoluta e velocidade relativa na seção 5, que são essenciais para entender
        a dinâmica de transferência de energia da bomba.

        Atributos calculados
        --------------------
        Cm5 : float
            Velocidade meridiana na seção 5 (m/s).
        Wm5 : float
            Componente meridiana da velocidade relativa na seção 5 (m/s).
        Wu5 : float
            Componente tangencial da velocidade relativa na seção 5 (m/s).
        Cu5 : float
            Componente tangencial da velocidade absoluta na seção 5 (m/s).
        C5 : float
            Velocidade absoluta (resultante) na seção 5 (m/s).
        W5 : float
            Velocidade relativa (resultante) na seção 5 (m/s).
        alpha_5_calc : float
            Ângulo calculado da velocidade absoluta na seção 5, medido em graus.
        """
        self.Cm5 = self.Cm

        # Conhecendo a pá na saída (beta_5), descobrimos as velocidades relativas
        self.Wm5 = self.Cm5
        self.Wu5 = self.Wm5 / np.tan(np.radians(self.beta_5))

        # A bomba dá o "empurrão" na água (transferência de momento):
        self.Cu5 = self.U - self.Wu5
        self.C5 = np.sqrt(self.Cm5 ** 2 + self.Cu5 ** 2)

        self.W5 = np.sqrt(self.Wu5 ** 2 + self.Wm5 ** 2)
        self.alpha_5_calc = np.degrees(np.arctan2(self.Cm5, self.Cu5))

    def get_geometry(self):
        """
        Recupera e retorna os parâmetros geométricos e operacionais.

        Retornos
        --------
        dict
            Um dicionário contendo os seguintes pares chave-valor:
            - D: Diâmetro externo do sistema.
            - d: Diâmetro interno do sistema.
            - R: Raio externo do sistema.
            - r: Raio interno do sistema.
            - rm: Raio médio do sistema.
            - dm: Diâmetro médio do sistema.
            - N_rpm: Velocidade de rotação em RPM.
            - omega_rad_s: Velocidade angular em radianos por segundo (2 * pi * N / 60).
            - U: Velocidade tangencial periférica.
            - A: Área da seção transversal do escoamento.
            - Q: Vazão volumétrica de projeto.
            - Cm_global: Velocidade meridiana global do escoamento.
        """
        return {
            "D": self.D,
            "d": self.d,
            "R": self.R,
            "r": self.r,
            "rm": self.rm,
            "dm": self.dm,
            "N_rpm": self.N,
            "omega_rad_s": 2 * np.pi * self.N / 60.0,
            "U": self.U,
            "A": self.A,
            "Q": self.Q,
            "Cm_global": self.Cm,
        }

    def get_section4(self):
        """
        Recupera os dados cinemáticos da seção de entrada (Estação 4).

        Retornos
        --------
        dict
            Um dicionário contendo os seguintes parâmetros:
            - "alpha_4_deg": Valor do ângulo absoluto na entrada (graus).
            - "beta_4_calc_deg": Valor calculado do ângulo relativo na entrada (graus).
            - "Cm4": Velocidade meridiana na entrada.
            - "Cu4": Componente tangencial da velocidade absoluta na entrada.
            - "C4_mag": Magnitude do vetor de velocidade absoluta na entrada.
            - "Wu4": Componente tangencial da velocidade relativa na entrada.
            - "Wm4": Componente meridiana da velocidade relativa na entrada.
            - "W4_mag": Magnitude do vetor de velocidade relativa na entrada.
        """
        return {
            "alpha_4_deg": self.alpha_4,
            "beta_4_calc_deg": self.beta_4_calc,
            "Cm4": self.Cm4,
            "Cu4": self.Cu4,
            "C4_mag": self.C4,
            "Wu4": self.Wu4,
            "Wm4": self.Wm4,
            "W4_mag": self.W4,
        }

    def get_section5(self):
        """
        Recupera os dados cinemáticos da seção de saída (Estação 5).

        Retornos
        --------
        dict
            Um dicionário contendo os seguintes parâmetros:
            - "alpha_5_calc_deg": Ângulo absoluto calculado na saída (graus).
            - "beta_5_input_deg": Ângulo relativo (da pá) inserido na saída (graus).
            - "Cm5": Velocidade meridiana na saída.
            - "Cu5": Componente tangencial da velocidade absoluta na saída.
            - "C5_mag": Magnitude do vetor de velocidade absoluta na saída.
            - "Wu5": Componente tangencial da velocidade relativa na saída.
            - "Wm5": Componente meridiana da velocidade relativa na saída.
            - "W5_mag": Magnitude do vetor de velocidade relativa na saída.
        """
        return {
            "alpha_5_calc_deg": self.alpha_5_calc,
            "beta_5_input_deg": self.beta_5,
            "Cm5": self.Cm5,
            "Cu5": self.Cu5,
            "C5_mag": self.C5,
            "Wu5": self.Wu5,
            "Wm5": self.Wm5,
            "W5_mag": self.W5,
        }

    def get_energy_transfer(self):
        """
        Calcula a transferência de energia baseada no Teorema de Euler para turbomáquinas.

        Retornos
        --------
        dict
            Um dicionário contendo:
            - "delta_E_specific_J_per_kg": Variação da energia específica do fluido (Trabalho Específico)
              em Joules por quilograma.
            - "delta_head_equivalent_m": Variação da energia convertida em altura manométrica
              (Carga equivalente) em metros.
        """
        delta_E = self.U * (self.Cu5 - self.Cu4)
        return {
            "delta_E_specific_J_per_kg": delta_E,
            "delta_head_equivalent_m": delta_E / 9.81
        }

    def plot_velocity_triangles(self, show=True):
        """
        Gera e plota os triângulos de velocidades para as condições de sucção e recalque do sistema.

        Este método cria um gráfico com dois painéis: um para a condição de entrada (Estação 4) e outro
        para a condição de saída (Estação 5). Cada triângulo inclui vetores representando os diferentes
        componentes de velocidade (tangencial, meridiana, absoluta e relativa), anotados com suas
        respectivas magnitudes e ângulos fundamentais.

        Parâmetros
        ----------
        show : bool, opcional
            Se True, exibe o gráfico na tela e o salva no diretório especificado. Padrão é True.
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # --- Triângulo de ENTRADA (4) ---
        ax = axes[0]
        ax.set_title('Triângulo de Velocidade - ENTRADA (Estação 4)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Componente Tangencial [m/s]', fontsize=10)
        ax.set_ylabel('Componente Meridiana [m/s]', fontsize=10)
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        ax.plot(0, 0, 'ko', markersize=5)

        ax.arrow(0, 0, self.U, 0, head_width=0.2, head_length=0.3, fc='red', ec='red', width=0.05)
        ax.text(self.U / 2, 0.5, f'U = {self.U:.2f} m/s', color='red', ha='center', va='bottom')

        ax.arrow(0, 0, self.Cu4, -self.Cm4, head_width=0.2, head_length=0.3, fc='blue', ec='blue', width=0.05)
        ax.text(self.Cu4 / 2 - 1, -self.Cm4 / 2, f'C4 = {self.C4:.2f} m/s', color='blue', ha='right', va='center')

        ax.arrow(self.U, 0, self.Cu4 - self.U, -self.Cm4, head_width=0.2, head_length=0.3, fc='green', ec='green',
                 width=0.05)
        ax.text(self.U - self.Wu4 / 2 + 1, -self.Wm4 / 2, f'W4 = {self.W4:.2f} m/s\nβ4 = {self.beta_4_calc:.1f}°',
                color='green', ha='left', va='center')

        ax.set_xlim(-5, self.U + 5)
        ax.set_ylim(-self.Cm4 - 2, 2)

        # --- Triângulo de SAÍDA (5) ---
        ax = axes[1]
        ax.set_title('Triângulo de Velocidade - SAÍDA (Estação 5)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Componente Tangencial [m/s]', fontsize=10)
        ax.set_ylabel('Componente Meridiana [m/s]', fontsize=10)
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        ax.plot(0, 0, 'ko', markersize=5)

        ax.arrow(0, 0, self.U, 0, head_width=0.2, head_length=0.3, fc='red', ec='red', width=0.05)
        ax.text(self.U / 2, 0.5, f'U = {self.U:.2f} m/s', color='red', ha='center', va='bottom')

        ax.arrow(0, 0, self.Cu5, -self.Cm5, head_width=0.2, head_length=0.3, fc='blue', ec='blue', width=0.05)
        ax.text(self.Cu5 / 2 - 1, -self.Cm5 / 2, f'C5 = {self.C5:.2f} m/s\nα5 = {self.alpha_5_calc:.1f}°', color='blue',
                ha='right', va='center')

        ax.arrow(self.U, 0, self.Cu5 - self.U, -self.Cm5, head_width=0.2, head_length=0.3, fc='green', ec='green',
                 width=0.05)
        ax.text(self.U - self.Wu5 / 2 + 1, -self.Wm5 / 2, f'W5 = {self.W5:.2f} m/s\nβ5 = {self.beta_5:.1f}°',
                color='green', ha='left', va='center')

        ax.set_xlim(-5, self.U + 5)
        ax.set_ylim(-self.Cm5 - 2, 2)

        plt.tight_layout()
        if show:
            plt.savefig('../out/triangulos_performance.png', dpi=300)
            plt.show()