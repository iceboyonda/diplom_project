import os
import sys
import django

# Добавляем путь к проекту в PYTHONPATH
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tyre_trust.settings')

# Инициализируем Django
django.setup()

# Импортируем и запускаем сервер
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver']) 