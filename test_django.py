import sys
print("Python path:", sys.executable)
print("Python version:", sys.version)

try:
    import django
    print("Django version:", django.get_version())
except ImportError as e:
    print("Error importing Django:", e) 