\NeedsTeXFormat{LaTeX2e}
% \ProvidesClass{PPGEI-tex}[2021/10/03 Classe criada para o modelo de tese no PPGEI]

\newcommand{\headlinecolor}{\normalcolor}
\LoadClass[12pt,a4paper]{report}
\setcounter{tocdepth}{3}
\setcounter{secnumdepth}{3}
\RequirePackage[english,portuguese]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{xcolor}                       %PACOTE PARA ALTERAR A COR DAS LETRAS
\RequirePackage{amsmath}                      %FACILITA A ESCRITA MATEMÁTICA
\RequirePackage{amsfonts}                     %EXTENSÃO QUE ADICIONA LETRAS E ALGUNS SÍMBOLOS MATEMÁTICOS
\RequirePackage{amssymb}                      %ADICIONA AINDA MAIS SÍMBOLOS MATEMÁTICOS
\RequirePackage{makeidx}                      %CRIA ÍNDICES
\RequirePackage{graphicx}                     %OFERECE FACILIDADES E MAIS CONFIGURAÇÕES PARA O \includegraphics{}
\RequirePackage{setspace}                     %OFERECE SUPORTE PARA CONFIGURAR O ESPAÇAMENTO ENTRE AS LINHAS
\RequirePackage{chngcntr}                     %MUDA COMO OS CONTADORES PODEM SER RESETADOS, PERMITINDO OUTRAS FORMAS DE MOSTRAR AS SEÇÕES E CAPÍTULOS
\RequirePackage{mfirstuc}                     %OFERECE OS COMANDOS QUE PERMITEM A CAPITALIZAÇÃO DA PRIMEIRA LETRA DA PALAVRA
\RequirePackage[portuguese]{nomencl}          %CRIA LISTA DE SÍMBOLOS E NOMENCLATURAS
\RequirePackage{verbatim}                     %OFERECCE O COMANDO \begin{verbatim} QUE PERMITE QUE O CÓDIGO SEJA MOSTRADO SEM COMPILAR
\RequirePackage{pdfpages}                     %PERMITE A INCLUSÃO DE PDFs
\RequirePackage{caption}                      %PERMITE CONFIGURAÇÕES EXTRAS DO \caption{}
\RequirePackage{subcaption}                   %PERMITE A ESCRITA DE SUBCAPTION EM SUBFIGURAS
\RequirePackage{booktabs}                     %MELHORA A QUALIDADE DAS TABELAS
\RequirePackage[nottoc, notlof, notlot]{tocbibind}            %ADICIONA A BIBLIOGRAFIA AO SUMÁRIO
\RequirePackage{fancyhdr}                     %PERMITE UMA EDIÇÃO MAIS BONITA DO CABEÇALHO E RODAPÉ DA PÁGINA
\RequirePackage{titletoc}                     %PERMITE A EDIÇÃO DO SUMÁRIO
\RequirePackage{titlesec}                     %PERMITE A EDIÇÃO DO TÍTULO DOS CAPÍTULOS E SEÇÕES
\RequirePackage{setspace}                     %PERMITE A ALTERAÇÃO DO ESPAÇAMENTO ENTRE AS LINHAS
\RequirePackage{pdfpages}                     %PERMITE INCLUIR PDF NO DOCUMENTO
\RequirePackage{etoolbox}                     %PERMITE INICIAR UMA FUNÇÃO NO COMEÇO DE UM AMBIENTE
\RequirePackage{indentfirst}
\RequirePackage{float}                        %PERMITE MELHORAR O CONTROLE DE FIGURAS E TABELAS
\RequirePackage{enumitem}                     %PERMITE MELHORAR A LISTAS ENUMERADAS E COM MARCADORES
\RequirePackage[section]{placeins}
\RequirePackage[subsection]{placeins}
\RequirePackage{listings}                      %PERMITE INCLUIR CÓDIGOS-FONTE NO DOCUMENTO
\RequirePackage[alf]{abntex2cite}               % referências abnt
%\RequirePackage[subsubsection]{placeins}
%\RequirePackage[subsubsection]{placeins}
\RequirePackage{lipsum}
\RequirePackage{siunitx}    % unidades
\sisetup{per-mode=symbol}  % η = 30%


%CONFIGURAR CAPTION E SUBCAPTION
\captionsetup{font=footnotesize, labelfont=bf, margin = 25pt}

%CONFIGURAR O AMBIENTE QUOTE
\renewenvironment{quote}
{\small\list{}{ \leftmargin=4cm \rightmargin=0cm \itshape \singlespacing}%
\item\relax}
{\endlist}

%CONFIGURA UMA LINHA BONITINHA NOS CAPÍTULOS
\newcommand{\hsp}{\hspace{20pt}}
\titleformat{\chapter}[hang]{\Huge\bfseries}{\thechapter\hsp\textcolor{gray!75}{|}\hsp}{0pt}{\Huge\bfseries}
%\titlespacing*{\chapter}{0pt}{-40pt}{40pt}
\titlespacing*{\chapter}{0pt}{0pt}{40pt}  % sem asterisco
%CONFIGURANDO O ESPAÇAMENTO
\onehalfspacing

%CONFIGURA O SUMÁRIO USANDO O titletoc
\titlecontents{section}
[.5em] %
{\smallskip}
{\thecontentslabel\enspace}%\thecontentslabel
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\contentspage}

\titlecontents{subsection}
[2.0em] %
{\smallskip}
{\textbf\thecontentslabel\enspace\textbf}%\thecontentslabel
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\textbf\contentspage}

\titlecontents{subsubsection}
[4.5em] %
{\smallskip}
{\thecontentslabel\enspace}%\thecontentslabel
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\contentspage}

\titlecontents{figure}
[-.2em] %
{\smallskip}
{\thecontentslabel\enspace}%\thecontentslabel
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\contentspage}

\titlecontents{table}
[-.2em] %
{\smallskip}
{\thecontentslabel\enspace}%\thecontentslabel
{\hspace*{7.12em}}
{\titlerule*[.75pc]{.}\contentspage}

%CONFIGURA O PACOTE nomencl
\makenomenclature
\renewcommand{\nomname}{\hfill Lista de Abreviaturas e Símbolos\hfill}
\renewcommand\nomgroup[1]{%
    \item[\bfseries
    \ifstrequal{#1}{C}{Símbolos}{%
        \ifstrequal{#1}{S}{Siglas}{}}%
    ]}


%CONFIGURA O PACOTE chngcntr
%\counterwithin{figure}{chapter}
%\counterwithin{table}{chapter}
\counterwithout{figure}{chapter}
\counterwithout{table}{chapter}
\RequirePackage[left=3cm,right=2cm,top=3cm,bottom=2cm]{geometry}

%CONFIGURA O fancyhdr
\pagestyle{fancy}
\fancyhf{}
\setlength{\headheight}{15.1pt}
\lhead{\leftmark}
\rhead{Página \thepage}


%RENOMEIA O table of contens
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


%CRIA A CAPA
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
    {\textbf{\MakeUppercase{\@title}}}
    \vfill%    
    {
        \textbf{\getlocal}

        \textbf{\the\year}}%
    \end{center}%
    \par
    \vskip 1.5em}


%CRIA A CONTRA-CAPA
\newcommand{\criarcontracapa}{%
    \newpage
    \thispagestyle{empty}
    \begin{center}%

    \lineskip .5em%
    \textbf{\MakeUppercase{\getuniversidade}}

    \textbf{\MakeUppercase{\getsetor}}

    \textbf{\MakeUppercase{\getprograma}}

    \vspace{2cm}

    {\textbf{\MakeUppercase{\@title}}}

    \vspace{2cm}

    \textbf{\MakeUppercase{\@author}}

    \vspace{0.5cm}

    \begin{flushright}
    \noindent\mbox{%
        \parbox{.48\textwidth}{%
            Atividade submetida à avaliação disciplinar do professor \xcapitalisewords{\getorientador} do Corpo Docente da \xcapitalisewords{\getuniversidade} como requisito para obtenção de aprovação disciplinar em \xcapitalisewords{\gettitulo} do bacharelado em \xcapitalisewords{\getcurso}.\\

            Área de concentração: \getareaconcentracao

            Orientador: \xcapitalisewords{\getorientador}\\

            Belém-PA: \today

        %Co-orientador: \xcapitalisewords{\getcoorientador}
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

%CRIA A FICHA CATALOGRÁFICA
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

%CRIA A PÁGINA DE ASSINATURAS
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


\newcommand{\criarepigrafe}[2]{
    \newpage
    \thispagestyle{empty}
    \null
    \vfill

    \begin{flushright}
    {\setstretch{1.5}\noindent\mbox{%
        \parbox{.8\textwidth}{%
            \begin{flushleft}
            \textit{#1}
            \end{flushleft}

            \begin{flushright}
            (#2)
            \end{flushright}

        }%
    }
    }
    \end{flushright}

    \onehalfspacing
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
  