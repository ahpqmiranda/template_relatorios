from core import *
from typing import List
import sympy as sp

# =============================================================================
# DEFINIÇÃO DOS DADOS DA QUESTÃO 2
# =============================================================================
raw_data_lista2_q02 = {
    "PCI": 42000,  # Poder calorífico em kJ/kg
    "P_a": 1.2,  # Pressão a 5% do curso (bar)
    "P_b": 4.8,  # Pressão a 75% do curso (bar)
    "y_a": 0.05,  # 5% do curso percorrido
    "y_b": 0.75,  # 75% do curso percorrido
    "n_poly": 1.3,  # Expoente politrópico
    "eta_rel": 0.60,  # Relação eta_i / eta_ciclo (60%)
    "k": 1.4  # Razão de calores específicos (ar-padrão)
}


# =============================================================================
# FUNÇÃO DE RESOLUÇÃO (ETAPAS)
# =============================================================================
def solve_lista2_q02(data: ResolvedData, beta: int) -> List[Step]:
    steps: List[Step] = []

    # --- Símbolos ---
    PCI, P_a, P_b, y_a, y_b = sp.symbols('PCI P_a P_b y_a y_b', positive=True, real=True)
    n_poly, eta_rel, k = sp.symbols('n_poly eta_rel k', positive=True, real=True)
    Rv, r, eta_ciclo, eta_i, isfc = sp.symbols('R_v r eta_ciclo eta_i isfc', positive=True, real=True)

    # --- Passo 1: Razão de volumes intermediários (Rv = Va / Vb) ---
    # Processo politrópico: Pa * Va^n = Pb * Vb^n => Va/Vb = (Pb/Pa)^(1/n)
    Rv_eq = sp.Eq(Rv, (P_b / P_a) ** (1 / n_poly))
    Rv_val = float(((data["P_b"] / data["P_a"]) ** (1 / data["n_poly"])))

    add_step(
        steps,
        "Razão de Volumes Intermediários ($R_v$)",
        "A partir da relação politrópica $P_A V_A^n = P_B V_B^n$, encontramos a razão entre os volumes a 5\\% e 75\\% do curso.",
        Rv_eq, Rv_val
    )

    # --- Passo 2: Razão de Compressão (r) ---
    # Sabemos que V(y) = Vc + (1 - y)*Vd, onde y é a fração do curso a partir do PMI.
    # r = 1 + Vd/Vc => Vd/Vc = r - 1
    # Substituindo: Va/Vb = Rv = [1 + (1 - y_a)*(r - 1)] / [1 + (1 - y_b)*(r - 1)]
    # Isolando r, temos: r = 1 + (Rv - 1) / [(1 - y_a) - Rv*(1 - y_b)]
    c_a = 1 - data["y_a"]  # Fração de Vd restante em A (0.95)
    c_b = 1 - data["y_b"]  # Fração de Vd restante em B (0.25)

    r_eq = sp.Eq(r, 1 + (Rv - 1) / ((1 - y_a) - Rv * (1 - y_b)))
    r_val = float(1 + (Rv_val - 1) / (c_a - Rv_val * c_b))

    add_step(
        steps,
        "Razão de compressão do motor ($r$)",
        "Substituindo os volumes pela relação $V(y) = V_c + (1-y)V_d$ na razão $R_v$ e isolando $r$ (onde $r-1 = V_d/V_c$).",
        r_eq, r_val
    )

    # --- Passo 3: Eficiência do ciclo ar-padrão ---
    # Sendo um motor a gasolina, modela-se como ciclo Otto ideal.
    eta_c_eq = sp.Eq(eta_ciclo, 1 - 1 / (r ** (k - 1)))
    eta_c_val = float(1 - 1 / (r_val ** (data["k"] - 1)))

    add_step(
        steps,
        "Eficiência do ciclo ar-padrão (Otto)",
        "Eficiência ideal calculada via $\\eta_{ciclo} = 1 - r^{1-k}$.",
        eta_c_eq, eta_c_val
    )

    # --- Passo 4: Eficiência indicada real ---
    eta_i_eq = sp.Eq(eta_i, eta_rel * eta_ciclo)
    eta_i_val = float(data["eta_rel"] * eta_c_val)

    add_step(
        steps,
        "Eficiência indicada real ($\\eta_i$)",
        "Multiplicamos a eficiência do ciclo ideal pela relação fornecida (60\\%).",
        eta_i_eq, eta_i_val
    )

    # --- Passo 5: Consumo Específico Indicado de Combustível (g/kWh) ---
    # ISFC = 1 / (PCI * eta_i) -> Dá em kg/kJ se PCI for kJ/kg
    # Para converter para g/kWh: 1 kWh = 3600 kJ (então multiplicamos por 3600 para dar por kWh)
    # E multiplicamos por 1000 para passar de kg para gramas -> Fator de 3.6 * 10^6
    isfc_eq = sp.Eq(isfc, 3600000 / (PCI * eta_i))
    isfc_val = float(3600000 / (data["PCI"] * eta_i_val))

    add_step(
        steps,
        "Consumo Específico Indicado ($CEI$)",
        "O consumo específico é $CEI = \\frac{\\dot{m}_f}{\\dot{W}_i} = \\frac{1}{PCI \\cdot \\eta_i}$. Para apresentar em g/kWh, aplicamos o fator de conversão de $3.6 \\times 10^6$.",
        isfc_eq, isfc_val
    )

    return steps


# =============================================================================
# ENUNCIADO
# =============================================================================
def format_question_text(data: ResolvedData) -> str:
    return """Um motor a gasolina é alimentado com um combustível cujo poder calorífico é de 42.000 kJ/kg. 
As pressões no interior do cilindro, quando o pistão está a 5\\% e a 75\\% do curso de compressão, 
são de 1,2 bar e 4,8 bar, respectivamente. 

Admitindo que o processo de compressão obedece à lei politrópica: $PV^{1,3} = constante$ 
e desprezando os efeitos de biela-manivela considerando $V$ variando linearmente com o curso, determine:
\\begin{enumerate}[label=\\alph*)]
\\item A razão de compressão do motor;
\\item Se a relação da eficiência indicada real do motor com a eficiência do ciclo ar-padrão ($\\eta_i/\\eta_{ciclo}$), 
é de 60\\%, calcule o consumo específico indicado de combustível em g/kWh.
\\end{enumerate}"""


# =============================================================================
# EXECUÇÃO
# =============================================================================
if __name__ == "__main__":
    data, steps, beta = solve_problem(
        "Questão 2 - Processo Politrópico e ISFC",
        solve_lista2_q02,
        raw_data_lista2_q02,
        beta_value=1
    )

    section_tex = question_to_latex_section(
        q_number=2,
        problem_title="Análise Politrópica e Consumo Específico",
        given=data,
        steps=steps,
        question_text=format_question_text(data)
    )

    with open("lista2_q02_section.tex", "w", encoding='utf-8') as f:
        f.write(section_tex)

    print("✅ Questão 2 gerada com sucesso em lista2_q02_section.tex")