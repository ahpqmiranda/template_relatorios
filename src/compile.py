import os
import subprocess as sp
import multiprocessing as mp

presentation = "apresentacao.pdf"
report = "relatorio.pdf"

if os.path.exists('out/' + presentation):
    os.remove('out/' + presentation)

if os.path.exists('out/' + report):
    os.remove('out/' + report)

texfiles = [i for i in os.listdir() if i.endswith('.tex')]
print(texfiles)
for i in texfiles:
    os.chdir(os.path.dirname(__file__))
    os.makedirs('out', exist_ok=True)

    subprocess = sp.run(['xelatex', i, '-output-directory=out', '-interaction=nonstopmode'], stdout=sp.PIPE,
                        stderr=sp.PIPE)
    try:
        if subprocess.returncode == 0:
            print('Success')
        else:
            print(subprocess.stdout.decode(), flush=True)
            print(subprocess.stderr.decode())
    except Exception as e:
        print(e)
    #
    # finally:
    #
        mp.Pool().map(os.remove, [f'out/{i.replace(".tex", ext)}' for ext in
                                  ['.log', '.aux', '.lof', '.toc', '.out', '.synctex.gz']])

    # os.remove('out/' + i.replace('.tex', '.log'))
    # os.remove('out/' + i.replace('.tex', '.aux'))
    # os.remove('out/' + i.replace('.tex', '.lof'))
    # os.remove('out/' + i.replace('.tex', '.toc'))
    # os.remove('out/' + i.replace('.tex', '.out'))
    # os.remove('out/' + i.replace('.tex', '.synctex.gz'))
    # # os.remove('out/main.synctex.gz(busy)')
