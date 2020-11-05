from os import system
from os.path import join, dirname, abspath

apps = ['app']
BASE_DIR = dirname(dirname(abspath(__file__)))

for app in apps:
    system(f'python {join(BASE_DIR, "manage.py")} makemigrations {app}')

system(f'python {join(BASE_DIR, "manage.py")} migrate')
