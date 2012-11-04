import os.path

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
print PROJECT_ROOT
DB_NAME = os.path.join(PROJECT_ROOT, 'pdb.db')
print DB_NAME