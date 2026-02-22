import subprocess
import os

# Caminho absoluto para o diretório raiz do projeto (dois níveis acima de q2.py)
home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Caminho para o arquivo tcc.tex
entrada = os.path.join(home, 'tcc.tex')

# Caminho para o diretório de saída (ex: ./out)
saida = os.path.join(home, 'out')

print(home)