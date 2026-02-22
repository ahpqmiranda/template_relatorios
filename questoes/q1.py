from core import *
from typing import List
import sympy as sp
import subprocess
import os

# Caminho absoluto para o diretório raiz do projeto (dois níveis acima de q2.py)
home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Caminho para o arquivo tcc.tex
entrada = os.path.join(home, 'tcc.tex')

# Caminho para o diretório de saída (ex: ./out)
saida = os.path.join(home, 'out')

os.makedirs(saida, exist_ok=True)

# Comando de compilação
comando = [
    'xelatex',
    '-interaction=nonstopmode',
    f'-output-directory={saida}',
    entrada
]


def solve_q01(data: ResolvedData, beta: int) -> List[Step]:
    steps: List[Step] = []

    # Pb, N, eta_th_f, eta_m, PCI = sp.symbols('Pb N eta_th_f eta_m PCI', positive=True, real=True)
    # d, c, rho_ar, mdot_f, V_ar = sp.symbols('mdot_f V_ar d c rho_ar', positive=True, real=True)
    # AF, Up, eta_v, eta_th_i, V_d, pme = sp.symbols('AF Up eta_v eta_th_i V_d pme', positive=True, real=True)

    # Simbólicos básicos
    Pb, N, PCI = sp.symbols('Pb N PCI', positive=True, real=True)

    # Eficiências
    eta_th_f, eta_m, eta_th_i, eta_v = sp.symbols('eta_th_f eta_m eta_th_i eta_v', positive=True, real=True)

    # Dimensões e propriedades físicas
    d, c, rho_ar = sp.symbols('d c rho_ar', positive=True, real=True)

    # Resultados de interesse
    mdot_f, V_ar, V_d, pme, Up = sp.symbols('mdot_f V_ar V_d pme Up', positive=True, real=True)

    # Razão ar/comb
    AF = sp.Symbol('AF', positive=True, real=True)

    # ETAPA 1: Consumo combustível kg/h
    mdot_f_eq = sp.Eq(mdot_f, (Pb / (eta_th_f * PCI)) * 3600)
    mdot_f_value = float(mdot_f_eq.rhs.subs({Pb: data["Pb"], eta_th_f: data["eta_th_f"], PCI: data["PCI"]}).evalf())
    add_step(steps,
             "Consumo de combustível (kg/h)",
             "Fórmula padrão para motores: $\\dot{{m}}_f = \\frac{{P_e}}{\\eta_{{t,e}} \\cdot PCI} \\times 3600$. "
             "Convertendo $P_e$ para W e isolando obtemos o consumo em kg/h.",
             expr=mdot_f_eq,
             value=mdot_f_value
             )

    # ETAPA 2: Vazão ar (m³/h)
    V_ar_eq = sp.Eq(V_ar, (AF * mdot_f) / rho_ar)
    V_ar_h_value = float(V_ar_eq.rhs.subs({
        AF: data["AF"],
        mdot_f: mdot_f_value,
        rho_ar: data["rho_ar"]
    }).evalf())

    add_step(steps,
             "Vazão volumétrica de ar (m$^3$/h)",
             "Aplicamos a fórmula $\\dot{{V}}_{{ar}} = \\frac{{AF_m \\cdot \\dot{{m}}_f}}{\\rho_{{ar}}}$. "
             "Multiplicamos o consumo de combustível por hora pela razão ar/combustível e dividimos pela densidade do ar "
             "para obter a vazão em m$^3$/h.",
             expr=V_ar_eq,
             value=V_ar_h_value
             )

    # ETAPA 3: Eficiência térmica indicada
    eta_th_i_eq = sp.Eq(eta_th_i, eta_th_f / eta_m)
    eta_th_i_value = float(eta_th_i_eq.rhs.subs({
        eta_th_f: data["eta_th_f"],
        eta_m: data["eta_m"]
    }).evalf())

    add_step(
        steps,
        "Eficiência térmica indicada",
        "Aplicamos a definição $\\eta_{t,i} = \\frac{\\eta_{t,e}}{\\eta_m}$, que relaciona a eficiência térmica ao freio com a eficiência indicada, "
        "considerando perdas mecânicas no motor.",
        expr=eta_th_i_eq,
        value=eta_th_i_value
    )

    # ETAPA 4: Cilindrada unitária (1 cilindro)
    Vd_eq = sp.Eq(V_d, sp.pi * d ** 2 / 4 * c)
    Vd_value = float(Vd_eq.rhs.subs({
        d: data["d"],
        c: data["c"]
    }).evalf())

    add_step(
        steps,
        "Cilindrada unitária (cc) (1 cilindro)",
        "Calculamos o volume deslocado por 1 cilindro usando a fórmula "
        "$V_d = \\frac{\\pi \\cdot d^2}{4} \\cdot c$, onde $d$ é o diâmetro interno e $c$ o curso do pistão.",
        expr=Vd_eq,
        value=Vd_value
    )

    # ETAPA 5: Eficiência volumétrica
    f_ciclo = data["N"] / 120  # Para motor 4 tempos
    Vd_total_expr = sp.pi * d ** 2 / 4 * c * 4  # Volume total (4 cilindros)

    V_adm_teor = Vd_total_expr * f_ciclo
    V_ar_ms = V_ar_h_value / 3600  # m³/s

    eta_v_eq = sp.Eq(V_ar_ms, eta_v * V_adm_teor)
    eta_v_value = float((V_ar_ms / V_adm_teor.subs({
        d: data["d"],
        c: data["c"],
        N: data["N"]
    })).evalf())

    add_step(
        steps,
        "Eficiência volumétrica",
        "Para motor 4 tempos, a frequência de admissão por cilindro é $f_{{ciclo}} = \\frac{{N}}{{120}}$. "
        "Calculamos a vazão volumétrica teórica de admissão por segundo como "
        "$\\dot{{V}}_{{adm,teor}} = V_d \\cdot f_{{ciclo}}$, considerando os 4 cilindros. "
        "Assim, a eficiência volumétrica é definida como $\\eta_v = \\frac{{\\dot{{V}}_{{ar}}}}{{\\dot{{V}}_{{adm,teor}}}}$.",
        expr=eta_v_eq,
        value=eta_v_value
    )

    # ETAPA 6: Pressão média efetiva (Pa)

    pme_eq = sp.Eq(pme, Pb / (Vd_total_expr * f_ciclo))

    pme_value = float((data["Pb"] / (
            (sp.pi * data["d"] ** 2 / 4 * data["c"] * 4) * f_ciclo
    )).evalf())

    add_step(
        steps,
        "Pressão média efetiva (Pa)",
        "A pressão média efetiva é dada por $p_{{me}} = \\frac{{P_e}}{{V_d \\cdot f_{{ciclo}}}}$, "
        "onde $V_d$ é o volume total deslocado e $f_{{ciclo}} = \\frac{{N}}{{120}}$ em motores 4 tempos.",
        pme_eq,
        pme_value
    )

    # ETAPA 7: Velocidade média do pistão (m/s)
    Up_eq = sp.Eq(Up, 2 * c * N / 60)
    Up_value = float(Up_eq.rhs.subs({
        c: data["c"],
        N: data["N"]
    }).evalf())

    add_step(
        steps,
        "Velocidade média do pistão (m/s)",
        "A velocidade média do pistão é calculada por $U_p = \\frac{2 \\cdot c \\cdot N}{60}$, "
        "considerando dois deslocamentos lineares por rotação do virabrequim.",
        Up_eq,
        Up_value
    )

    # ✅ AVALIAÇÃO FINAL (subs_map completo)
    subs_map = {
        Pb: data["Pb"], N: data["N"], eta_th_f: data["eta_th_f"],
        eta_m: data["eta_m"], PCI: data["PCI"],
        d: data["d"], c: data["c"], rho_ar: data["rho_ar"]
    }

    # for step in steps:
    #     # Força limpeza de TODOS símbolos residuais
    #     step.value = sp.simplify(step.expr.subs(subs_map).doit())

    return steps


raw_data_q01 = {
    # β-adaptativos (por grupo)
    "Pb": lambda beta, ctx: float(f"6{beta}000"),  # W
    "N": lambda beta, ctx: float(f"2{beta}00"),  # rpm
    "eta_th_f": 0.30,  # %
    "eta_m": lambda beta, ctx: float(f"0.8{beta}"),
    "PCI": lambda beta, ctx: float(f"4{beta}000000"),  # J/kg
    "AF": 15,
    "rho_ar": 1.184,  # kg/m³

    "d": lambda beta, ctx: float(f"0.12{beta}"),  # m
    "c": 0.10,  # fixo 10 cm
}


def format_question_text(data: ResolvedData) -> str:
    """Gera enunciado com dados numéricos formatados."""
    Pb_kw = float(data["Pb"]) / 1000
    N_rpm = int(float(data["N"]))
    PCI_mjkg = float(data["PCI"]) / 1e6
    d_mm = float(data["d"]) * 1000
    c_mm = float(data["c"]) * 1000

    return f"""Um motor de ignição por compressão de 4 tempos apresenta potência de 
\\textbf{{{Pb_kw:.0f} kW}} a {N_rpm} rpm. A eficiência térmica ao freio é de 30\\% e 
o poder calorífico inferior do combustível é de \\textbf{{{PCI_mjkg:.0f} MJ/kg}}. 
O diâmetro do cilindro é \\textbf{{{d_mm:.1f} mm}} e o curso {c_mm:.0f} mm. 
Considerando densidade do ar = \\textbf{{1.184 kg/m$^3$}}:

\\begin{{enumerate}}
\\item Determinar o consumo de combustível em kg/h;
\\item Consumo de ar em m$^3$/h;  
\\item Eficiência térmica indicada;
\\item Eficiência volumétrica;
\\item Pressão média efetiva;
\\item Velocidade média do pistão.
\\end{{enumerate}}"""


if __name__ == "__main__":
    data, steps, beta = solve_problem(
        "Motor Otto 4T - Consumo específico (β-adaptativo)",
        solve_q01, raw_data_q01, beta_value=2
    )

    section_tex = question_to_latex_section(
        q_number=1,
        problem_title="Motor Otto 4T",
        given=data,
        steps=steps,
        question_text=format_question_text(data)
    )

    with open("q01_section.tex", "w") as f:
        f.write(section_tex)

    print(f"✅ Q01 gerada (β={beta})")

    print(f"  m_f     = {safe_float(steps[0].value)} kg/h")
    print(f"  V_ar    = {safe_float(steps[1].value)} m³/h")
    print(f"  η_t,i   = {safe_float(steps[2].value)} %")
    print(f"  η_v     = {safe_float(steps[3].value)} %")
    print(f"  p_me    = {safe_float(steps[4].value)} bar")
    print(f"  U_p     = {safe_float(steps[5].value)} m/s")


    processo = subprocess.run(comando, cwd=home, capture_output=True, text=True)

    # Mostra a saída da compilação
    print('Saída:')
    print(processo.stdout)

    print('\nErros:')
    print(processo.stderr)