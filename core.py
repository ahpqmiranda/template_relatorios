from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union, Tuple
import sympy as sp

# =============================================================================
# 0) Tipos e estruturas
# =============================================================================

BetaLike = Union[int, float, sp.Expr]
DataValue = Union[
    int,
    float,
    sp.Expr,
    Callable[[sp.Symbol, Dict[str, Any]], Union[int, float, sp.Expr]],
]
RawData = Dict[str, DataValue]
ResolvedData = Dict[str, sp.Expr]


@dataclass
class Step:
    """
    Representa uma etapa do solucionário.

    - title: nome curto da etapa (ex.: "Potência indicada")
    - rationale: justificativa textual (o "porquê" da etapa)
    - expr: expressão/igualdade simbólica (SymPy) para documentar o cálculo
    - value: resultado numérico/simbólico (após substituições)
    - extra_latex: campo opcional para inserir texto/observações em LaTeX
    """
    title: str
    rationale: str
    expr: sp.Expr
    value: Optional[int, float] = None
    extra_latex: Optional[str] = None


# =============================================================================
# 1) Núcleo: beta, resolução de dados e utilitários
# =============================================================================

def make_beta(name: str = "beta") -> sp.Symbol:
    """
    Cria o símbolo beta como constante simbólica.
    Use subs={beta: valor_inteiro} quando quiser resultado numérico.
    """
    return sp.Symbol(name, real=True)



def resolve_data(raw: RawData, beta_int: int, *, simplify: bool = True) -> ResolvedData:
    """
    Recebe beta INTEIRO, cria Symbol só para lambdas.
    """
    beta_sym = sp.Symbol("beta", real=True)  # temporário para lambdas
    resolved: ResolvedData = {}

    def to_sympy(x: Any) -> sp.Expr:
        if isinstance(x, sp.Expr): return x
        if isinstance(x, bool): return sp.Integer(int(x))
        if isinstance(x, int): return sp.Integer(x)
        if isinstance(x, float): return sp.Float(x)
        return sp.sympify(x)

    # Resolve dados
    for k, v in raw.items():
        if callable(v):
            # ✅ CHAVE: passa beta_int como número, não Symbol!
            computed_sym = v(beta_int, resolved)  # beta_int ao invés de beta_sym!
            resolved[k] = to_sympy(computed_sym)
        else:
            resolved[k] = to_sympy(v)

    return {k: sp.simplify(v) if simplify else v for k, v in resolved.items()}



def eval_expr(expr: sp.Expr, subs: Dict[sp.Symbol, BetaLike], *, simplify: bool = True) -> sp.Expr:
    """
    Substitui símbolos (ex.: beta) e avalia expressão.
    """
    out = expr.subs(subs)
    return sp.simplify(out) if simplify else out


def add_step(
        steps: List[Step],
        title: str,
        rationale: str,  # Comentário (quebra linhas OK)
        expr: sp.Expr,
        value: Union[float, None] = None,  # Aceita numérico direto!
        *,
        simplify: bool = True,
        extra_latex: Optional[str] = None
) -> None:
    """Nova versão: aceita value numérico direto."""
    st = Step(title=title, rationale=rationale, expr=expr, value=value, extra_latex=extra_latex)

    if value is not None:
        if isinstance(value, (int, float)):
            st.value = value  # <- mantenha float nativo
        else:
            st.value = sp.simplify(value)

    steps.append(st)


# =============================================================================
# 2) Helpers de domínio (motores/combustão)
# =============================================================================

def cycles_per_second(N_rpm: sp.Expr, *, four_stroke: bool = True) -> sp.Expr:
    """
    Retorna a frequência de ciclos [ciclos/s].
    - 4 tempos: 1 ciclo a cada 2 voltas => N/120
    - 2 tempos: 1 ciclo a cada 1 volta => N/60
    """
    return N_rpm / (120 if four_stroke else 60)


def brake_to_indicated_power(Pb: sp.Expr, eta_m: sp.Expr) -> sp.Expr:
    """
    Converte potência ao freio (eixo) em potência indicada via eficiência mecânica:
    eta_m = Pb / Pi  => Pi = Pb/eta_m
    """
    return Pb / eta_m


def fuel_vol_flow_from_indicated(Pi: sp.Expr, eta_th_i: sp.Expr, PCI_v: sp.Expr) -> sp.Expr:
    """
    Vazão volumétrica de combustível quando PCI é dado por volume:
    eta_th,i = Pi / (Vdot_f * PCI_v)  => Vdot_f = Pi / (eta_th,i * PCI_v)
    """
    return Pi / (eta_th_i * PCI_v)


def air_vol_flow_from_ratio(Vdot_f: sp.Expr, AF_vol: sp.Expr) -> sp.Expr:
    """
    Vazão volumétrica de ar usando razão volumétrica ar/combustível:
    Vdot_a = (A/F)_vol * Vdot_f
    """
    return AF_vol * Vdot_f


def displacement_from_vol_eff(Vdot_a: sp.Expr, eta_v: sp.Expr, N_rpm: sp.Expr, *, four_stroke: bool = True) -> sp.Expr:
    """
    Relaciona vazão volumétrica admitida e cilindrada:
    Vdot_a = eta_v * Vd * f_ciclo
    => Vd = Vdot_a / (eta_v * f_ciclo)
    """
    f = cycles_per_second(N_rpm, four_stroke=four_stroke)
    return Vdot_a / (eta_v * f)


# =============================================================================
# 3) Exportação LaTeX
# =============================================================================

def steps_to_latex(
        title: str,
        given: ResolvedData,
        steps: List[Step]
) -> str:
    """
    Gera um .tex completo com:
    - Título
    - Dados
    - Etapas: justificativa + expressão + resultado (se calculado)
    """

    def latex_expr(e: sp.Expr) -> str:
        return sp.latex(sp.simplify(e))

    lines: List[str] = []
    lines += [
        r"\documentclass[12pt]{article}",
        r"\usepackage[a4paper,margin=2cm]{geometry}",
        r"\usepackage{amsmath,amssymb}",
        r"\usepackage{enumitem}",
        r"\usepackage{hyperref}",
        r"\begin{document}",
        rf"\section*{{{title}}}",
        r"\subsection*{Dados}",
        r"\begin{itemize}[leftmargin=*,itemsep=2pt]",
    ]

    # Dados
    for k, v in given.items():
        lines.append(rf"\item ${k} = {latex_expr(v)}$")

    lines += [r"\end{itemize}", r"\subsection*{Solu\c{c}\~ao (etapas)}", r"\begin{enumerate}[leftmargin=*]"]

    for st in steps:
        lines.append(r"\item \textbf{" + st.title + r"}\\")
        lines.append(st.rationale + r"\\")
        lines.append(r"\[ " + latex_expr(st.expr) + r" \]")

        if st.value is not None:
            lines.append(r"\[ \Rightarrow " + latex_expr(st.value) + r" \]")

        if st.extra_latex:
            lines.append(st.extra_latex)

    lines += [r"\end{enumerate}", r"\end{document}"]
    return "\n".join(lines)


def question_to_latex_section(
        q_number: int, problem_title: str, given: ResolvedData,
        steps: List[Step], question_text: str = ""
) -> str:
    def latex_expr(e: sp.Expr) -> str:
        """✅ Suporte completo Eq + expr simples."""
        if isinstance(e, (float, int)):
            return f"{e}"  # formata float com até 6 dígitos úteis
        elif isinstance(e, sp.Eq):
            return sp.latex(e)  # Eq nativo: lhs = rhs
        elif isinstance(e, sp.Expr):
            return sp.latex(sp.simplify(e))
        return str(e)

    def format_question_text(text: str) -> List[str]:
        """✅ Formatação ANTI-CORTE: parágrafos reais + verbatim para longas linhas."""
        lines = [r"\begin{{verbatim}}"]  # Caixa com quebra automática

        for para in text.split('\n\n'):  # Parágrafos
            para = para.strip()
            if para:
                # Substitui $$ por $ e quebra linhas longas
                para = para.replace("$$", "$")
                lines.append(para.replace("\\textbf{", "\\textbf{").replace("}", "}"))
                lines.append("")  # quebra linha

        lines.append(r"\end{{verbatim}}")
        return lines

    lines = [
        rf"\newpage",
        rf"\section*{{Questão {q_number} — {problem_title}}}",
        rf"\label{{sec:q_{q_number}}}",
        r"\vspace{{10pt}}",  # espaço antes enunciado
    ]

    # ✅ ENUNCIADO SEM CORTE
    if question_text.strip():
        lines += [
            r"\begin{{minipage}}{{\textwidth}}",  # largura total
            r"\small",  # fonte menor
            r"\paragraph{{Enunciado:}}"
        ]
        lines += format_question_text(question_text)
        lines += [
            r"\end{{minipage}}",
            r"\vspace{{15pt}}"
        ]

    unit_map_text = {
        "Pb": r"W",  # Potência: Watts
        "N": r"min^{-1}",  # Rotação: rpm = min⁻¹
        "PCI": r"J/kg",  # PCI: Joule/kg
        "d": r"m",  # Diâmetro: metros
        "c": r"m",  # Curso: metros
        "eta_th_f": r"--",  # Eficiência: adimensional
        "eta_m": r"--",
        "v_d": r"m$^3$",
        "AF": r"--",  # Razão mássica: adimensional
        "rho_ar": r"kg/m$^3$",  # Densidade: kg/m³
        "mdot_f": r"kg/h",  # Consumo: kg/h (padrão técnico)
        "V_ar": r"m$^3$/h",
    }


    # DADOS - TABELA SIMPLES (substitua seu itemize)
    lines += [
        r"\subsection*{Solução}",
        r"\noindent\textbf{Dados:}\\[5pt]",
        r"\begin{center}",
        r"\begin{tabular}{|c|r|c|} \hline",
        r"\textbf{Parâmetro} & \textbf{Valor} & \textbf{{Unidade}} \\ \hline\hline"
    ]

    for k, v in given.items():
        unit = f"{unit_map_text.get(k, '--')}"  # padrão se não achar
        lines.append(rf"${k}$ & {latex_expr(v)} & {unit} \\ \hline")

    lines += [
        r"\end{tabular}",
        r"\end{center}\\[10pt]",
        r"\paragraph{Resolução:}",
        r"\begin{enumerate}[leftmargin=*,itemsep=8pt]"
    ]

    # No loop dos steps:
    for st in steps:
        lines += [
            rf"\subsubsection*{{{st.title}}}",  # título
            rf"\noindent {st.rationale}",  # comentário
        ]
        print("Valor do step:", st.value, "->", latex_expr(st.value))

        # ✅ EQ ou EXPR - funciona ambos!
        lines.append(rf"\[{latex_expr(st.expr)}\]")  # fórmula simbólica

        if st.value is not None:
            lines.append(rf"\[\Rightarrow {latex_expr(st.value)}\]")  # resultado!

        if st.extra_latex:
            lines.append(rf"\noindent\footnotesize{{{st.extra_latex}}}")

        lines.append(r"\vspace{{6pt}}")

    lines += [r"\end{{enumerate}}", r"\newpage"]
    return "\n".join(lines)


def safe_float(val: Any) -> float:
    """Converte QUALQUER SymPy → float (Eq, Expr, Float, número)."""
    if val is None:
        return 0.0

    # Se Eq → pega rhs
    if hasattr(val, 'rhs'):
        val = val.rhs

    # Se tem evalf → calcula
    if hasattr(val, 'evalf'):
        val = val.evalf()

    # N para número decimal
    if hasattr(val, 'n'):
        val = val.n()

    return float(val)


# =============================================================================
# 5) Runner (padrão para todas as questões)
# =============================================================================

def normalize_beta(beta_value: int) -> int:
    """Garante que beta é inteiro válido (ex.: 3, 4, 5...)."""
    return int(beta_value)


def solve_problem(
        problem_title: str,
        solver_fn: Callable[[ResolvedData, int], List[Step]],  # ✅ beta agora é int!
        raw_data: RawData,
        *,
        beta_value: int  # obrigatório!
) -> Tuple[ResolvedData, List[Step], int]:
    """
    Versão simplificada: beta é SEMPRE inteiro obrigatório.

    Remove:
    - beta simbólico (não usado mais)
    - subs simbólico (complicado)

    Mantém:
    - resolve_data() com lambdas usando beta_sym interno
    - steps com .value já calculados
    """
    beta = int(beta_value)
    data = resolve_data(raw_data, beta)  # ✅ beta int!
    steps = solver_fn(data, beta)
    return data, steps, beta
