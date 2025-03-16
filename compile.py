import os
import subprocess as sp


if os.path.exists('out/main.pdf'):
    os.remove('out/main.pdf')

os.chdir(os.path.dirname(__file__))
os.makedirs('out', exist_ok=True)

subprocess = sp.run(['xelatex',
                     'src/main.tex',
                     '-no-pdf',
                     '-interaction=nonstopmode',
                     '-synctex=1', '%0', '%S'], stdout=sp.PIPE,
                    stderr=sp.PIPE) # '-output-directory=out'
try:
    if subprocess.returncode == 0:
        print('Success')
    else:
        print(subprocess.stdout.decode(), flush=True)
        print(subprocess.stderr.decode())
except Exception as e:
    print(e)

# finally:
#     try:
#         os.remove('out/main.log')
#         os.remove('out/main.aux')
#         os.remove('out/main.lof')
#         os.remove('out/main.toc')
#         os.remove('out/main.out')
#         os.remove('out/main.synctex.gz')
#     except Exception as e:
#         print(e)
#         print('Files not found to remove!')
    # os.remove('out/main.synctex.gz(busy)')
