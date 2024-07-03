from setuptools import setup
import sys
import os

# Adicione aqui o nome do arquivo Python principal da sua aplicação
main_script = 'index.py'

sys.argv.append('py2app')

setup(
    app=[main_script],
    options={
        'py2app': {
            'packages': ['customtkinter', 'sqlite3', 'lancamento'],  # Adicione aqui os pacotes que sua aplicação utiliza
        },
    },
    setup_requires=['py2app'],
)
