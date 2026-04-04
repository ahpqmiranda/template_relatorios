\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{PPGEI-tex}[2026/04/03 Classe adaptada para o modelo PPGEI baseada em Article]

\newcommand{\headlinecolor}{\normalcolor}
% Alterado de report para article
\LoadClass[12pt,a4paper]{article}

\setcounter{tocdepth}{3}
\setcounter{secnumdepth}{3}
\RequirePackage[english,portuguese]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{xcolor}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{makeidx}
\RequirePackage{graphicx}
\RequirePackage{setspace}
\RequirePackage{mfirstuc}
\RequirePackage[portuguese]{nomencl}
\RequirePackage{verbatim}
\RequirePackage{pdfpages}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{booktabs}
\RequirePackage[nottoc, notlof, notlot]{tocbibind}
\RequirePackage{fancyhdr}
\RequirePackage{titletoc}
\RequirePackage{titlesec}
\RequirePackage{etoolbox}
\RequirePackage{indentfirst}
\RequirePackage{float}
\RequirePackage{enumitem}
\RequirePackage[section]{placeins}
\RequirePackage[subsection]{placeins}
\RequirePackage{listings}
\RequirePackage[alf]{abntex2cite}
\RequirePackage[acronym]{glossaries}
\RequirePackage{siunitx}
% ------------------------------------------------------------------------
% PACOTE E CONFIGURAÇÃO DE LINKS (Navegação no PDF)
% ------------------------------------------------------------------------

\sisetup{per-mode=symbol}

% CONFIGURAR CAPTION E SUBCAPTION
\captionsetup{font=footnotesize, labelfont=bf, margin = 25pt}

% CONFIGURAR O AMBIENTE QUOTE
\renewenvironment{quote}
{\small\list{}{ \leftmargin=4cm \rightmargin=0cm \itshape \singlespacing}%
\item\relax}
{\endlist}

% CONFIGURANDO O ESPAÇAMENTO
\onehalfspacing

% CONFIGURA O SUMÁRIO USANDO O titletoc (Adaptado para article)
\titlecontents{section}
[.5em] %
{\smallskip}
{\textbf{\thecontentslabel}\enspace\textbf}
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\textbf{\contentspage}}

\titlecontents{subsection}
[2.0em] %
{\smallskip}
{\thecontentslabel\enspace}
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\contentspage}

\titlecontents{subsubsection}
[4.5em] %
{\smallskip}
{\thecontentslabel\enspace}
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\contentspage}

% CONFIGURA O PACOTE nomencl
\makenomenclature
\renewcommand{\nomname}{\hfill Lista de Abreviaturas e Símbolos\hfill}
\renewcommand\nomgroup[1]{%
    \item[\bfseries
    \ifstrequal{#1}{C}{Símbolos}{%
        \ifstrequal{#1}{S}{Siglas}{}}%
    ]}

\RequirePackage[left=3cm,right=2cm,top=3cm,bottom=2cm]{geometry}

% CONFIGURA O fancyhdr
\pagestyle{fancy}
\fancyhf{}
\setlength{\headheight}{15.1pt}
\lhead{\leftmark}
\rhead{Página \thepage}

% RENOMEIA O table of contens
\AtBeginDocument{\renewcommand{\contentsname}{\hfill Sumário\hfill}}
\AtBeginDocument{\renewcommand{\listfigurename}{\hfill Lista de figuras \hfill}}
\AtBeginDocument{\renewcommand{\listtablename}{\hfill Lista de tabelas \hfill}}

%%%%%%%% COMANDOS EXTRAS PARA VALORES DE CRIAÇÃO DA CAPA E CONTRA CAPA %%%%%%
\newcommand{\getuniversidade}{}
\newcommand{\universidade}[1]{\renewcommand{\getuniversidade}{#1}}

\newcommand{\getsetor}{}
\newcommand{\setor}[1]{\renewcommand{\getsetor}{#1}}

\newcommand{\getprograma}{}
\newcommand{\programa}[1]{\renewcommand{\getprograma}{#1}}

\newcommand{\getbrasao}{}
\newcommand{\brasao}[1]{\renewcommand{\getbrasao}{#1}}

\newcommand{\getlocal}{}
\newcommand{\local}[1]{\renewcommand{\getlocal}{#1}}

\newcommand{\getcurso}{}
\newcommand{\curso}[1]{\renewcommand{\getcurso}{#1}}

\newcommand{\gettitulo}{}
\newcommand{\titulo}[1]{\renewcommand{\gettitulo}{#1}}

\newcommand{\getareaconcentracao}{}
\newcommand{\areaconcentracao}[1]{\renewcommand{\getareaconcentracao}{#1}}

\newcommand{\getorientador}{}
\newcommand{\orientador}[1]{\renewcommand{\getorientador}{#1}}

\newcommand{\getcoorientador}{}
\newcommand{\coorientador}[1]{\renewcommand{\getcoorientador}{#1}}

\newcommand{\getfichacatalografica}{}
\newcommand{\fichacatalografica}[1]{\renewcommand{\getfichacatalografica}{#1}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% CRIA A CAPA
\newcommand{\criarcapa}{%
    \newpage
    \setcounter{page}{0}
    \thispagestyle{empty}
    \begin{center}%

    \lineskip .5em%
    \begin{figure}[h]
    \centering
    \includegraphics[width=0.2\linewidth]{\getbrasao}
    \end{figure}
    \textbf{\MakeUppercase{\getuniversidade}}

    \textbf{\MakeUppercase{\getsetor}}

    \textbf{\MakeUppercase{\getprograma}}

    \vspace{2cm}

    \textbf{\MakeUppercase{\@author}}

    \vspace{5cm}

    {\textbf{\MakeUppercase{\getareaconcentracao}}}

    \vspace{0.5cm}

    {\textbf{\MakeUppercase{\@title}}}
    \vfill%
    {
        \textbf{\getlocal}

        \textbf{\the\year}}%
    \end{center}%
    \par
    \vskip 1.5em}

% CRIA A CONTRA-CAPA
\newcommand{\criarcontracapa}{%
    \newpage
    \thispagestyle{empty}
    \begin{center}%

    \lineskip .5em%
    \textbf{\MakeUppercase{\getuniversidade}}

    \textbf{\MakeUppercase{\getsetor}}

    \textbf{\MakeUppercase{\getprograma}}

    \vspace{2cm}

    {\textbf{\MakeUppercase{\getareaconcentracao}}}

    \vspace{0.5cm}

    {\textbf{\MakeUppercase{\@title}}}

    \vspace{2cm}

    \textbf{\MakeUppercase{\@author}}

    \vspace{0.5cm}

    \begin{flushright}
    \noindent\mbox{%
        \parbox{.48\textwidth}{%
            Atividade submetida à avaliação disciplinar do professor \xcapitalisewords{\getorientador} do Corpo Docente da \xcapitalisewords{\getuniversidade} como requisito para obtenção de aprovação disciplinar em \xcapitalisewords{\gettitulo} do bacharelado em \xcapitalisewords{\getcurso}.\\

            Orientador: \xcapitalisewords{\getorientador}\\

            Belém-PA: \today
        }%
    }
    \end{flushright}

    \vfill%
    {
        \textbf{\getlocal}

        \textbf{\the\year}}%
    \end{center}%
    \par
    \vskip 1.5em}

% CRIA A FICHA CATALOGRÁFICA
\newcommand{\criarfichacatalografica}{
    \newpage
    \thispagestyle{empty}
    \mbox

    \vfill
    \begin{center}
    \textbf{FICHA CATALOGRÁFICA}
    \vspace{.5cm}
    \end{center}

    \noindent\fbox{%
        \parbox{\textwidth}{%
            \begin{large}
            \getfichacatalografica
            \end{large}
        }%
    }
}

% CRIA A PÁGINA DE ASSINATURAS
\newcommand{\criarpaginaassinatura}{
    \newpage
    \thispagestyle{empty}
    \begin{center}
    \textbf{\MakeUppercase{\@author}}

    \vspace{2cm}

    {\Large\textbf{\MakeUppercase{\@title}}}

    \vspace{2cm}

    \begin{flushright}
    {\setstretch{2.0}\noindent\mbox{%
        \parbox{.6\textwidth}{%
            Atividade submetida à avaliação disciplinar do professor \xcapitalisewords{\getorientador} do Corpo Docente da \xcapitalisewords{\getuniversidade} como requisito para obtenção de aprovação disciplinar em \xcapitalisewords{\gettitulo} do bacharelado em \xcapitalisewords{\getcurso}.\\


            \vspace{1.5cm}

            \getlocal, \rule{1.5cm}{0.4pt}  de \rule{3cm}{0.4pt}  de \the\year.
        }%
    }
    }
    \end{flushright}

    \vspace{\fill}

    \noindent\rule{.7\textwidth}{0.4pt}

    \getorientador
    \end{center}
}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    numbers=left,
    numbersep=5pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2
}

\lstset{style=mystyle}

% ------------------------------------------------------------------------
% CONFIGURAÇÃO DAS REFERÊNCIAS PARA A CLASSE ARTICLE
% ------------------------------------------------------------------------
\AtBeginDocument{%
% Garante que o nome seja "Referências" em vez de "Bibliografia"
    \renewcommand{\refname}{Referências}%

    % Descomente a opção desejada abaixo:

    % OPÇÃO 1: Referências numeradas (Ex: "5 Referências")
    \renewcommand{\bibsection}{\section{\refname}}

% OPÇÃO 2: Referências NÃO numeradas, mas inclusas no sumário
% \renewcommand{\bibsection}{\section*{\refname}}
}
