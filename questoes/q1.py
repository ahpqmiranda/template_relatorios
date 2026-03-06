from core import *
from typing import List
import sympy as sp
import os
import subprocess

# =============================================================================
# DEFINIÇÃO DOS DADOS DA QUESTÃO 1
# =============================================================================
raw_data_lista2_q01 = {
    # Dados do motor
    "d": 0.200,  # Diâmetro (m)
    "c": 0.250,  # Curso (m)
    "Vc": 0.001570,  # Volume morto (m³)
    "N": 500,  # Ciclos por minuto (rpm)

    # Estados Iniciais e Máximos
    "P1": 100000,  # Pressão no início da compressão (Pa) -> 1 bar
    "T1": 300.15,  # Temperatura no início (K) -> 27 °C
    "T3": 1673.15,  # Temperatura máxima do ciclo (K) -> 1400 °C

    # Propriedades do ar como gás ideal (dados no fim da lista)
    "cv": 717,  # J/kg-K
    "cp": 1004,  # J/kg-K
    "k": 1.4,  # Razão de calores específicos
    "R": 288.2  # Constante do gás (Ru/MW = 8314.5 / 28.85) em J/kg-K
}


# =============================================================================
# FUNÇÃO DE RESOLUÇÃO (ETAPAS)
# =============================================================================
def solve_lista2_q01(data: ResolvedData, beta: int) -> List[Step]:
    steps: List[Step] = []

    # --- Símbolos ---
    d, c, Vc, N = sp.symbols('d c Vc N', positive=True, real=True)
    P1, T1, T3 = sp.symbols('P1 T1 T3', positive=True, real=True)
    k, cv, cp, R = sp.symbols('k cv cp R', positive=True, real=True)

    Vd, r = sp.symbols('Vd r', positive=True, real=True)
    T2, P2, P3, T4, P4 = sp.symbols('T2 P2 P3 T4 P4', positive=True, real=True)
    eta_th, w_in, w_out, w_net, q_in = sp.symbols('eta_th w_in w_out w_net q_in', positive=True, real=True)
    pme, Wdot_i = sp.symbols('pme Wdot_i', positive=True, real=True)

    # --- Passo 1: Volume Deslocado e Razão de Compressão ---
    Vd_eq = sp.Eq(Vd, sp.pi * d ** 2 / 4 * c)
    Vd_val = float(Vd_eq.rhs.subs({d: data["d"], c: data["c"]}).evalf())
    add_step(steps, "Volume Deslocado", "Cálculo do volume varrido pelo pistão em 1 cilindro.", Vd_eq, Vd_val)

    r_eq = sp.Eq(r, (Vd + Vc) / Vc)
    r_val = float(r_eq.rhs.subs({Vd: Vd_val, Vc: data["Vc"]}).evalf())
    add_step(steps, "Razão de Compressão", "Relação entre o volume máximo (Vd + Vc) e o volume mínimo (Vc).", r_eq,
             r_val)

    # --- Passo 2: Estado 2 (Fim da Compressão Isentrópica) ---
    T2_eq = sp.Eq(T2, T1 * r ** (k - 1))
    T2_val = float(T2_eq.rhs.subs({T1: data["T1"], r: r_val, k: data["k"]}).evalf())
    add_step(steps, "Temperatura no Estado 2", "Processo isentrópico (1-2): $T_2 = T_1 \cdot r^{k-1}$.", T2_eq, T2_val)

    P2_eq = sp.Eq(P2, P1 * r ** k)
    P2_val = float(P2_eq.rhs.subs({P1: data["P1"], r: r_val, k: data["k"]}).evalf())
    add_step(steps, "Pressão no Estado 2", "Processo isentrópico (1-2): $P_2 = P_1 \cdot r^k$.", P2_eq, P2_val)

    # --- Passo 3: Estado 3 (Fim da Adição de Calor Isocórica) ---
    P3_eq = sp.Eq(P3, P2 * (T3 / T2))
    P3_val = float(P3_eq.rhs.subs({P2: P2_val, T3: data["T3"], T2: T2_val}).evalf())
    add_step(steps, "Pressão no Estado 3", "Processo isocórico (2-3): $\\frac{P_3}{T_3} = \\frac{P_2}{T_2}$.", P3_eq,
             P3_val)

    # --- Passo 4: Estado 4 (Fim da Expansão Isentrópica) ---
    T4_eq = sp.Eq(T4, T3 * (1 / r) ** (k - 1))
    T4_val = float(T4_eq.rhs.subs({T3: data["T3"], r: r_val, k: data["k"]}).evalf())
    add_step(steps, "Temperatura no Estado 4", "Processo isentrópico (3-4): $T_4 = T_3 \cdot (1/r)^{k-1}$.", T4_eq,
             T4_val)

    P4_eq = sp.Eq(P4, P3 * (1 / r) ** k)
    P4_val = float(P4_eq.rhs.subs({P3: P3_val, r: r_val, k: data["k"]}).evalf())
    add_step(steps, "Pressão no Estado 4", "Processo isentrópico (3-4): $P_4 = P_3 \cdot (1/r)^k$.", P4_eq, P4_val)

    # --- Passo 5: Eficiência Térmica do Ciclo ---
    eta_eq = sp.Eq(eta_th, 1 - 1 / (r ** (k - 1)))
    eta_val = float(eta_eq.rhs.subs({r: r_val, k: data["k"]}).evalf())
    add_step(steps, "Eficiência Térmica", "Eficiência do ciclo Otto ideal em função da razão de compressão.", eta_eq,
             eta_val)

    # --- Passo 6: Trabalho Específico (J/kg) ---
    q_in_eq = sp.Eq(q_in, cv * (T3 - T2))
    q_in_val = float(q_in_eq.rhs.subs({cv: data["cv"], T3: data["T3"], T2: T2_val}).evalf())
    add_step(steps, "Calor Adicionado", "Calor fornecido a volume constante: $q_{in} = c_v(T_3 - T_2)$.", q_in_eq,
             q_in_val)

    w_net_eq = sp.Eq(w_net, eta_th * q_in)
    w_net_val = float(w_net_eq.rhs.subs({eta_th: eta_val, q_in: q_in_val}).evalf())
    add_step(steps, "Trabalho Específico Líquido",
             "Trabalho líquido por unidade de massa: $w_{net} = \\eta_{th} \cdot q_{in}$.", w_net_eq, w_net_val)

    # --- Passo 7: Pressão Média Efetiva (Pa) ---
    # Necessário calcular a massa de ar: m = P1*(Vd+Vc)/(R*T1)
    m_ar_val = float((data["P1"] * (Vd_val + data["Vc"]) / (data["R"] * data["T1"])))
    W_ciclo_total_val = w_net_val * m_ar_val  # Trabalho total em Joules

    pme_eq = sp.Eq(pme, w_net * (data["P1"] * (Vd + Vc) / (R * T1)) / Vd)  # Expressão para demonstrar
    pme_val = float(W_ciclo_total_val / Vd_val)
    add_step(steps, "Pressão Média Efetiva (PME)", "Trabalho total do ciclo dividido pelo volume deslocado.", pme_eq,
             pme_val)

    # --- Passo 8: Potência Indicada (W) ---
    # Para motor 2 tempos, ocorre 1 ciclo por rotação
    Wdot_eq = sp.Eq(Wdot_i, pme * Vd * (N / 60))
    Wdot_val = float(Wdot_eq.rhs.subs({pme: pme_val, Vd: Vd_val, N: data["N"]}).evalf())
    add_step(steps, "Potência Indicada",
             "Potência gerada baseada na PME, volume deslocado e frequência (1 ciclo/volta para 2 tempos).", Wdot_eq,
             Wdot_val)

    return steps


# =============================================================================
# ENUNCIADO
# =============================================================================
def format_question_text(data: ResolvedData) -> str:
    return """Um motor a gás monocilíndrico de dois tempos é modelado usando o ciclo Otto, apresenta
diâmetro do cilindro de 200 mm e curso do pistão de 250 mm. O volume morto é de 1570 cm$^3$.
No início do processo de compressão, o fluido de trabalho encontra-se a uma pressão de 1 bar e
temperatura de 27$^\\circ$C. A temperatura máxima atingida ao longo do ciclo é de 1400$^\\circ$C. 

Com base nessas informações, determine:
\\begin{enumerate}[label=\\alph*)]
\\item A pressão e a temperatura nos principais estados termodinâmicos do ciclo;
\\item A eficiência térmica do ciclo;
\\item O trabalho específico produzido por ciclo;
\\item A pressão média efetiva;
\\item A potência indicada fornecida pelo motor, sabendo que ele realiza 500 ciclos por minuto.
\\end{enumerate}"""


# =============================================================================
# EXECUÇÃO
# =============================================================================
if __name__ == "__main__":
    # Roda a função do framework
    data, steps, beta = solve_problem(
        "Questão 1 - Motor Otto 2 Tempos",
        solve_lista2_q01,
        raw_data_lista2_q01,
        beta_value=1
    )

    # Gera o código LaTeX formatado
    section_tex = question_to_latex_section(
        q_number=1,
        problem_title="Ciclo Otto Ideal",
        given=data,
        steps=steps,
        question_text=format_question_text(data)
    )

    # Salva no arquivo
    with open("lista2_q01_section.tex", "w", encoding='utf-8') as f:
        f.write(section_tex)

    print("✅ Questão 1 gerada com sucesso em lista2_q01_section.tex")