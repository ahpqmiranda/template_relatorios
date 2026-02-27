# ⚙️ Análise de Turbomáquinas: Bomba de Fluxo Axial Lewis VL750

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)
![UFPA](https://img.shields.io/badge/UFPA-Engenharia_Mecânica-red?style=for-the-badge)

Este repositório contém o projeto de dimensionamento termofluidodinâmico, cinemático e econômico de uma bomba de fluxo axial (**Weir Lewis® VL750**) aplicada a um sistema de circulação forçada em um evaporador de múltiplo efeito.

O trabalho foi desenvolvido como requisito de avaliação na disciplina de **Máquinas de Fluxo / Turbomáquinas Hidráulicas** da Faculdade de Engenharia Mecânica da Universidade Federal do Pará (UFPA).

---

## 📋 Sobre o Projeto

O desafio de engenharia envolveu bombear $8.000 \text{ m}^3/\text{h}$ de uma solução aquosa salina altamente corrosiva a $80^\circ\text{C}$. O projeto aborda a solução completa do problema integrando:

* **Termodinâmica e Instalação:** Prevenção de cavitação via elevação da cota do evaporador, garantindo um $NPSH_d$ seguro contra a alta pressão de vapor.
* **Modelagem Cinemática:** Aplicação do Teorema de Euler para Turbomáquinas através de scripts em Python.
* **Análise de Custos:** Redução drástica de CAPEX (de ~R$ 950k para R$ 340k) substituindo uma carcaça maciça de liga Duplex 2205 por ferro fundido com revestimento catódico interno (cladding).

---

## 💻 O Pacote Python (`turbomachine`)

Para automatizar os cálculos iterativos e a geração de gráficos, desenvolvemos um pacote orientado a objetos em Python localizado na pasta `scripts/turbomachine`. 

A classe principal, `TurbomachineAnalyzer`, permite instanciar uma turbomáquina com base em seus parâmetros geométricos e condições de escoamento, calculando automaticamente:
1. Geometria do rotor (raio médio, áreas).
2. Componentes dos triângulos de velocidades (meridiana, tangencial, absoluta e relativa).
3. Transferência de energia específica pelo Teorema de Euler.

### Exemplo de Uso
```python
from turbomachine import TurbomachineAnalyzer

# Instanciando a bomba Lewis VL750
analyzer = TurbomachineAnalyzer(
    D=0.93, d=0.60, N=975, Q=2.2222, 
    alpha_4=90.0, beta_5=8.87
)

# Gerando o gráfico cinemático
analyzer.plot_velocity_triangles()
```
---
## 📊 Resultados Numéricos e Gráficos
Os algoritmos geram visualizações em dark mode prontas para relatórios técnicos industriais, salvas automaticamente no diretório out/.

1. Triângulos de Velocidades (Cinemática do Rotor)
Representação visual da transferência de momento angular. Observa-se a entrada de fluxo puramente axial na Estação 4 e o ganho de componente tangencial na Estação 5, responsável pela conversão do trabalho de eixo em carga hidrodinâmica.

2. Leis de Afinidade (Curvas de Desempenho)
Extrapolação do ponto de projeto utilizando as Leis de Afinidade. O gráfico demonstra o comportamento quadrático da Altura Manométrica e o comportamento cúbico da Potência Hidráulica frente à variação de rotação (RPM), essencial para o dimensionamento de inversores de frequência (VFD).

---
## 📄 Relatório Técnico Completo
Toda a fundamentação teórica, memorial de cálculo de perda de carga, detalhamento do motor WEG de 400 cv e o orçamento executivo com BDI estão documentados no relatório final formatado em LaTeX (Padrão ABNT).

Clique no botão abaixo para ler o documento em PDF:

<div align="center">



<a href="out/tcc.pdf">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/📄_ABRIR_RELATÓRIO_EM_PDF-FF0000?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white" alt="Abrir PDF">
</a>



</div>

Projeto acadêmico desenvolvido por Alan Miranda, Luis Mota, Jesiele Silva, José Neto e Marcos Inete — UFPA 2026.