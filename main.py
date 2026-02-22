import os
import subprocess as sp

# Garante que o script rode na pasta do arquivo .py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

output_dir = 'out'
file_name = 'tcc' # Nome sem extensão
os.makedirs(output_dir, exist_ok=True)

# Limpeza prévia (opcional)
pdf_path = os.path.join(output_dir, f'{file_name}.pdf')
if os.path.exists(pdf_path):
    os.remove(pdf_path)

# Comando corrigido
cmd = [
    'xelatex',
    f'-output-directory={output_dir}',
    '-interaction=nonstopmode',
    '-synctex=1',
    f'{file_name}.tex'
]

result = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, text=True)

if result.returncode == 0:
    print(f'✨ Sucesso! PDF gerado em: {pdf_path}')
else:
    print('❌ Erro na compilação:')
    print(result.stdout) # O log do LaTeX sai no stdout
