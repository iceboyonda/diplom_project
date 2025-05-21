import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tyre_trust.settings')
django.setup()

from tyres.models import RimModel, RimVariant

# Очищаем существующие диски
print(f"Удаление существующих моделей дисков ({RimModel.objects.count()} шт.)...")
RimModel.objects.all().delete()
print(f"Осталось моделей дисков после удаления: {RimModel.objects.count()} шт.")

# Список популярных моделей дисков с их вариациями
rims_data = [
    {
        'brand': 'Replica',
        'name': 'RS-1',
        'description': 'Спортивный дизайн с 5 спицами, идеально подходит для спортивных автомобилей',
        'variants': [
            {'diameter': 17, 'width': 7.5, 'bolt_pattern': '5x114.3', 'offset': 45, 'dia': 73.1, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 8500},
            {'diameter': 18, 'width': 8.0, 'bolt_pattern': '5x114.3', 'offset': 40, 'dia': 73.1, 'color': 'Черный', 'material': 'Алюминий', 'price': 9500},
            {'diameter': 19, 'width': 8.5, 'bolt_pattern': '5x114.3', 'offset': 35, 'dia': 73.1, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 11500},
        ]
    },
    {
        'brand': 'BBS',
        'name': 'CH-R',
        'description': 'Классический дизайн с Y-образными спицами, премиальное качество',
        'variants': [
            {'diameter': 18, 'width': 8.0, 'bolt_pattern': '5x112', 'offset': 45, 'dia': 66.6, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 45000},
            {'diameter': 19, 'width': 8.5, 'bolt_pattern': '5x112', 'offset': 40, 'dia': 66.6, 'color': 'Черный', 'material': 'Алюминий', 'price': 52000},
        ]
    },
    {
        'brand': 'OZ',
        'name': 'Ultraleggera',
        'description': 'Легкосплавные диски с уникальным дизайном, минимальный вес',
        'variants': [
            {'diameter': 17, 'width': 7.5, 'bolt_pattern': '5x100', 'offset': 48, 'dia': 56.1, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 32000},
            {'diameter': 18, 'width': 8.0, 'bolt_pattern': '5x100', 'offset': 45, 'dia': 56.1, 'color': 'Черный', 'material': 'Алюминий', 'price': 38000},
        ]
    },
    {
        'brand': 'Enkei',
        'name': 'RPF1',
        'description': 'Легкие гоночные диски с классическим дизайном',
        'variants': [
            {'diameter': 16, 'width': 7.0, 'bolt_pattern': '4x100', 'offset': 43, 'dia': 73.1, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 15000},
            {'diameter': 17, 'width': 7.5, 'bolt_pattern': '4x100', 'offset': 40, 'dia': 73.1, 'color': 'Черный', 'material': 'Алюминий', 'price': 18000},
        ]
    },
    {
        'brand': 'Rial',
        'name': 'Lucca',
        'description': 'Элегантный дизайн с 10 спицами, отличное соотношение цена/качество',
        'variants': [
            {'diameter': 17, 'width': 7.5, 'bolt_pattern': '5x108', 'offset': 45, 'dia': 63.4, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 12000},
            {'diameter': 18, 'width': 8.0, 'bolt_pattern': '5x108', 'offset': 40, 'dia': 63.4, 'color': 'Черный', 'material': 'Алюминий', 'price': 14000},
            {'diameter': 19, 'width': 8.5, 'bolt_pattern': '5x108', 'offset': 35, 'dia': 63.4, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 16000},
        ]
    },
    {
        'brand': 'Aez',
        'name': 'Kiel',
        'description': 'Современный дизайн с двойными спицами, доступная цена',
        'variants': [
            {'diameter': 16, 'width': 7.0, 'bolt_pattern': '4x100', 'offset': 45, 'dia': 73.1, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 8000},
            {'diameter': 17, 'width': 7.5, 'bolt_pattern': '4x100', 'offset': 40, 'dia': 73.1, 'color': 'Черный', 'material': 'Алюминий', 'price': 9500},
        ]
    },
    {
        'brand': 'Dotz',
        'name': 'Hanzo',
        'description': 'Агрессивный дизайн с острыми спицами, стильный внешний вид',
        'variants': [
            {'diameter': 18, 'width': 8.0, 'bolt_pattern': '5x114.3', 'offset': 40, 'dia': 73.1, 'color': 'Черный', 'material': 'Алюминий', 'price': 22000},
            {'diameter': 19, 'width': 8.5, 'bolt_pattern': '5x114.3', 'offset': 35, 'dia': 73.1, 'color': 'Серебристый', 'material': 'Алюминий', 'price': 25000},
            {'diameter': 20, 'width': 9.0, 'bolt_pattern': '5x114.3', 'offset': 30, 'dia': 73.1, 'color': 'Черный', 'material': 'Алюминий', 'price': 28000},
        ]
    },
    {
        'brand': 'Rays',
        'name': 'Volk Racing TE37',
        'description': 'Культовые кованые диски с уникальным дизайном, легкий вес и высокая прочность',
        'variants': [
            {'diameter': 17, 'width': 8.0, 'bolt_pattern': '5x114.3', 'offset': 35, 'dia': 73.1, 'color': 'Бронза', 'material': 'Кованый алюминий', 'price': 65000},
            {'diameter': 18, 'width': 9.5, 'bolt_pattern': '5x114.3', 'offset': 22, 'dia': 73.1, 'color': 'Черный', 'material': 'Кованый алюминий', 'price': 75000},
            {'diameter': 19, 'width': 10.5, 'bolt_pattern': '5x114.3', 'offset': 15, 'dia': 73.1, 'color': 'Бронза', 'material': 'Кованый алюминий', 'price': 85000},
        ]
    },
    {
        'brand': 'Work',
        'name': 'Emotion CR Kai',
        'description': 'Современный дизайн с двойными спицами, популярный выбор для тюнинга',
        'variants': [
            {'diameter': 17, 'width': 9.0, 'bolt_pattern': '5x114.3', 'offset': 17, 'dia': 73.1, 'color': 'Белый', 'material': 'Алюминий', 'price': 20000},
            {'diameter': 18, 'width': 9.5, 'bolt_pattern': '5x114.3', 'offset': 30, 'dia': 73.1, 'color': 'Матовый бронзовый', 'material': 'Алюминий', 'price': 24000},
            {'diameter': 19, 'width': 10.0, 'bolt_pattern': '5x114.3', 'offset': 25, 'dia': 73.1, 'color': 'Черный', 'material': 'Алюминий', 'price': 28000},
        ]
    },
    {
        'brand': 'Vossen',
        'name': 'HF-3',
        'description': 'Премиальные диски с уникальным дизайном, идеально подходят для люксовых автомобилей',
        'variants': [
            {'diameter': 20, 'width': 9.0, 'bolt_pattern': '5x112', 'offset': 32, 'dia': 66.6, 'color': 'Глянцевый черный', 'material': 'Гибридный кованый', 'price': 40000},
            {'diameter': 20, 'width': 10.5, 'bolt_pattern': '5x120', 'offset': 42, 'dia': 72.5, 'color': 'Двойной глянцевый черный', 'material': 'Гибридный кованый', 'price': 45000},
            {'diameter': 21, 'width': 11.0, 'bolt_pattern': '5x112', 'offset': 35, 'dia': 66.6, 'color': 'Глянцевый черный', 'material': 'Гибридный кованый', 'price': 50000},
        ]
    },
    {
        'brand': 'Rotiform',
        'name': 'LAS-R',
        'description': 'Стильные диски с агрессивным дизайном, популярны в стэнс-культуре',
        'variants': [
            {'diameter': 19, 'width': 8.5, 'bolt_pattern': '5x112', 'offset': 35, 'dia': 57.1, 'color': 'Серебристый машинный', 'material': 'Алюминий', 'price': 25000},
            {'diameter': 19, 'width': 10.0, 'bolt_pattern': '5x120', 'offset': 40, 'dia': 72.5, 'color': 'Серебристый машинный', 'material': 'Алюминий', 'price': 28000},
            {'diameter': 20, 'width': 10.5, 'bolt_pattern': '5x112', 'offset': 30, 'dia': 57.1, 'color': 'Черный машинный', 'material': 'Алюминий', 'price': 32000},
        ]
    }
]

# Добавляем диски в базу данных
for rim_data in rims_data:
    rim = RimModel.objects.create(
        brand=rim_data['brand'],
        name=rim_data['name'],
        description=rim_data['description']
    )
    print(f"Добавлена модель диска: {rim.brand} {rim.name}")
    
    for variant_data in rim_data['variants']:
        RimVariant.objects.create(
            model=rim,
            **variant_data
        )

print("Диски успешно добавлены в базу данных!")
print(f"Всего моделей дисков в базе: {RimModel.objects.count()} шт.") 