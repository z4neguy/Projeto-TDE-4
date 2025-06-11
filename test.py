import os
import django

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'escola.settings')  # substitua 'escola' pelo nome do seu projeto
django.setup()

from django.db import connection

print(connection.introspection.table_names())